"""
Dashboard Streamlit - Exploração APIs Google
Visualização de dados para planejamento de eletropostos
"""

import streamlit as st
from config.settings import STREAMLIT_CONFIG
from components.sidebar import render_sidebar
from components.mapa import render_mapa
from components.dados import render_dados_eletropostos

# Configuração da página
st.set_page_config(**STREAMLIT_CONFIG)

# CSS para mapa fullscreen
st.markdown("""
    <style>
    .main .block-container {
        padding: 0.5rem 0.5rem 0rem 0.5rem;
        max-width: 100%;
    }
    iframe {
        width: 100%;
        height: 90vh;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizar sidebar e obter configurações
config = render_sidebar()

# LÓGICA DE COLETA (executada ANTES das abas)
if config['btn_coletar']:
    with st.spinner("Coletando dados das APIs..."):
        
        # Eletropostos
        if config['modulos']['eletropostos']:
            from api.places import get_places_client
            places_client = get_places_client()
            
            eletropostos = places_client.buscar_eletropostos(
                location=(config['lat_centro'], config['lng_centro']),
                radius_meters=config['raio_km'] * 1000
            )
            
            # Salvar em session_state
            st.session_state['eletropostos'] = eletropostos
            st.session_state['dados_coletados'] = True
        
        # Outros módulos (preparar para futuro)
        if config['modulos']['pois']:
            st.session_state['pois'] = []  
        
        if config['modulos']['rotas']:
            st.session_state['rotas'] = []  
        
        if config['modulos']['conectividade']:
            st.session_state['conectividade'] = {}  

# Sistema de abas
tab_mapa, tab_dados = st.tabs(["Mapa", "Dados"])

# ABA: MAPA
with tab_mapa:
    # Verificar se existem dados coletados
    eletropostos_mapa = st.session_state.get('eletropostos', None)
    
    # Renderizar mapa (com ou sem eletropostos)
    map_data = render_mapa(
        lat_centro=config['lat_centro'],
        lng_centro=config['lng_centro'],
        raio_km=config['raio_km'],
        eletropostos=eletropostos_mapa,
        tema='claro'  # Mudar para 'escuro' quando quiser
    )
    
    # Processar clique
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lng = map_data["last_clicked"]["lng"]
        st.info(f"Ponto selecionado: ({clicked_lat:.6f}, {clicked_lng:.6f})")
    
    # Informação sobre dados no mapa
    if eletropostos_mapa:
        st.success(f"Exibindo {len(eletropostos_mapa)} eletropostos no mapa")
    else:
        st.info("Nenhum dado coletado ainda. Configure na sidebar e clique em 'Coletar dados'")

# ABA: DADOS
with tab_dados:
    if st.session_state.get('dados_coletados', False):
        
        # Eletropostos
        if config['modulos']['eletropostos']:
            st.subheader("Eletropostos existentes")
            eletropostos = st.session_state.get('eletropostos', [])
            render_dados_eletropostos(eletropostos)
        
        # Outros módulos
        if config['modulos']['pois']:
            st.subheader("POIs relevantes")
            st.info("Módulo em desenvolvimento")
        
        if config['modulos']['rotas']:
            st.subheader("Análise de rotas")
            st.info("Módulo em desenvolvimento")
        
        if config['modulos']['conectividade']:
            st.subheader("Conectividade")
            st.info("Módulo em desenvolvimento")
    else:
        st.info("Clique em 'Coletar dados' na sidebar para iniciar")









