# """
# Cliente para Places API (New) - Google Maps Platform
# Suporta busca de POIs, incluindo estações de carregamento VE
# """

# import requests
# from typing import Dict, List, Optional, Tuple
# from config.settings import GOOGLE_MAPS_API_KEY


# class PlacesAPINew:
#     """Cliente para Places API (New)"""
    
#     BASE_URL = "https://places.googleapis.com/v1/places"
    
#     def __init__(self):
#         self.api_key = GOOGLE_MAPS_API_KEY
#         self.headers = {
#             'Content-Type': 'application/json',
#             'X-Goog-Api-Key': self.api_key,
#             'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.types,places.evChargeOptions,places.id'
#         }
    
#     def nearby_search(
#         self,
#         location: Tuple[float, float],
#         radius_meters: int = 5000,
#         included_types: Optional[List[str]] = None
#     ) -> List[Dict]:
#         """
#         Busca lugares próximos a uma localização
        
#         Args:
#             location: (latitude, longitude)
#             radius_meters: Raio de busca em metros
#             included_types: Tipos de lugares (ex: ['electric_vehicle_charging_station'])
        
#         Returns:
#             Lista de lugares encontrados (máximo 20 por limitação da API)
#         """
#         url = f"{self.BASE_URL}:searchNearby"
        
#         payload = {
#             "locationRestriction": {
#                 "circle": {
#                     "center": {
#                         "latitude": location[0],
#                         "longitude": location[1]
#                     },
#                     "radius": radius_meters
#                 }
#             }
#         }
        
#         if included_types:
#             payload["includedTypes"] = included_types
        
#         try:
#             response = requests.post(url, json=payload, headers=self.headers)
#             response.raise_for_status()
            
#             data = response.json()
#             places = data.get('places', [])
            
#             print(f"✓ Places API: {len(places)} lugares encontrados")
#             return places
            
#         except requests.exceptions.RequestException as e:
#             print(f"✗ Erro na Places API (New): {e}")
#             if hasattr(e, 'response') and e.response is not None:
#                 print(f"   Detalhes: {e.response.text}")
#             return []
    
#     def buscar_eletropostos(
#         self,
#         location: Tuple[float, float],
#         radius_meters: int = 5000
#     ) -> List[Dict]:
#         """
#         Busca estações de carregamento de VE próximas
        
#         Args:
#             location: (latitude, longitude)
#             radius_meters: Raio de busca em metros
        
#         Returns:
#             Lista de eletropostos com informações detalhadas (máximo 20)
#         """
#         return self.nearby_search(
#             location=location,
#             radius_meters=radius_meters,
#             included_types=['electric_vehicle_charging_station']
#         )
    
#     def testar_conexao(self) -> bool:
#         """Testa conexão com Places API (New)"""
#         try:
#             # Buscar eletropostos em Campinas
#             resultado = self.buscar_eletropostos(
#                 location=(-22.9056, -47.0608),
#                 radius_meters=5000
#             )
            
#             if resultado is not None:
#                 print(f"✓ Places API (New): OK - {len(resultado)} eletropostos encontrados")
#                 return True
#             return False
            
#         except Exception as e:
#             print(f"✗ Places API (New): {e}")
#             return False


# # Instância global
# _places_client = None

# def get_places_client() -> PlacesAPINew:
#     """Retorna instância única do cliente Places"""
#     global _places_client
#     if _places_client is None:
#         _places_client = PlacesAPINew()
#     return _places_client








# """
# Cliente para Places API (New) - Google Maps Platform
# Suporta busca de POIs com MÁXIMA extração de informações
# """

# import requests
# import math
# from typing import Dict, List, Optional, Tuple
# from config.settings import GOOGLE_MAPS_API_KEY

# class PlacesAPINew:
#     """Cliente para Places API (New)"""
    
#     BASE_URL = "https://places.googleapis.com/v1/places"
    
