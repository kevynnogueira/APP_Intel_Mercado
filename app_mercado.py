import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import gc
#import warnings
#warnings.filterwarnings('ignore')

gc.enable()

st.set_page_config(page_title="Calculadora de mercado"
                   #, page_icon=":signal_strength:"
                   , layout="wide")

with st.container():
    st.title(" :signal_strength: Calculadora de mercado")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("Desenvolvido por [Kevyn Nogueira](https://www.linkedin.com/in/kevynnogueira/)")
    st.write("-------------------------------------------------------------------------------")

with st.expander("INFORMAÇÕES BÁSICAS"):

    titulos_infos = ['Dicionário de dados', 'Referências']
    tab1, tab2 = st.tabs(titulos_infos)

    with tab1:
        dados = ['CNPJ BASICO',
            'CNPJ ORDEM',
            'CNPJ DV',
            'IDENTIFICADOR MATRIZ/FILIAL',
            'NOME FANTASIA',
            'CNAE FISCAL PRINCIPAL',
            'TIPO DE LOGRADOURO',
            'LOGRADOURO',
            'NUMERO',
            'COMPLEMENTO',
            'BAIRRO',
            'CEP',
            'UF ou Unidade Federativa',
            'MUNICIPIO',
            'DDD 1',
            'TELEFONE 1',
            'CORREIO ELETRONICO',
            'TIPO DE EMPRESA',
            'DESCRICAO_MUNICIPIO',
            'CAPITAL SOCIAL ou Capital',
            'PORTE DA EMPRESA',
            'DESCRICAO CNAE'
        ]

        descricoes = ['NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS DÍGITOS DO CNPJ).',
        'NÚMERO DO ESTABELECIMENTO DE INSCRIÇÃO NO CNPJ (DO NONO ATÉ O DÉCIMO SEGUNDO DÍGITO DO CNPJ).',
        'DÍGITO VERIFICADOR DO NÚMERO DE INSCRIÇÃO NO CNPJ (DOIS ÚLTIMOS DÍGITOS DO CNPJ).',
        'CÓDIGO DO IDENTIFICADOR MATRIZ/FILIAL',
        'CORRESPONDE AO NOME FANTASIA',
        'CÓDIGO DA ATIVIDADE ECONÔMICA PRINCIPAL DO ESTABELECIMENTO',
        'DESCRIÇÃO DO TIPO DE LOGRADOURO',
        'NOME DO LOGRADOURO ONDE SE LOCALIZA O ESTABELECIMENTO.',
        'NÚMERO ONDE SE LOCALIZA O ESTABELECIMENTO. QUANDO NÃO HOUVER PREENCHIMENTO DO NÚMERO HAVERÁ ‘S/N’.',
        'COMPLEMENTO PARA O ENDEREÇO DE LOCALIZAÇÃO DO ESTABELECIMENTO',
        'BAIRRO ONDE SE LOCALIZA O ESTABELECIMENTO.',
        'CÓDIGO DE ENDEREÇAMENTO POSTAL REFERENTE AO LOGRADOURO NO QUAL O ESTABELECIMENTO ESTA LOCALIZADO',
        'UNIDADE DA FEDERAÇÃO EM QUE SE ENCONTRA O ESTABELECIMENTO',
        'CÓDIGO DO MUNICÍPIO DE JURISDIÇÃO ONDE SE ENCONTRA O ESTABELECIMENTO',
        'CONTÉM O DDD 1',
        'CONTÉM O NÚMERO DO TELEFONE 1',
        'CONTÉM O E-MAIL DO CONTRIBUINTE',
        'Contém o tipo de atividade da empresa. Sumariza os CNAE (Nçao é uma classificação oficial do governo)',
        'MUNICÍPIO DE JURISDIÇÃO ONDE SE ENCONTRA O ESTABELECIMENTO',
        'CAPITAL SOCIAL DA EMPRESA. Todo valor bruto disponibilizado para abrir uma empresa e mantê-la funcionando até que gere lucros',
        'Se refere ao tamanhoda empresa, podendo ser: NÃO INFORMADO; MICRO EMPRESA;  EMPRESA DE PEQUENO PORTE; DEMAIS',
        'Descricão do CNAE fiscal principal do estabelecimento'
        ]

        tab1_dict = {'DADO': dados, 'DESCRIÇÃO': descricoes}
        tab1_df = pd.DataFrame(data=tab1_dict)
        st.dataframe(tab1_df)

    with tab2:
        st.write("Dados foram obtidos através de:")
        st.write('[Dados abertos do governo](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)')
        st.write('[Dados de geolocalização do Open Adresses](https://openaddresses.io/)')


@st.cache_data
def carregar_dados():
    df = pd.read_parquet("df_completo.parquet")
    return df

df = carregar_dados()

st.sidebar.header("FILTROS:")

# Create for UF
uf=st.sidebar.multiselect("Unidade federativa:", df["UF"].sort_values().unique())
if not uf:
    df2=df.copy()
else:
    df2=df[df["UF"].isin(uf)]

