"""
Componente: Mapa interativo fullscreen
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config.settings import DEFAULT_ZOOM


def render_mapa(lat_centro, lng_centro, raio_km, tema='claro'):
    """
    Renderiza mapa interativo
    
    Args:
        lat_centro: Latitude do centro
        lng_centro: Longitude do centro
        raio_km: Raio de busca em km
        tema: 'claro' ou 'escuro'
    
    Returns:
        Dados do mapa (cliques, etc)
    """
    
    # Selecionar tile baseado no tema
    tiles_config = {
        'claro': 'CartoDB positron',
        'escuro': 'CartoDB dark_matter'  # Mapa escuro moderno
    }
    
    # Criar mapa
    mapa = folium.Map(
        location=[lat_centro, lng_centro],
        zoom_start=DEFAULT_ZOOM,
        tiles=tiles_config.get(tema, 'CartoDB positron')
    )
    
    # Marcador central
    folium.Marker(
        [lat_centro, lng_centro],
        tooltip="Ponto central da área de interesse",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)
    
    # Círculo de raio
    folium.Circle(
        [lat_centro, lng_centro],
        radius=raio_km * 1000,
        color='blue',
        fill=True,
        fillOpacity=0.1,
        popup=f"Raio: {raio_km} km"
    ).add_to(mapa)
    
    # Renderizar com altura máxima
    map_data = st_folium(
        mapa,
        width=None,
        height=700,
        returned_objects=["last_clicked"]
    )
    
    return map_data


def adicionar_eletropostos_ao_mapa(mapa, eletropostos):
    """Adiciona marcadores de eletropostos ao mapa"""
    
    for posto in eletropostos:
        if 'location' in posto:
            lat = posto['location']['latitude']
            lng = posto['location']['longitude']
            nome = posto.get('displayName', {}).get('text', 'N/A')
            
            folium.Marker(
                [lat, lng],
                popup=nome,
                tooltip=nome,
                icon=folium.Icon(color='green', icon='bolt', prefix='fa')
            ).add_to(mapa)
    
    return mapa