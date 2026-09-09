import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='ConectaONG — Dashboard',
    page_icon='🤝',
    layout='wide'
)

st.title('🤝 ConectaONG')
st.subheader('Dashboard de Organizações da Sociedade Civil')
st.caption(
    'Projeto Integrador — Etapa 2 | Distribuição estimada das OSCs por estado e região'
)

st.markdown(
    'Este dashboard apresenta a distribuição estimada das Organizações da Sociedade Civil '
    '(OSCs) no Brasil e apoia a proposta do ConectaONG de conectar organizações, '
    'voluntários e doadores.'
)

arquivo_padrao = 'organizacoes_sociais_por_estado_brasil.csv'

df = pd.read_csv(arquivo_padrao, sep=';')

df.columns = df.columns.str.strip()

for col in ['Região', 'UF', 'Estado', 'Fonte dos Dados']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

col_oscs = 'Estimativa de OSCs Ativas'

if col_oscs not in df.columns:
    st.error(f"A coluna '{col_oscs}' não foi encontrada no CSV.")
    st.stop()
df[col_oscs] = pd.to_numeric(df[col_oscs], errors='coerce')
df = df.drop_duplicates().dropna(subset=[col_oscs, 'Estado', 'Região']).copy()

total_oscs = int(df[col_oscs].sum())
estado_maior = df.loc[df[col_oscs].idxmax(), 'Estado']
valor_maior = int(df[col_oscs].max())
df_regiao = df.groupby('Região', as_index=False)[col_oscs].sum().sort_values(col_oscs, ascending=False)
regiao_maior = df_regiao.iloc[0]['Região']
valor_regiao_maior = int(df_regiao.iloc[0][col_oscs])
participacao_maior = valor_regiao_maior / total_oscs * 100

st.markdown('### Indicadores principais')
k1, k2, k3 = st.columns(3)
k1.metric('Total estimado de OSCs', f'{total_oscs:,.0f}'.replace(',', '.'))
k2.metric('Estado com maior estimativa', estado_maior, f'{valor_maior:,.0f} OSCs'.replace(',', '.'))
k3.metric('Região com maior estimativa', regiao_maior, f'{valor_regiao_maior:,.0f} OSCs'.replace(',', '.'))
st.divider()

st.markdown('### 1. Estimativa de OSCs Ativas por Estado')
df_estado = df.sort_values(col_oscs, ascending=True)
fig_estado = px.bar(df_estado, x=col_oscs, y='Estado', orientation='h', text=col_oscs, title='Estimativa de OSCs Ativas por Estado', labels={col_oscs:'Estimativa de OSCs Ativas','Estado':'Estado'}, hover_data=['UF','Região'])
fig_estado.update_traces(texttemplate='%{text:,}', textposition='outside')
fig_estado.update_layout(template='plotly_white', height=750, margin=dict(l=20,r=80,t=70,b=20))
st.plotly_chart(fig_estado, use_container_width=True)
st.caption('Pergunta respondida: quais estados apresentam as maiores estimativas de OSCs ativas?')

col1, col2 = st.columns(2)
with col1:
    st.markdown('### 2. OSCs estimadas por região')
    fig_regiao = px.bar(df_regiao, x='Região', y=col_oscs, text=col_oscs, title='Estimativa de OSCs Ativas por Região', labels={'Região':'Região',col_oscs:'Estimativa de OSCs Ativas'})
    fig_regiao.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_regiao.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig_regiao, use_container_width=True)
with col2:
    st.markdown('### 3. Participação das regiões')
    fig_donut = px.pie(df_regiao, names='Região', values=col_oscs, hole=0.45, title='Participação das Regiões no Total Estimado de OSCs')
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown('### Tabela-resumo por região')
df_regiao_display = df_regiao.copy()
df_regiao_display['Participação (%)'] = (df_regiao_display[col_oscs] / total_oscs * 100).round(2)
st.dataframe(df_regiao_display, use_container_width=True, hide_index=True)

st.markdown('### Análise dos resultados')
st.write(f'Com base na base utilizada, o Brasil apresenta uma estimativa de {total_oscs:,.0f} OSCs ativas. O estado com maior estimativa é {estado_maior}, com {valor_maior:,.0f} OSCs.'.replace(',', '.'))
st.write(f'A região com maior concentração estimada é o {regiao_maior}, com {valor_regiao_maior:,.0f} OSCs, representando aproximadamente {participacao_maior:.2f}% do total.'.replace(',', '.'))
st.info('Relação com o ConectaONG: conhecer a distribuição das OSCs ajuda a compreender onde existe maior concentração de organizações e pode apoiar funcionalidades de busca e filtros por localização.')
st.warning('Limitação da base: os dados disponíveis apresentam apenas a quantidade estimada de OSCs por UF e região. Não há dados sobre voluntários, doadores, campanhas, causas ou valores de doações.')
st.markdown('### Fonte dos dados')
st.write('Ipea / Mapa das OSC (Base 2024-2026), conforme informado na base utilizada.')