#     def __init__(self):
#         self.api_key = GOOGLE_MAPS_API_KEY
#         # ¡Añadimos muchos más campos al FieldMask para enriquecer la tarjeta!
#         self.headers = {
#             'Content-Type': 'application/json',
#             'X-Goog-Api-Key': self.api_key,
#             'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.types,places.evChargeOptions,places.rating,places.userRatingCount,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours'
#         }
    
#     def nearby_search(
#         self,
#         location: Tuple[float, float],
#         radius_meters: int = 5000,
#         included_types: Optional[List[str]] = None
#     ) -> List[Dict]:
#         """Busca lugares próximos a una localización (Llamada base)"""
#         url = f"{self.BASE_URL}:searchNearby"
#         payload = {
#             "locationRestriction": {
#                 "circle": {
#                     "center": {"latitude": location[0], "longitude": location[1]},
#                     "radius": radius_meters
#                 }
#             }
#         }
#         if included_types:
#             payload["includedTypes"] = included_types
        
#         try:
#             response = requests.post(url, json=payload, headers=self.headers)
#             response.raise_for_status()
#             return response.json().get('places', [])
#         except requests.exceptions.RequestException as e:
#             print(f"✗ Erro na Places API (New): {e}")
#             return []
    
#     def buscar_eletropostos(
#         self,
#         location: Tuple[float, float],
#         radius_meters: int = 5000
#     ) -> List[Dict]:
#         """
#         Busca estações de carregamento usando uma estratégia de 5 pontos
#         para contornar o limite de 20 resultados da API.
#         """
#         lat, lng = location
#         # Raio da Terra em metros
#         R = 6378137 
#         # Deslocamento para os pontos auxiliares (metade do raio principal)
#         offset = radius_meters / 2
        
#         # Calcular deltas de latitude e longitude
#         dLat = (offset / R) * (180 / math.pi)
#         dLng = (offset / (R * math.cos(math.pi * lat / 180))) * (180 / math.pi)
        
#         # 5 pontos: Centro, Norte, Sul, Leste, Oeste
#         pontos_busca = [
#             (lat, lng),                  # Centro
#             (lat + dLat, lng),           # Norte
#             (lat - dLat, lng),           # Sul
#             (lat, lng + dLng),           # Leste
#             (lat, lng - dLng)            # Oeste
#         ]
        
#         todos_lugares = {} # Usar dicionário para evitar duplicados pelo ID
        
#         # Fazer a busca em cada ponto com um raio ligeiramente maior para garantir sobreposição
#         raio_busca = int(radius_meters * 0.75)
        
#         for ponto in pontos_busca:
#             lugares = self.nearby_search(
#                 location=ponto,
#                 radius_meters=raio_busca,
#                 included_types=['electric_vehicle_charging_station']
#             )
#             for lugar in lugares:
#                 if 'id' in lugar:
#                     todos_lugares[lugar['id']] = lugar
                    
#         resultados_finais = list(todos_lugares.values())
#         print(f"✓ Places API (Grid Search): {len(resultados_finais)} eletropostos únicos encontrados na área.")
#         return resultados_finais
    
#     def testar_conexao(self) -> bool:
#         try:
#             resultado = self.buscar_eletropostos(location=(-22.9056, -47.0608), radius_meters=5000)
#             if resultado is not None:
#                 print(f"✓ Places API: OK - {len(resultado)} eletropostos encontrados")
#                 return True
#             return False
#         except Exception as e:
#             print(f"✗ Places API (New): {e}")
#             return False

# _places_client = None

# def get_places_client() -> PlacesAPINew:
#     global _places_client
#     if _places_client is None:
#         _places_client = PlacesAPINew()
#     return _places_client







"""
Cliente para Places API (New) - Google Maps Platform
Suporta busca de POIs com MÁXIMA extração de informações
"""

import requests
import math
from typing import Dict, List, Optional, Tuple
from config.settings import GOOGLE_MAPS_API_KEY

