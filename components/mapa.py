# """
# Componente: Mapa interativo fullscreen
# """

# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from config.settings import DEFAULT_ZOOM


# def render_mapa(lat_centro, lng_centro, raio_km, eletropostos=None, tema='claro'):
#     """
#     Renderiza mapa interativo
    
#     Args:
#         lat_centro: Latitude do centro
#         lng_centro: Longitude do centro
#         raio_km: Raio de busca em km
#         eletropostos: Lista opcional de eletropostos para desenhar
#         tema: 'claro' ou 'escuro'
    
#     Returns:
#         Dados do mapa (cliques, etc)
#     """
    
#     # Selecionar tile baseado no tema
#     tiles_config = {
#         'claro': 'CartoDB positron',
#         'escuro': 'CartoDB dark_matter'  # Mapa escuro moderno
#     }
    
#     # Criar mapa
#     mapa = folium.Map(
#         location=[lat_centro, lng_centro],
#         zoom_start=DEFAULT_ZOOM,
#         tiles=tiles_config.get(tema, 'CartoDB positron')
#     )
    
#     # Marcador central
#     folium.Marker(
#         [lat_centro, lng_centro],
#         tooltip="Ponto central da área de interesse",
#         icon=folium.Icon(color='red', icon='info-sign')
#     ).add_to(mapa)
    
#     # Círculo de raio
#     folium.Circle(
#         [lat_centro, lng_centro],
#         radius=raio_km * 1000,
#         color='blue',
#         fill=True,
#         fillOpacity=0.1,
#         popup=f"Raio: {raio_km} km"
#     ).add_to(mapa)
    
#     # Adicionar eletropostos se fornecidos
#     if eletropostos:
#         mapa = adicionar_eletropostos_ao_mapa(mapa, eletropostos)
    
#     # Renderizar com altura máxima
#     map_data = st_folium(
#         mapa,
#         width=None,
#         height=700,
#         returned_objects=["last_clicked"]
#     )
    
#     return map_data


# def adicionar_eletropostos_ao_mapa(mapa, eletropostos):
#     """Adiciona marcadores de eletropostos ao mapa"""
    
#     for i, posto in enumerate(eletropostos, 1):
#         if 'location' in posto:
#             lat = posto['location']['latitude']
#             lng = posto['location']['longitude']
#             nome = posto.get('displayName', {}).get('text', f'Eletroposto {i}')
#             endereco = posto.get('formattedAddress', 'Endereço não disponível')
            
#             # Criar popup com informações detalhadas
#             popup_html = f"""
#             <div style="font-family: Arial; width: 200px;">
#                 <h4 style="margin: 0 0 10px 0; color: #2e7d32;">{nome}</h4>
#                 <p style="margin: 5px 0; font-size: 12px;">
#                     <b>Endereço:</b><br>{endereco}
#                 </p>
#                 <p style="margin: 5px 0; font-size: 11px; color: #666;">
#                     <b>Coordenadas:</b><br>
#                     {lat:.6f}, {lng:.6f}
#                 </p>
#             </div>
#             """
            
#             folium.Marker(
#                 [lat, lng],
#                 popup=folium.Popup(popup_html, max_width=250),
#                 tooltip=nome,
#                 icon=folium.Icon(color='green', icon='bolt', prefix='fa')
#             ).add_to(mapa)
    
#     return mapa










# """
# Componente: Mapa interativo fullscreen con popup enriquecido
# """

# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from config.settings import DEFAULT_ZOOM

# def render_mapa(lat_centro, lng_centro, raio_km, eletropostos=None, tema='claro'):
#     tiles_config = {
#         'claro': 'CartoDB positron',
#         'escuro': 'CartoDB dark_matter'
#     }
    
#     mapa = folium.Map(
#         location=[lat_centro, lng_centro],
#         zoom_start=DEFAULT_ZOOM,
#         tiles=tiles_config.get(tema, 'CartoDB positron')
#     )
    
#     folium.Marker(
#         [lat_centro, lng_centro],
#         tooltip="Ponto central da área de interesse",
#         icon=folium.Icon(color='red', icon='info-sign')
#     ).add_to(mapa)
    