# Create for DESCRICAO_MUNICIPIO
municipio=st.sidebar.multiselect("Município:", df2["DESCRICAO_MUNICIPIO"].sort_values().unique())
if not municipio:
    df3=df2.copy()
else:
    df3=df2[df2["DESCRICAO_MUNICIPIO"].isin(municipio)]

# Create for BAIRRO
bairro=st.sidebar.multiselect("Bairro:", df3["BAIRRO"].sort_values().unique())

if not bairro:
    df4 = df3.copy()
else:
    df4 = df3[df3["BAIRRO"].isin(bairro)]

# Create for PORTE DA EMPRESA
porte_empresa = st.sidebar.multiselect("Porte da empresa:", df4["PORTE DA EMPRESA"].sort_values().unique())

if not porte_empresa:
    df5 = df4.copy()
else:
    df5 = df4[df4["PORTE DA EMPRESA"].isin(porte_empresa)]


# Create for TIPO DE EMPRESA
tipo_empresa = st.sidebar.multiselect("Tipo de empresa:", df5["TIPO DE EMPRESA"].sort_values().unique())

if not tipo_empresa:
    df6 = df5.copy()
else:
    df6 = df5[df5["TIPO DE EMPRESA"].isin(porte_empresa)]

# Filtering the data

if not uf and not municipio and not bairro and not porte_empresa and not tipo_empresa: filtered_df = df6.copy()
elif uf and municipio and bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif uf and municipio and bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and municipio and bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro)]
elif uf and municipio and not bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and municipio and not bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif uf and municipio and not bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and municipio and not bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio)]
elif uf and not municipio and bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and not municipio and bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif uf and not municipio and bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['BAIRRO'].isin(bairro) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and not municipio and bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['BAIRRO'].isin(bairro)]
elif uf and not municipio and not bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and not municipio and not bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif uf and not municipio and not bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif uf and not municipio and not bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['UF'].isin(uf)]
elif not uf and municipio and bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and municipio and bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not uf and municipio and bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and municipio and bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro)]
elif not uf and municipio and not bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and municipio and not bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not uf and municipio and not bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and municipio and not bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['DESCRICAO_MUNICIPIO'].isin(municipio)]
elif not uf and not municipio and bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and not municipio and bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not uf and not municipio and bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['BAIRRO'].isin(bairro) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and not municipio and bairro and not porte_empresa and not tipo_empresa: filtered_df = df6[df6['BAIRRO'].isin(bairro)]
elif not uf and not municipio and not bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
elif not uf and not municipio and not bairro and porte_empresa and not tipo_empresa: filtered_df = df6[df6['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not uf and not municipio and not bairro and not porte_empresa and tipo_empresa: filtered_df = df6[df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
#elif uf and municipio and bairro and porte_empresa and tipo_empresa: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]
else: filtered_df = df6[df6['UF'].isin(uf) & df6['DESCRICAO_MUNICIPIO'].isin(municipio) & df6['BAIRRO'].isin(bairro) & df6['PORTE DA EMPRESA'].isin(porte_empresa) & df6['TIPO DE EMPRESA'].isin(tipo_empresa)]

filtered_df['CAPITAL SOCIAL'] = filtered_df['CAPITAL SOCIAL'].astype('float')
capital_df=filtered_df[['CNPJ BASICO', 'CAPITAL SOCIAL']].drop_duplicates()
#-----------------------------------------------------------------------------------------------
# create columns
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Quantidade total de empresas ativas",filtered_df["CNPJ BASICO"].nunique())

kpi2.metric("Quantidade total de estabelecimentos ativos",filtered_df["CNPJ BASICO"].count())


capital = f"R${capital_df['CAPITAL SOCIAL'].astype('float').sum():_.2f}"
capital = capital.replace('.', ',').replace('_', '.')
kpi3.metric("Capital social total", capital)

#-----------------------------------------------------------------------------------------------
st.subheader("Dados por porte")

titulos_guias = ['Quantidade de estabelecimentos', 'Capital social das empresas (R$)']
guia1, guia2 = st.tabs(titulos_guias)

# Adicionar conteúdo a cada guia
with guia1:
    porte_df = filtered_df.groupby(by=["PORTE DA EMPRESA"], as_index=False)["CNPJ BASICO"].count().sort_values(
        by=["CNPJ BASICO"])
    csv = porte_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv,
                       file_name="Quantidade_de_estabelecimentos_por_porte_da_empresa.csv", mime='text/csv')

    fig = px.bar(porte_df, x="PORTE DA EMPRESA", y="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with guia2:
    capital_porte_df = filtered_df[['CNPJ BASICO', "PORTE DA EMPRESA", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_porte_df = capital_porte_df.groupby(by=["PORTE DA EMPRESA"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_porte_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_porte.csv", mime='text/csv')

    fig = px.bar(capital_porte_df, x="PORTE DA EMPRESA", y="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader("Dados por atividade")

#------------------------
guia3, guia4 = st.tabs(titulos_guias)

with guia3:
    tipo_cnae_df = filtered_df.groupby(by=["TIPO DE EMPRESA"], as_index=False)["CNPJ BASICO"].count().sort_values(
        by=["CNPJ BASICO"])
    csv = tipo_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv,
                       file_name="Quantidade_de_estabelecimentos_por_atividade.csv", mime='text/csv')

    fig = px.bar(tipo_cnae_df, x="TIPO DE EMPRESA", y="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with guia4:
    capital_tipo_df = filtered_df[['CNPJ BASICO', "TIPO DE EMPRESA", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_tipo_df = capital_tipo_df.groupby(by=["TIPO DE EMPRESA"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_tipo_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_atividade.csv", mime='text/csv')

    fig = px.bar(capital_tipo_df, x="TIPO DE EMPRESA", y="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)


#------------------------
st.subheader("Dados de estabelecimentos por CNAE")
guia5, guia6 = st.tabs(titulos_guias)

with guia5:
    cnae_df=filtered_df.groupby(by=["DESCRICAO CNAE"], as_index=False)["CNPJ BASICO"].count().sort_values(by =["CNPJ BASICO"])
    csv = cnae_df.to_csv(index = False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_CNAE.csv", mime='text/csv')

    fig=px.bar(cnae_df, y="DESCRICAO CNAE", x="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with guia6:
    capital_cnae_df = filtered_df[['CNPJ BASICO', "DESCRICAO CNAE", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_cnae_df = capital_cnae_df.groupby(by=["DESCRICAO CNAE"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_CNAE.csv", mime='text/csv')

    fig = px.bar(capital_cnae_df, y="DESCRICAO CNAE", x="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

# --------------------------------------

with st.expander("ANÁLISE REGIONAL"):
    if not uf and not municipio and not bairro:
        st.write("Selecione alguma localização nos filtros para visualizar")
    else:
        st.subheader("Dados por municipío")
        guia7, guia8 = st.tabs(titulos_guias)

        with guia7:
            municipio_cnpj_df=filtered_df[['DESCRICAO_MUNICIPIO','CNPJ BASICO']].groupby(['DESCRICAO_MUNICIPIO']).count().reset_index().sort_values(by = 'CNPJ BASICO',ascending=False).reset_index(drop  = True)
            csv = municipio_cnpj_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_municipio.csv", mime='text/csv')

            fig=px.bar(municipio_cnpj_df, x="DESCRICAO_MUNICIPIO", y="CNPJ BASICO", text_auto=True, template="seaborn")
            st.plotly_chart(fig,use_container_width=True, height=200)

        with guia8:
            capital_municipio_df = filtered_df[['CNPJ BASICO', "DESCRICAO_MUNICIPIO", 'CAPITAL SOCIAL']].drop_duplicates()
            capital_municipio_df = capital_municipio_df.groupby(by=["DESCRICAO_MUNICIPIO"], as_index=False)[
                "CAPITAL SOCIAL"].sum().sort_values(by=["CAPITAL SOCIAL"])

            csv = capital_municipio_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de capital', data=csv,
                               file_name="Capital_de_empresas_por_municipio.csv", mime='text/csv')

            fig = px.bar(capital_municipio_df, x="DESCRICAO_MUNICIPIO", y="CAPITAL SOCIAL", text_auto=True, template="seaborn").update_layout(
                xaxis={
                    "range": [capital_municipio_df["CAPITAL SOCIAL"].quantile(1), df["CAPITAL SOCIAL"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig,use_container_width=True, height=200)

        st.subheader("Dados por bairro")
        guia9, guia10 = st.tabs(titulos_guias)

        with guia9:
            bairro_cnpj_df=filtered_df[['BAIRRO','CNPJ BASICO']].groupby(['BAIRRO']).count().reset_index().sort_values(by = 'CNPJ BASICO',ascending=False).reset_index(drop  = True)
            csv = bairro_cnpj_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados', data=csv, file_name="Quantidade_de_estabelecimentos_por_bairro.csv", mime='text/csv')


            fig=px.bar(bairro_cnpj_df, x="BAIRRO", y="CNPJ BASICO", text_auto=True, template="seaborn").update_layout(
                xaxis={
                    "range": [bairro_cnpj_df["CNPJ BASICO"].quantile(1), df["CNPJ BASICO"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig,use_container_width=True, height=200)

        with guia10:
            capital_bairro_df = filtered_df[['CNPJ BASICO', "BAIRRO", 'CAPITAL SOCIAL']].drop_duplicates()
            capital_bairro_df = capital_bairro_df.groupby(by=["BAIRRO"], as_index=False)[
                "CAPITAL SOCIAL"].sum().sort_values(by=["CAPITAL SOCIAL"])

            csv = capital_bairro_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de capital', data=csv,
                               file_name="Capital_de_empresas_por_bairro.csv", mime='text/csv')

            fig = px.bar(capital_bairro_df, x="BAIRRO", y="CAPITAL SOCIAL", text_auto=True,
                         template="seaborn").update_layout(
                xaxis={
                    "range": [capital_bairro_df["CAPITAL SOCIAL"].quantile(1), df["CAPITAL SOCIAL"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig, use_container_width=True, height=200)

gc.collect()