class PlacesAPINew:
    """Cliente para Places API (New)"""
    
    BASE_URL = "https://places.googleapis.com/v1/places"
    
    def __init__(self):
        self.api_key = GOOGLE_MAPS_API_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.types,places.evChargeOptions,places.rating,places.userRatingCount,places.websiteUri,places.nationalPhoneNumber,places.regularOpeningHours'
        }

    @staticmethod
    def _calcular_distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula la distancia en metros entre dos coordenadas usando la fórmula de Haversine"""
        R = 6371000  # Radio medio de la Tierra en metros
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def nearby_search(
        self,
        location: Tuple[float, float],
        radius_meters: int = 5000,
        included_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """Busca lugares próximos a una localización (Llamada base)"""
        url = f"{self.BASE_URL}:searchNearby"
        payload = {
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": location[0], "longitude": location[1]},
                    "radius": radius_meters
                }
            }
        }
        if included_types:
            payload["includedTypes"] = included_types
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json().get('places', [])
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na Places API (New): {e}")
            return []
    
    def buscar_eletropostos(
        self,
        location: Tuple[float, float],
        radius_meters: int = 5000
    ) -> List[Dict]:
        """
        Busca estações de carregamento usando malha de 9 pontos 
        e filtro estrito de distância.
        """
        lat, lng = location
        R = 6378137 # Raio equatorial da Terra em metros
        
        # Deslocamento ajustado para criar uma malha 3x3 que cubra a área
        offset = radius_meters * 0.6 
        
        dLat = (offset / R) * (180 / math.pi)
        dLng = (offset / (R * math.cos(math.pi * lat / 180))) * (180 / math.pi)
        
        # Malha de 9 pontos para evitar saturar o limite de 20 resultados em áreas densas
        pontos_busca = [
            (lat, lng),                  # Centro
            (lat + dLat, lng),           # Norte
            (lat - dLat, lng),           # Sul
            (lat, lng + dLng),           # Leste
            (lat, lng - dLng),           # Oeste
            (lat + dLat, lng + dLng),    # Nordeste
            (lat + dLat, lng - dLng),    # Noroeste
            (lat - dLat, lng + dLng),    # Sudeste
            (lat - dLat, lng - dLng)     # Sudoeste
        ]
        
        todos_lugares = {}
        # O raio de cada sub-busca deve ser suficiente para sobrepor, mas não tão grande que sature
        raio_busca = int(radius_meters * 0.55)
        
        # Fazer as buscas
        for ponto in pontos_busca:
            lugares = self.nearby_search(
                location=ponto,
                radius_meters=raio_busca,
                included_types=['electric_vehicle_charging_station']
            )
            for lugar in lugares:
                if 'id' in lugar:
                    todos_lugares[lugar['id']] = lugar
                    
        # FILTRO ESTRITO DE DISTÂNCIA (Garante que nenhum ponto saia do círculo do mapa)
        resultados_filtrados = []
        for lugar in todos_lugares.values():
            if 'location' in lugar:
                lugar_lat = lugar['location']['latitude']
                lugar_lng = lugar['location']['longitude']
                distancia_real = self._calcular_distancia_haversine(lat, lng, lugar_lat, lugar_lng)
                
                if distancia_real <= radius_meters:
                    # Guardamos a distância exata para exibir na interface/tabela
                    lugar['distancia_centro_m'] = round(distancia_real)
                    resultados_filtrados.append(lugar)
                    
        print(f"✓ Places API: {len(resultados_filtrados)} eletropostos validados dentro do raio estrito.")
        return resultados_filtrados
    
    def testar_conexao(self) -> bool:
        try:
            resultado = self.buscar_eletropostos(location=(-22.9056, -47.0608), radius_meters=5000)
            if resultado is not None:
                print(f"✓ Places API: OK - {len(resultado)} eletropostos encontrados")
                return True
            return False
        except Exception as e:
            print(f"✗ Places API (New): {e}")
            return False

_places_client = None

def get_places_client() -> PlacesAPINew:
    global _places_client
    if _places_client is None:
        _places_client = PlacesAPINew()
    return _places_client