#     folium.Circle(
#         [lat_centro, lng_centro],
#         radius=raio_km * 1000,
#         color='blue',
#         fill=True,
#         fillOpacity=0.1,
#         popup=f"Raio: {raio_km} km"
#     ).add_to(mapa)
    
#     if eletropostos:
#         mapa = adicionar_eletropostos_ao_mapa(mapa, eletropostos)
    
#     map_data = st_folium(
#         mapa,
#         width=None,
#         height=700,
#         returned_objects=["last_clicked"]
#     )
#     return map_data

# def adicionar_eletropostos_ao_mapa(mapa, eletropostos):
#     for i, posto in enumerate(eletropostos, 1):
#         if 'location' in posto:
#             lat = posto['location']['latitude']
#             lng = posto['location']['longitude']
#             nome = posto.get('displayName', {}).get('text', f'Eletroposto {i}')
#             endereco = posto.get('formattedAddress', 'Endereço não disponível')
            
#             # Extrair informações adicionais
#             rating = posto.get('rating', 'N/A')
#             user_ratings = posto.get('userRatingCount', 0)
#             telefone = posto.get('nationalPhoneNumber', 'N/A')
#             website = posto.get('websiteUri', '#')
            
#             # Processar dados do EV (Conectores e Potência)
#             ev_info = ""
#             ev_options = posto.get('evChargeOptions', {})
#             conector_total = ev_options.get('connectorCount', 0)
#             conectores_detalhes = ev_options.get('connectorAggregation', [])
            
#             if conector_total > 0:
#                 ev_info += f"<p style='margin: 5px 0; font-size: 12px;'><b>🔌 Conectores ({conector_total}):</b><br>"
#                 for conn in conectores_detalhes:
#                     tipo = conn.get('type', 'Desconhecido').replace('EV_CONNECTOR_TYPE_', '')
#                     count = conn.get('count', 0)
#                     kw = conn.get('maxChargeRateKw', 'N/A')
#                     ev_info += f"- {count}x {tipo} (Max: {kw}kW)<br>"
#                 ev_info += "</p>"
#             else:
#                 ev_info += "<p style='margin: 5px 0; font-size: 12px; color: #d32f2f;'>Sem detalhes de conectores.</p>"

#             # Estrela de avaliação visual
#             estrelas = f"⭐ {rating} ({user_ratings} avaliações)" if rating != 'N/A' else "Sem avaliações"

#             # Construir Popup HTML aprimorado
#             popup_html = f"""
#             <div style="font-family: Arial, sans-serif; width: 280px;">
#                 <h4 style="margin: 0 0 8px 0; color: #1565c0; border-bottom: 1px solid #ccc; padding-bottom: 5px;">{nome}</h4>
#                 <p style="margin: 0 0 10px 0; font-size: 13px; font-weight: bold; color: #e65100;">
#                     {estrelas}
#                 </p>
#                 <p style="margin: 5px 0; font-size: 12px;">
#                     <b>📍 Endereço:</b><br>{endereco}
#                 </p>
#                 <p style="margin: 5px 0; font-size: 12px;">
#                     <b>📞 Contato:</b> {telefone}
#                 </p>
#                 <div style="background-color: #f1f8e9; padding: 8px; border-radius: 5px; margin: 10px 0;">
#                     {ev_info}
#                 </div>
#                 <div style="display: flex; justify-content: space-between; align-items: center;">
#                     <span style="font-size: 10px; color: #666;">{lat:.5f}, {lng:.5f}</span>
#                     <a href="{website}" target="_blank" style="font-size: 12px; color: #fff; background-color: #1565c0; padding: 4px 8px; text-decoration: none; border-radius: 4px;">Web</a>
#                 </div>
#             </div>
#             """
            
#             folium.Marker(
#                 [lat, lng],
#                 popup=folium.Popup(popup_html, max_width=300),
#                 tooltip=nome,
#                 icon=folium.Icon(color='green', icon='bolt', prefix='fa')
#             ).add_to(mapa)
            
#     return mapa










