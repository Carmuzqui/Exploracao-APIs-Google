# """
# Cliente base para Google Maps API
# Gerencia requisições, cache e tratamento de erros
# """

# import googlemaps
# import pickle
# import hashlib
# import json
# from pathlib import Path
# from datetime import datetime, timedelta
# from typing import Dict, Any, Optional
# from config.settings import (
#     GOOGLE_MAPS_API_KEY,
#     CACHE_DIR,
#     CACHE_ENABLED,
#     CACHE_TTL_DAYS
# )


# class GoogleMapsClient:
#     """Cliente unificado para APIs Google Maps"""
    
#     def __init__(self):
#         """Inicializa cliente com API key"""
#         self.client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
#         self.cache_dir = CACHE_DIR
        
#     def _gerar_cache_key(self, api_name: str, params: Dict) -> str:
#         """Gera chave única para cache baseada em parâmetros"""
#         params_str = json.dumps(params, sort_keys=True)
#         hash_obj = hashlib.md5(params_str.encode())
#         return f"{api_name}_{hash_obj.hexdigest()}.pkl"
    
#     def _carregar_cache(self, cache_key: str) -> Optional[Any]:
#         """Carrega dados do cache se existir e não estiver expirado"""
#         if not CACHE_ENABLED:
#             return None
        
#         cache_path = self.cache_dir / cache_key
        
#         if not cache_path.exists():
#             return None
        
#         # Verificar se cache expirou
#         file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
#         if datetime.now() - file_time > timedelta(days=CACHE_TTL_DAYS):
#             cache_path.unlink()  # Deletar cache expirado
#             return None
        
#         # Carregar dados
#         with open(cache_path, 'rb') as f:
#             return pickle.load(f)
    
#     def _salvar_cache(self, cache_key: str, data: Any):
#         """Salva dados no cache"""
#         if not CACHE_ENABLED:
#             return
        
#         cache_path = self.cache_dir / cache_key
#         with open(cache_path, 'wb') as f:
#             pickle.dump(data, f)
    
#     def _fazer_requisicao(
#         self,
#         api_name: str,
#         api_method,
#         params: Dict,
#         usar_cache: bool = True
#     ) -> Any:
#         """
#         Método genérico para fazer requisições com cache
        
#         Args:
#             api_name: Nome da API (para cache)
#             api_method: Método da API a chamar
#             params: Parâmetros da requisição
#             usar_cache: Se deve usar cache
        
#         Returns:
#             Resposta da API
#         """
#         # Tentar carregar do cache
#         if usar_cache:
#             cache_key = self._gerar_cache_key(api_name, params)
#             cached_data = self._carregar_cache(cache_key)
            
#             if cached_data is not None:
#                 print(f"✓ Cache hit: {api_name}")
#                 return cached_data
        
#         # Fazer requisição
#         try:
#             print(f"→ Requisição API: {api_name}")
#             resultado = api_method(**params)
            
#             # Salvar no cache
#             if usar_cache:
#                 self._salvar_cache(cache_key, resultado)
            
#             return resultado
            
#         except googlemaps.exceptions.ApiError as e:
#             print(f"✗ Erro na API {api_name}: {e}")
#             raise
#         except Exception as e:
#             print(f"✗ Erro inesperado em {api_name}: {e}")
#             raise    
    

#     def testar_conexao(self) -> bool:
#         """Testa se a API key está funcionando com múltiplas APIs"""
#         testes = []
        
#         # Teste 1: Geocoding API
#         try:
#             result = self.client.geocode("Campinas, SP, Brasil")
#             if result:
#                 print("✓ Geocoding API: OK")
#                 testes.append(True)
#             else:
#                 testes.append(False)
#         except Exception as e:
#             print(f"✗ Geocoding API: {e}")
#             testes.append(False)
        
#         # Teste 2: Directions API
#         try:
#             result = self.client.directions(
#                 origin=(-22.9056, -47.0608),
#                 destination=(-22.9100, -47.0650),
#                 mode="driving"
#             )
#             if result:
#                 print("✓ Directions API: OK")
#                 testes.append(True)
#             else:
#                 testes.append(False)
#         except Exception as e:
#             print(f"✗ Directions API: {e}")
#             testes.append(False)        
        
#         # Teste 3: Places API (New)
#         try:
#             from api.places import get_places_client
#             places_client = get_places_client()
#             if places_client.testar_conexao():
#                 testes.append(True)
#             else:
#                 testes.append(False)
#         except Exception as e:
#             print(f"✗ Places API (New): {e}")
#             testes.append(False)
        
#         # Resultado final
#         if all(testes):
#             print("\n✓ Todas as APIs estão funcionando!")
#             return True
#         else:
#             print(f"\n⚠ {sum(testes)}/{len(testes)} APIs funcionando")
#             return False


# # Instância global (singleton)
# _client_instance = None

# def get_client() -> GoogleMapsClient:
#     """Retorna instância única do cliente"""
#     global _client_instance
#     if _client_instance is None:
#         _client_instance = GoogleMapsClient()
#     return _client_instance










