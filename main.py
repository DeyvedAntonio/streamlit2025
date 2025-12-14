import pandas as pd
import streamlit as st


st.set_page_config('Minhas finanças', page_icon='💰')

st.markdown(
    """
# Boas vindas!

## Nosso app financeiro

Espero que você curta.
"""
)

file_upload = st.file_uploader(
    label='Faça upload dos dados aqui', type=['csv']
)

if file_upload:
    df = pd.read_csv(file_upload, sep=';')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

    exp1 = st.expander('Dados Brutos')
    columns_fmt = {
        'Valor': st.column_config.NumberColumn('Valor', format='R$ %f')
    }
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    exp2 = st.expander('Instituições')
    df_instituicao = df.pivot_table(
        index='Data', columns='Instituição', values='Valor'
    )

    tab_data, tab_history, tab_share = exp2.tabs(
        ['Dados', 'Histórico', 'Distribuição',]
    )
    with tab_data:
        st.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)

    with tab_share:
        date = st.selectbox('Filtro Data', options=df_instituicao.index)
        last_dt = df_instituicao.loc[date]
        st.bar_chart(last_dt)

    df_data = df.groupby(by='Data')[['Valor']].sum()
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['Diferença Mensal'] = df_data['Valor'] - df_data['lag_1']
    df_data['Média 6M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(6).mean()
    df_data['Média 12M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(12).mean()
    df_data['Média 24M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(24).mean()

    st.dataframe(df_data)
