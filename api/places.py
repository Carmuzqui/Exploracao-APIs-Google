"""
Cliente para Places API (New) - Google Maps Platform
Suporta busca de POIs, incluindo estações de carregamento VE
"""

import requests
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
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.types,places.evChargeOptions'
        }
    
    def nearby_search(
        self,
        location: Tuple[float, float],
        radius_meters: int = 5000,
        included_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Busca lugares próximos a uma localização
        
        Args:
            location: (latitude, longitude)
            radius_meters: Raio de busca em metros
            included_types: Tipos de lugares (ex: ['electric_vehicle_charging_station'])
        
        Returns:
            Lista de lugares encontrados
        """
        url = f"{self.BASE_URL}:searchNearby"
        
        payload = {
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": location[0],
                        "longitude": location[1]
                    },
                    "radius": radius_meters
                }
            }
        }
        
        if included_types:
            payload["includedTypes"] = included_types
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return data.get('places', [])
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na Places API (New): {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Detalhes: {e.response.text}")
            return []
    
    def buscar_eletropostos(
        self,
        location: Tuple[float, float],
        radius_meters: int = 5000
    ) -> List[Dict]:
        """
        Busca estações de carregamento de VE próximas
        
        Args:
            location: (latitude, longitude)
            radius_meters: Raio de busca em metros
        
        Returns:
            Lista de eletropostos com informações detalhadas
        """
        return self.nearby_search(
            location=location,
            radius_meters=radius_meters,
            included_types=['electric_vehicle_charging_station']
        )
    
    def testar_conexao(self) -> bool:
        """Testa conexão com Places API (New)"""
        try:
            # Buscar eletropostos em Campinas
            resultado = self.buscar_eletropostos(
                location=(-22.9056, -47.0608),
                radius_meters=5000
            )
            
            if resultado is not None:
                print(f"✓ Places API (New): OK - {len(resultado)} eletropostos encontrados")
                return True
            return False
            
        except Exception as e:
            print(f"✗ Places API (New): {e}")
            return False


# Instância global
_places_client = None

def get_places_client() -> PlacesAPINew:
    """Retorna instância única do cliente Places"""
    global _places_client
    if _places_client is None:
        _places_client = PlacesAPINew()
    return _places_client