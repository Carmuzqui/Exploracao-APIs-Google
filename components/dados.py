"""
Componente: Visualización de datos con TODA información
"""

import streamlit as st
import pandas as pd

def render_dados_eletropostos(eletropostos):
    """Renderiza tabela de eletropostos"""
    
    if not eletropostos:
        st.warning("Nenhum eletroposto encontrado na área.")
        return
    
    # Processar dados mais ricos para a tabela
    dados = []
    for posto in eletropostos:
        ev_options = posto.get('evChargeOptions', {})
        total_conectores = ev_options.get('connectorCount', 0)
        
        max_kw = 0
        for conn in ev_options.get('connectorAggregation', []):
            kw = conn.get('maxChargeRateKw', 0)
            if kw > max_kw:
                max_kw = kw
                
        # Converter distância de metros para km
        distancia_km = posto.get('distancia_centro_m', 0) / 1000
                
        dados.append({
            'Nome': posto.get('displayName', {}).get('text', 'N/A'),
            'Distância (km)': round(distancia_km, 2),
            'Endereço': posto.get('formattedAddress', 'N/A'),
            'Conectores': total_conectores,
            'Potência Máx (kW)': max_kw if max_kw > 0 else 'N/A',
            'Avaliação': posto.get('rating', 'N/A'),
            'Latitude': posto.get('location', {}).get('latitude', 'N/A'),
            'Longitude': posto.get('location', {}).get('longitude', 'N/A')
        })
    
    # Criar DataFrame e ordenar pela distância (do mais próximo ao mais distante)
    df = pd.DataFrame(dados)
    if 'Distância (km)' in df.columns:
        df = df.sort_values('Distância (km)')
    
    # Métricas atualizadas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Postos", len(df))
    with col2:
        st.metric("Total de Conectores", df[df['Conectores'] != 'N/A']['Conectores'].sum())
    with col3:
        postos_rapidos = len(df[pd.to_numeric(df['Potência Máx (kW)'], errors='coerce') >= 50])
        st.metric("Postos Rápidos (≥50kW)", postos_rapidos)
    
    st.divider()
    
    # Tabela
    st.dataframe(
        df,
        width='stretch',
        hide_index=True
    )
    
    # Botão de download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV Completo",
        data=csv,
        file_name="eletropostos_detalhados.csv",
        mime="text/csv"
    )