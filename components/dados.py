"""
Componente: Visualização de dados tabulados
"""

import streamlit as st
import pandas as pd


def render_dados_eletropostos(eletropostos):
    """Renderiza tabela de eletropostos"""
    
    if not eletropostos:
        st.warning("Nenhum eletroposto encontrado")
        return
    
    # Processar dados para tabela
    dados = []
    for posto in eletropostos:
        dados.append({
            'Nome': posto.get('displayName', {}).get('text', 'N/A'),
            'Endereço': posto.get('formattedAddress', 'N/A'),
            'Latitude': posto.get('location', {}).get('latitude', 'N/A'),
            'Longitude': posto.get('location', {}).get('longitude', 'N/A')
        })
    
    # Criar DataFrame
    df = pd.DataFrame(dados)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", len(df))
    with col2:
        st.metric("Com endereço", df['Endereço'].notna().sum())
    with col3:
        st.metric("Com coordenadas", df['Latitude'].notna().sum())
    
    st.divider()
    
    # Tabela
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Botão de download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="eletropostos.csv",
        mime="text/csv"
    )