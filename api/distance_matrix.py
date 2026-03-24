"""
Cliente para Distance Matrix API
Calcula distâncias e tempos entre múltiplos pontos
"""

from typing import List, Tuple, Dict, Optional
from datetime import datetime
from api.google_maps import get_client


class DistanceMatrixAPI:
    """Cliente para Distance Matrix API"""
    
    def __init__(self):
        self.client = get_client()
    
    def calcular_matriz(
        self,
        origens: List[Tuple[float, float]],
        destinos: List[Tuple[float, float]],
        modo: str = "driving",
        departure_time: Optional[datetime] = None
    ) -> Dict:
        """
        Calcula matriz de distâncias entre múltiplos pontos
        
        Args:
            origens: Lista de (lat, lng) pontos de origem
            destinos: Lista de (lat, lng) pontos de destino
            modo: 'driving', 'walking', 'bicycling', 'transit'
            departure_time: Horário de partida (para tráfego)
        
        Returns:
            Matriz de distâncias e tempos
        """
        params = {
            'origins': origens,
            'destinations': destinos,
            'mode': modo
        }
        
        if departure_time is not None:
            params['departure_time'] = departure_time
        
        resultado = self.client._fazer_requisicao(
            api_name='distance_matrix',
            api_method=self.client.client.distance_matrix,
            params=params
        )
        
        return self._processar_resultado(resultado, origens, destinos)
    
    def _processar_resultado(
        self,
        resultado: Dict,
        origens: List[Tuple[float, float]],
        destinos: List[Tuple[float, float]]
    ) -> Dict:
        """Processa resultado em formato estruturado"""
        if not resultado or 'rows' not in resultado:
            return {}
        
        matriz = []
        
        for i, row in enumerate(resultado['rows']):
            for j, element in enumerate(row['elements']):
                if element['status'] == 'OK':
                    matriz.append({
                        'origem_idx': i,
                        'destino_idx': j,
                        'origem_coords': origens[i],
                        'destino_coords': destinos[j],
                        'distancia_metros': element['distance']['value'],
                        'distancia_texto': element['distance']['text'],
                        'duracao_segundos': element['duration']['value'],
                        'duracao_texto': element['duration']['text'],
                        'duracao_trafego_segundos': element.get('duration_in_traffic', {}).get('value')
                    })
        
        return {
            'matriz': matriz,
            'total_origens': len(origens),
            'total_destinos': len(destinos),
            'total_pares': len(matriz)
        }
    
    def calcular_cobertura(
        self,
        ponto_central: Tuple[float, float],
        pontos_candidatos: List[Tuple[float, float]],
        raio_max_metros: int = 5000
    ) -> List[Dict]:
        """
        Calcula quais pontos estão dentro do raio de cobertura
        
        Args:
            ponto_central: (lat, lng) ponto central
            pontos_candidatos: Lista de pontos a verificar
            raio_max_metros: Raio máximo de cobertura
        
        Returns:
            Lista de pontos dentro da cobertura
        """
        resultado = self.calcular_matriz(
            origens=[ponto_central],
            destinos=pontos_candidatos
        )
        
        pontos_cobertos = []
        
        for item in resultado.get('matriz', []):
            if item['distancia_metros'] <= raio_max_metros:
                pontos_cobertos.append({
                    'coords': item['destino_coords'],
                    'distancia_metros': item['distancia_metros'],
                    'duracao_segundos': item['duracao_segundos'],
                    'dentro_cobertura': True
                })
        
        return pontos_cobertos
    
    def calcular_conectividade(
        self,
        pontos: List[Tuple[float, float]],
        raio_max_metros: int = 10000
    ) -> Dict:
        """
        Calcula conectividade entre todos os pontos (grafo completo)
        
        Args:
            pontos: Lista de pontos a analisar
            raio_max_metros: Distância máxima para considerar conectado
        
        Returns:
            Dicionário com métricas de conectividade
        """
        resultado = self.calcular_matriz(
            origens=pontos,
            destinos=pontos
        )
        
        conexoes = []
        total_conexoes_possiveis = len(pontos) * (len(pontos) - 1)
        
        for item in resultado.get('matriz', []):
            # Ignorar conexão consigo mesmo
            if item['origem_idx'] != item['destino_idx']:
                if item['distancia_metros'] <= raio_max_metros:
                    conexoes.append({
                        'origem': item['origem_idx'],
                        'destino': item['destino_idx'],
                        'distancia': item['distancia_metros'],
                        'tempo': item['duracao_segundos']
                    })
        
        return {
            'total_pontos': len(pontos),
            'conexoes': conexoes,
            'total_conexoes': len(conexoes),
            'conexoes_possiveis': total_conexoes_possiveis,
            'taxa_conectividade': len(conexoes) / total_conexoes_possiveis if total_conexoes_possiveis > 0 else 0
        }


# Instância global
_distance_matrix_client = None

def get_distance_matrix_client() -> DistanceMatrixAPI:
    """Retorna instância única do cliente Distance Matrix"""
    global _distance_matrix_client
    if _distance_matrix_client is None:
        _distance_matrix_client = DistanceMatrixAPI()
    return _distance_matrix_client