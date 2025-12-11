"""
Cliente para Directions API
Calcula rotas, tempos de viagem e distâncias entre pontos
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime
from api.google_maps import get_client


class DirectionsAPI:
    """Cliente para Directions API"""
    
    def __init__(self):
        self.client = get_client()
    
    # def calcular_rota(
    #     self,
    #     origem: Tuple[float, float],
    #     destino: Tuple[float, float],
    #     modo: str = "driving",
    #     departure_time: Optional[datetime] = None,
    #     alternatives: bool = False
    # ) -> Dict:
    #     """
    #     Calcula rota entre dois pontos
        
    #     Args:
    #         origem: (lat, lng) ponto inicial
    #         destino: (lat, lng) ponto final
    #         modo: 'driving', 'walking', 'bicycling', 'transit'
    #         departure_time: Horário de partida (para considerar tráfego)
    #         alternatives: Se deve retornar rotas alternativas
        
    #     Returns:
    #         Dicionário com informações da rota
    #     """
    #     params = {
    #         'origin': origem,
    #         'destination': destino,
    #         'mode': modo,
    #         'alternatives': alternatives,
    #         'departure_time': departure_time or datetime.now()
    #     }
        
    #     resultado = self.client._fazer_requisicao(
    #         api_name='directions',
    #         api_method=self.client.client.directions,
    #         params=params
    #     )
        
    #     return self._processar_resultado(resultado)



    def calcular_rota(
        self,
        origem: Tuple[float, float],
        destino: Tuple[float, float],
        modo: str = "driving",
        departure_time: Optional[datetime] = None,
        alternatives: bool = False
    ) -> Dict:
        """
        Calcula rota entre dois pontos
        
        Args:
            origem: (lat, lng) ponto inicial
            destino: (lat, lng) ponto final
            modo: 'driving', 'walking', 'bicycling', 'transit'
            departure_time: Horário de partida (para considerar tráfego)
            alternatives: Se deve retornar rotas alternativas
        
        Returns:
            Dicionário com informações da rota
        """
        params = {
            'origin': origem,
            'destination': destino,
            'mode': modo,
            'alternatives': alternatives
        }
        
        # Só adicionar departure_time se foi especificado
        if departure_time is not None:
            params['departure_time'] = departure_time
        
        resultado = self.client._fazer_requisicao(
            api_name='directions',
            api_method=self.client.client.directions,
            params=params
        )
        
        return self._processar_resultado(resultado)






    
    def _processar_resultado(self, resultado: List[Dict]) -> Dict:
        """Processa resultado da API para formato simplificado"""
        if not resultado:
            return {}
        
        rota = resultado[0]  # Primeira rota
        leg = rota['legs'][0]  # Primeiro trecho
        
        return {
            'distancia_metros': leg['distance']['value'],
            'distancia_texto': leg['distance']['text'],
            'duracao_segundos': leg['duration']['value'],
            'duracao_texto': leg['duration']['text'],
            'duracao_trafego_segundos': leg.get('duration_in_traffic', {}).get('value'),
            'origem': leg['start_address'],
            'destino': leg['end_address'],
            'polyline': rota['overview_polyline']['points'],
            'passos': len(leg['steps']),
            'rotas_alternativas': len(resultado) - 1
        }
    
    def calcular_multiplas_rotas(
        self,
        origem: Tuple[float, float],
        destinos: List[Tuple[float, float]],
        modo: str = "driving"
    ) -> List[Dict]:
        """
        Calcula rotas de uma origem para múltiplos destinos
        
        Args:
            origem: (lat, lng) ponto inicial
            destinos: Lista de (lat, lng) destinos
            modo: Modo de transporte
        
        Returns:
            Lista de rotas processadas
        """
        rotas = []
        for destino in destinos:
            rota = self.calcular_rota(origem, destino, modo)
            if rota:
                rotas.append(rota)
        
        return rotas
    
    def analisar_trafego(
        self,
        origem: Tuple[float, float],
        destino: Tuple[float, float],
        horarios: List[int]
    ) -> List[Dict]:
        """
        Analisa tráfego em diferentes horários
        
        Args:
            origem: (lat, lng) ponto inicial
            destino: (lat, lng) ponto final
            horarios: Lista de horas do dia (0-23)
        
        Returns:
            Lista com análise de tráfego por horário
        """
        analises = []
        
        for hora in horarios:
            # Criar datetime para o horário específico
            agora = datetime.now()
            departure = agora.replace(hour=hora, minute=0, second=0)
            
            rota = self.calcular_rota(origem, destino, departure_time=departure)
            
            if rota:
                analises.append({
                    'hora': hora,
                    'duracao_normal': rota['duracao_segundos'],
                    'duracao_trafego': rota.get('duracao_trafego_segundos'),
                    'diferenca_percentual': self._calcular_diferenca(
                        rota['duracao_segundos'],
                        rota.get('duracao_trafego_segundos')
                    )
                })
        
        return analises
    
    def _calcular_diferenca(self, normal: int, trafego: Optional[int]) -> Optional[float]:
        """Calcula diferença percentual entre tempo normal e com tráfego"""
        if not trafego or normal == 0:
            return None
        return ((trafego - normal) / normal) * 100


# Instância global
_directions_client = None

def get_directions_client() -> DirectionsAPI:
    """Retorna instância única do cliente Directions"""
    global _directions_client
    if _directions_client is None:
        _directions_client = DirectionsAPI()
    return _directions_client