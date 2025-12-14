import pandas as pd
import streamlit as st


def calc_general_stats(df: pd.DataFrame):
    df_data = df.groupby(by='Data')[['Valor']].sum()
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['Diferença Mensal'] = df_data['Valor'] - df_data['lag_1']
    df_data['Diferença Mensal Rel.'] = df_data['Valor'] / df_data['lag_1'] - 1
    df_data['Média 6M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(6).mean()  # NOQA: E501
    df_data['Média 12M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(12).mean()  # NOQA: E501
    df_data['Média 24M Diferença Mensal'] = df_data['Diferença Mensal'].rolling(24).mean()  # NOQA: E501

    df_data = df_data.drop('lag_1', axis=1)

    return df_data


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

    exp3 = st.expander('Estatísticas Gerais')

    df_stats = calc_general_stats(df)

    columns_config = {
        'Valor': st.column_config.NumberColumn('Valor', format='R$ %.2f'),
        'Diferença Mensal': st.column_config.NumberColumn('Diferença Mensal', format='R$ %.2f'),  # NOQA: E501
        'Média 6M Diferença Mensal': st.column_config.NumberColumn('Média 6M Diferença Mensal', format='R$ %.2f'),  # NOQA: E501
        'Média 12M Diferença Mensal': st.column_config.NumberColumn('Média 12M Diferença Mensal', format='R$ %.2f'),  # NOQA: E501
        'Média 24M Diferença Mensal': st.column_config.NumberColumn('Média 24M Diferença Mensal', format='R$ %.2f'),  # NOQA: E501
        'Diferença Mensal Rel.': st.column_config.NumberColumn('Diferença Mensal Rel.', format='percent'),  # NOQA: E501
    }

    exp3.dataframe(df_stats, column_config=columns_config)
