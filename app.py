# """
# Dashboard Streamlit - Exploração APIs Google
# Visualização de dados para planejamento de eletropostos
# """

# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from config.settings import (
#     STREAMLIT_CONFIG,
#     DEFAULT_CENTER,
#     DEFAULT_ZOOM
# )

# # Configuração da página
# st.set_page_config(**STREAMLIT_CONFIG)

# # CSS customizado para mapa fullscreen
# st.markdown("""
#     <style>
#     /* Remover padding padrão */
#     .main .block-container {
#         padding-top: 1rem;
#         padding-bottom: 0rem;
#         padding-left: 1rem;
#         padding-right: 1rem;
#     }
    
#     /* Mapa fullscreen */
#     iframe {
#         width: 100%;
#         height: 85vh;
#     }
#     </style>
# """, unsafe_allow_html=True)


# # Sidebar (ocultável)
# with st.sidebar:
#     st.header("Configurações")
    
#     # Seleção de área
#     st.subheader("🗺️ Área de interesse")
#     st.markdown("Coordenadas do centro:")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         lat_centro = st.number_input(
#             "Latitude",
#             value=DEFAULT_CENTER['lat'],
#             format="%.6f"
#         )
#     with col2:
#         lng_centro = st.number_input(
#             "Longitude",
#             value=DEFAULT_CENTER['lng'],
#             format="%.6f"
#         )
    
#     raio_km = st.slider(
#         "Raio de busca (km):",
#         min_value=1,
#         max_value=20,
#         value=5
#     )
    
#     # Módulos
#     st.subheader("Consultas")
    
#     modulo_eletropostos = st.checkbox("Eletropostos existentes", value=True)
#     modulo_pois = st.checkbox("POIs relevantes", value=False)
#     modulo_rotas = st.checkbox("Análise de rotas", value=False)
#     modulo_conectividade = st.checkbox("Conectividade", value=False)
    
#     # Botão de coleta
#     st.divider()
#     btn_coletar = st.button("🔍 Coletar dados", type="primary", use_container_width=True)
    
    

# # Criar mapa base
# mapa = folium.Map(
#     location=[lat_centro, lng_centro],
#     zoom_start=DEFAULT_ZOOM,
#     tiles='CartoDB positron'
# )

# # Adicionar marcador do centro
# folium.Marker(
#     [lat_centro, lng_centro],
#     # popup="Centro de busca",
#     tooltip="Ponto central da área de interese",
#     icon=folium.Icon(color='red', icon='info-sign')
# ).add_to(mapa)

# # Adicionar círculo de raio
# folium.Circle(
#     [lat_centro, lng_centro],
#     radius=raio_km * 1000,  # Converter para metros
#     color='blue',
#     fill=True,
#     fillOpacity=0.1,
#     popup=f"Raio: {raio_km} km"
# ).add_to(mapa)

# # Renderizar mapa
# map_data = st_folium(
#     mapa,
#     width=None,
#     height=600,
#     returned_objects=["last_clicked"]
# )

# # Processar clique no mapa
# if map_data and map_data.get("last_clicked"):
#     clicked_lat = map_data["last_clicked"]["lat"]
#     clicked_lng = map_data["last_clicked"]["lng"]
    
#     st.info(f"📍 Ponto selecionado: ({clicked_lat:.6f}, {clicked_lng:.6f})")

# # Área de resultados
# if btn_coletar:
#     st.subheader("Resultados")
    
#     with st.spinner("Coletando dados das APIs..."):
        
#         # Módulo: Eletropostos
#         if modulo_eletropostos:
#             with st.expander("⚡ Eletropostos Existentes", expanded=True):
#                 from api.places import get_places_client
                
#                 places_client = get_places_client()
#                 eletropostos = places_client.buscar_eletropostos(
#                     location=(lat_centro, lng_centro),
#                     radius_meters=raio_km * 1000
#                 )
                
#                 st.metric("Total encontrado", len(eletropostos))
                
#                 if eletropostos:
#                     for i, posto in enumerate(eletropostos[:5], 1):
#                         st.write(f"**{i}.** {posto.get('displayName', {}).get('text', 'N/A')}")
#                         st.caption(f"📍 {posto.get('formattedAddress', 'N/A')}")
        
#         # Módulo: POIs
#         if modulo_pois:
#             with st.expander("🏢 POIs Relevantes"):
#                 st.info("Módulo em desenvolvimento")
        
#         # Módulo: Rotas
#         if modulo_rotas:
#             with st.expander("🛣️ Análise de Rotas"):
#                 st.info("Módulo em desenvolvimento")
        
#         # Módulo: Conectividade
#         if modulo_conectividade:
#             with st.expander("🔗 Conectividade"):
#                 st.info("Módulo em desenvolvimento")












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

# Sistema de abas
tab_mapa, tab_dados = st.tabs(["Mapa", "Dados"])

# ABA: MAPA
with tab_mapa:
    map_data = render_mapa(
        lat_centro=config['lat_centro'],
        lng_centro=config['lng_centro'],
        raio_km=config['raio_km'],
        tema='claro'  # Mudar para 'escuro' quando quiser
    )
    
    # Processar clique
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lng = map_data["last_clicked"]["lng"]
        st.info(f"Ponto selecionado: ({clicked_lat:.6f}, {clicked_lng:.6f})")

# ABA: DADOS
with tab_dados:
    if config['btn_coletar']:
        with st.spinner("Coletando dados..."):
            
            # Eletropostos
            if config['modulos']['eletropostos']:
                st.subheader("Eletropostos existentes")
                
                from api.places import get_places_client
                places_client = get_places_client()
                
                eletropostos = places_client.buscar_eletropostos(
                    location=(config['lat_centro'], config['lng_centro']),
                    radius_meters=config['raio_km'] * 1000
                )
                
                render_dados_eletropostos(eletropostos)
                
                # Salvar em session_state para usar no mapa
                st.session_state['eletropostos'] = eletropostos
            
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

