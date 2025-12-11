"""
Cliente para Roads API
Obtém informações sobre vias, velocidades e tráfego
"""

import requests
from typing import List, Tuple, Dict, Optional
from config.settings import GOOGLE_MAPS_API_KEY


class RoadsAPI:
    """Cliente para Roads API"""
    
    SNAP_TO_ROADS_URL = "https://roads.googleapis.com/v1/snapToRoads"
    NEAREST_ROADS_URL = "https://roads.googleapis.com/v1/nearestRoads"
    SPEED_LIMITS_URL = "https://roads.googleapis.com/v1/speedLimits"
    
    def __init__(self):
        self.api_key = GOOGLE_MAPS_API_KEY
    
    def snap_to_roads(
        self,
        pontos: List[Tuple[float, float]],
        interpolate: bool = True
    ) -> List[Dict]:
        """
        Ajusta pontos GPS para as vias mais próximas
        
        Args:
            pontos: Lista de (lat, lng)
            interpolate: Se deve interpolar pontos entre os fornecidos
        
        Returns:
            Lista de pontos ajustados às vias
        """
        # Formatar pontos como string
        path = "|".join([f"{lat},{lng}" for lat, lng in pontos])
        
        params = {
            'path': path,
            'interpolate': str(interpolate).lower(),
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.SNAP_TO_ROADS_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._processar_snap_result(data)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na Roads API (snap): {e}")
            return []
    
    def _processar_snap_result(self, data: Dict) -> List[Dict]:
        """Processa resultado do snap to roads"""
        if 'snappedPoints' not in data:
            return []
        
        pontos_processados = []
        
        for point in data['snappedPoints']:
            pontos_processados.append({
                'lat': point['location']['latitude'],
                'lng': point['location']['longitude'],
                'place_id': point.get('placeId'),
                'original_index': point.get('originalIndex')
            })
        
        return pontos_processados
    
    def nearest_roads(
        self,
        pontos: List[Tuple[float, float]]
    ) -> List[Dict]:
        """
        Encontra as vias mais próximas de pontos específicos
        
        Args:
            pontos: Lista de (lat, lng)
        
        Returns:
            Lista de vias mais próximas
        """
        # Formatar pontos como string
        points_str = "|".join([f"{lat},{lng}" for lat, lng in pontos])
        
        params = {
            'points': points_str,
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.NEAREST_ROADS_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._processar_nearest_result(data)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na Roads API (nearest): {e}")
            return []
    
    def _processar_nearest_result(self, data: Dict) -> List[Dict]:
        """Processa resultado do nearest roads"""
        if 'snappedPoints' not in data:
            return []
        
        vias = []
        
        for point in data['snappedPoints']:
            vias.append({
                'lat': point['location']['latitude'],
                'lng': point['location']['longitude'],
                'place_id': point.get('placeId')
            })
        
        return vias
    
    def get_speed_limits(
        self,
        place_ids: List[str]
    ) -> List[Dict]:
        """
        Obtém limites de velocidade para vias específicas
        
        Args:
            place_ids: Lista de Place IDs das vias
        
        Returns:
            Lista com limites de velocidade
        """
        params = {
            'placeId': place_ids,
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.SPEED_LIMITS_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._processar_speed_limits(data)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na Roads API (speed limits): {e}")
            return []
    
    def _processar_speed_limits(self, data: Dict) -> List[Dict]:
        """Processa resultado dos limites de velocidade"""
        if 'speedLimits' not in data:
            return []
        
        limites = []
        
        for limit in data['speedLimits']:
            limites.append({
                'place_id': limit.get('placeId'),
                'speed_limit_kmh': limit.get('speedLimit'),
                'units': limit.get('units', 'KPH')
            })
        
        return limites
    
    def analisar_via(
        self,
        pontos: List[Tuple[float, float]]
    ) -> Dict:
        """
        Análise completa de uma via (snap + speed limits)
        
        Args:
            pontos: Lista de pontos ao longo da via
        
        Returns:
            Análise completa da via
        """
        # Ajustar pontos à via
        pontos_ajustados = self.snap_to_roads(pontos)
        
        if not pontos_ajustados:
            return {}
        
        # Extrair place_ids únicos
        place_ids = list(set([
            p['place_id'] for p in pontos_ajustados 
            if p.get('place_id')
        ]))
        
        # Obter limites de velocidade
        limites = []
        if place_ids:
            limites = self.get_speed_limits(place_ids[:100])  # Máximo 100 por requisição
        
        return {
            'pontos_ajustados': pontos_ajustados,
            'total_pontos': len(pontos_ajustados),
            'place_ids': place_ids,
            'limites_velocidade': limites,
            'velocidade_media_kmh': self._calcular_velocidade_media(limites)
        }
    
    def _calcular_velocidade_media(self, limites: List[Dict]) -> Optional[float]:
        """Calcula velocidade média dos limites encontrados"""
        if not limites:
            return None
        
        velocidades = [l['speed_limit_kmh'] for l in limites if l.get('speed_limit_kmh')]
        
        if not velocidades:
            return None
        
        return sum(velocidades) / len(velocidades)


# Instância global
_roads_client = None

def get_roads_client() -> RoadsAPI:
    """Retorna instância única do cliente Roads"""
    global _roads_client
    if _roads_client is None:
        _roads_client = RoadsAPI()
    return _roads_client