"""
Componente: Mapa interativo fullscreen con popup enriquecido
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from config.settings import DEFAULT_ZOOM

def render_mapa(lat_centro, lng_centro, raio_km, eletropostos=None, tema='claro'):
    tiles_config = {
        'claro': 'CartoDB positron',
        'escuro': 'CartoDB dark_matter'
    }
    
    mapa = folium.Map(
        location=[lat_centro, lng_centro],
        zoom_start=DEFAULT_ZOOM,
        tiles=tiles_config.get(tema, 'CartoDB positron')
    )
    
    folium.Marker(
        [lat_centro, lng_centro],
        tooltip="Ponto central da área de interesse",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)
    
    # Este círculo agora coincidirá perfeitamente com os pontos devido ao filtro Haversine
    folium.Circle(
        [lat_centro, lng_centro],
        radius=raio_km * 1000,
        color='blue',
        fill=True,
        fillOpacity=0.1,
        popup=f"Raio: {raio_km} km"
    ).add_to(mapa)
    
    if eletropostos:
        mapa = adicionar_eletropostos_ao_mapa(mapa, eletropostos)
    
    map_data = st_folium(
        mapa,
        width=None,
        height=700,
        returned_objects=["last_clicked"]
    )
    return map_data

def adicionar_eletropostos_ao_mapa(mapa, eletropostos):
    for i, posto in enumerate(eletropostos, 1):
        if 'location' in posto:
            lat = posto['location']['latitude']
            lng = posto['location']['longitude']
            nome = posto.get('displayName', {}).get('text', f'Eletroposto {i}')
            endereco = posto.get('formattedAddress', 'Endereço não disponível')
            distancia = posto.get('distancia_centro_m', 0) / 1000 # Converter a km
            
            rating = posto.get('rating', 'N/A')
            user_ratings = posto.get('userRatingCount', 0)
            telefone = posto.get('nationalPhoneNumber', 'N/A')
            website = posto.get('websiteUri', '#')
            
            ev_info = ""
            ev_options = posto.get('evChargeOptions', {})
            conector_total = ev_options.get('connectorCount', 0)
            conectores_detalhes = ev_options.get('connectorAggregation', [])
            
            if conector_total > 0:
                ev_info += f"<p style='margin: 5px 0; font-size: 12px;'><b>🔌 Conectores ({conector_total}):</b><br>"
                for conn in conectores_detalhes:
                    tipo = conn.get('type', 'Desconhecido').replace('EV_CONNECTOR_TYPE_', '')
                    count = conn.get('count', 0)
                    kw = conn.get('maxChargeRateKw', 'N/A')
                    ev_info += f"- {count}x {tipo} (Max: {kw}kW)<br>"
                ev_info += "</p>"
            else:
                ev_info += "<p style='margin: 5px 0; font-size: 12px; color: #d32f2f;'>Sem detalhes de conectores.</p>"

            estrelas = f"⭐ {rating} ({user_ratings} avaliações)" if rating != 'N/A' else "Sem avaliações"

            popup_html = f"""
            <div style="font-family: Arial, sans-serif; width: 280px;">
                <h4 style="margin: 0 0 8px 0; color: #1565c0; border-bottom: 1px solid #ccc; padding-bottom: 5px;">{nome}</h4>
                <p style="margin: 0 0 10px 0; font-size: 13px; font-weight: bold; color: #e65100;">
                    {estrelas}
                </p>
                <p style="margin: 5px 0; font-size: 12px;">
                    <b>📍 Endereço:</b><br>{endereco}
                </p>                
                <p style="margin: 5px 0; font-size: 12px;">
                    <b>📞 Contato:</b> {telefone}
                </p>
                <div style="background-color: #f1f8e9; padding: 8px; border-radius: 5px; margin: 10px 0;">
                    {ev_info}
                </div>
                <p style="margin: 5px 0; font-size: 12px; color: #d84315;">
                    <b>Distância do centro:</b> {distancia:.2f} km
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 10px; color: #666;">{lat:.5f}, {lng:.5f}</span>
                    <a href="{website}" target="_blank" style="font-size: 12px; color: #fff; background-color: #1565c0; padding: 4px 8px; text-decoration: none; border-radius: 4px;">Web</a>
                </div>
            </div>
            """
            
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=nome,
                icon=folium.Icon(color='green', icon='bolt', prefix='fa')
            ).add_to(mapa)
            
    return mapa