"""
Componente: Sidebar com controles
"""

import streamlit as st
from config.settings import DEFAULT_CENTER


def render_sidebar():
    """Renderiza sidebar com configurações"""
    
    with st.sidebar:
        st.header("Configurações")
        
        # Área de interesse
        st.subheader("Área de interesse")
        st.markdown("Coordenadas do centro:")
        
        col1, col2 = st.columns(2)
        with col1:
            lat_centro = st.number_input(
                "Latitude",
                value=DEFAULT_CENTER['lat'],
                format="%.6f",
                key="lat_centro"
            )
        with col2:
            lng_centro = st.number_input(
                "Longitude",
                value=DEFAULT_CENTER['lng'],
                format="%.6f",
                key="lng_centro"
            )
        
        raio_km = st.slider(
            "Raio de busca (km):",
            min_value=1,
            max_value=20,
            value=5,
            key="raio_km"
        )
        
        # Módulos
        st.subheader("Consultas")
        
        modulos = {
            'eletropostos': st.checkbox("Eletropostos existentes", value=True),
            'pois': st.checkbox("POIs relevantes", value=False),
            'rotas': st.checkbox("Análise de rotas", value=False),
            'conectividade': st.checkbox("Conectividade", value=False)
        }
        
        # Botão de coleta
        st.divider()
        btn_coletar = st.button("Coletar dados", type="primary", use_container_width=True)
        
        return {
            'lat_centro': lat_centro,
            'lng_centro': lng_centro,
            'raio_km': raio_km,
            'modulos': modulos,
            'btn_coletar': btn_coletar
        }