"""
Cliente base para Google Maps API
Gerencia requisições, cache e tratamento de erros
"""

import googlemaps
import pickle
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from config.settings import (
    GOOGLE_MAPS_API_KEY,
    CACHE_DIR,
    CACHE_ENABLED,
    CACHE_TTL_DAYS
)


class GoogleMapsClient:
    """Cliente unificado para APIs Google Maps"""
    
    def __init__(self):
        """Inicializa cliente com API key"""
        self.client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        self.cache_dir = CACHE_DIR
        
    def _gerar_cache_key(self, api_name: str, params: Dict) -> str:
        """Gera chave única para cache baseada em parâmetros"""
        # Converter datetime para string antes de serializar
        params_serializaveis = self._preparar_params_para_cache(params)
        params_str = json.dumps(params_serializaveis, sort_keys=True)
        hash_obj = hashlib.md5(params_str.encode())
        return f"{api_name}_{hash_obj.hexdigest()}.pkl"

    def _preparar_params_para_cache(self, params: Dict) -> Dict:
        """Converte objetos não-serializáveis para formato compatível com JSON"""
        params_limpos = {}
        
        for key, value in params.items():
            if isinstance(value, datetime):
                # Converter datetime para timestamp
                params_limpos[key] = value.timestamp()
            elif isinstance(value, tuple):
                # Converter tuplas para listas
                params_limpos[key] = list(value)
            elif isinstance(value, dict):
                # Recursivo para dicionários aninhados
                params_limpos[key] = self._preparar_params_para_cache(value)
            else:
                params_limpos[key] = value
        
        return params_limpos
    
    def _carregar_cache(self, cache_key: str) -> Optional[Any]:
        """Carrega dados do cache se existir e não estiver expirado"""
        if not CACHE_ENABLED:
            return None
        
        cache_path = self.cache_dir / cache_key
        
        if not cache_path.exists():
            return None
        
        # Verificar se cache expirou
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if datetime.now() - file_time > timedelta(days=CACHE_TTL_DAYS):
            cache_path.unlink()  # Deletar cache expirado
            return None
        
        # Carregar dados
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    
    def _salvar_cache(self, cache_key: str, data: Any):
        """Salva dados no cache"""
        if not CACHE_ENABLED:
            return
        
        cache_path = self.cache_dir / cache_key
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
    
    def _fazer_requisicao(
        self,
        api_name: str,
        api_method,
        params: Dict,
        usar_cache: bool = True
    ) -> Any:
        """
        Método genérico para fazer requisições com cache
        
        Args:
            api_name: Nome da API (para cache)
            api_method: Método da API a chamar
            params: Parâmetros da requisição
            usar_cache: Se deve usar cache
        
        Returns:
            Resposta da API
        """
        # Tentar carregar do cache
        if usar_cache:
            cache_key = self._gerar_cache_key(api_name, params)
            cached_data = self._carregar_cache(cache_key)
            
            if cached_data is not None:
                print(f"✓ Cache hit: {api_name}")
                return cached_data
        
        # Fazer requisição
        try:
            print(f"→ Requisição API: {api_name}")
            resultado = api_method(**params)
            
            # Salvar no cache
            if usar_cache:
                self._salvar_cache(cache_key, resultado)
            
            return resultado
            
        except googlemaps.exceptions.ApiError as e:
            print(f"✗ Erro na API {api_name}: {e}")
            raise
        except Exception as e:
            print(f"✗ Erro inesperado em {api_name}: {e}")
            raise    
    

    def testar_conexao(self) -> bool:
        """Testa se a API key está funcionando com múltiplas APIs"""
        testes = []
        
        # Teste 1: Geocoding API
        try:
            result = self.client.geocode("Campinas, SP, Brasil")
            if result:
                print("✓ Geocoding API: OK")
                testes.append(True)
            else:
                testes.append(False)
        except Exception as e:
            print(f"✗ Geocoding API: {e}")
            testes.append(False)
        
        # Teste 2: Directions API
        try:
            result = self.client.directions(
                origin=(-22.9056, -47.0608),
                destination=(-22.9100, -47.0650),
                mode="driving"
            )
            if result:
                print("✓ Directions API: OK")
                testes.append(True)
            else:
                testes.append(False)
        except Exception as e:
            print(f"✗ Directions API: {e}")
            testes.append(False)        
        
        # Teste 3: Places API (New)
        try:
            from api.places import get_places_client
            places_client = get_places_client()
            if places_client.testar_conexao():
                testes.append(True)
            else:
                testes.append(False)
        except Exception as e:
            print(f"✗ Places API (New): {e}")
            testes.append(False)
        
        # Resultado final
        if all(testes):
            print("\n✓ Todas as APIs estão funcionando!")
            return True
        else:
            print(f"\n⚠ {sum(testes)}/{len(testes)} APIs funcionando")
            return False


# Instância global (singleton)
_client_instance = None

def get_client() -> GoogleMapsClient:
    """Retorna instância única do cliente"""
    global _client_instance
    if _client_instance is None:
        _client_instance = GoogleMapsClient()
    return _client_instance