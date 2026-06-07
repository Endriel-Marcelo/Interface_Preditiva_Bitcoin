import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="BTC Analyzer",
    page_icon="₿",
    layout="wide"
)

# ==============================
# CSS PERSONALIZADO
# ==============================

st.markdown("""
<style>
    .titulo-principal {
        font-size: 48px;
        font-weight: 800;
        color: #F7931A;
        text-align: center;
        margin-bottom: 0px;
    }

    .subtitulo {
        font-size: 20px;
        color: #C9D1D9;
        text-align: center;
        margin-bottom: 35px;
    }

    .info-box {
        background-color: #161B22;
        border-left: 5px solid #F7931A;
        padding: 18px;
        border-radius: 12px;
        color: #C9D1D9;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        color: #FAFAFA;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #F7931A, #FFB347);
        color: #0E1117;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 16px;
        transition: 0.3s;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #FFB347, #F7931A);
        color: #0E1117;
        transform: scale(1.02);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #161B22;
        border-radius: 14px;
        padding: 14px 28px;
        color: #C9D1D9;
        font-weight: 700;
        border: 1px solid #30363D;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #F7931A, #FFB347);
        color: #0E1117;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #161B22, #1F2937);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #30363D;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
    }

    .custom-card {
        background: linear-gradient(135deg, #161B22, #1F2937);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #30363D;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
        min-height: 92px;
    }

    .custom-card-label {
        color: #FAFAFA;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .custom-card-value {
        font-size: 32px;
        font-weight: 700;
    }

    .footer {
        margin-top: 40px;
        text-align: center;
        color: #8B949E;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# CARREGAR E TRATAR DADOS
# ==============================

@st.cache_data
def carregar_dados():
    dados = pd.read_csv("bitcoin_data.csv")

    dados["Date"] = pd.to_datetime(dados["Timestamp"], unit="s")
    dados["Dia"] = dados["Date"].dt.date

    dados_diario = dados.groupby("Dia").agg({
        "Close": "last"
    }).reset_index()

    dados_diario["Dia"] = pd.to_datetime(dados_diario["Dia"])
    dados_diario = dados_diario.sort_values(by="Dia")

    dados_diario["Variacao_%"] = dados_diario["Close"].pct_change() * 100
    dados_diario = dados_diario.dropna()

    return dados_diario


try:
    dados_diario = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo bitcoin_data.csv não encontrado. Coloque o arquivo na mesma pasta do app.py.")
    st.stop()
except Exception as erro:
    st.error(f"Ocorreu um erro ao carregar os dados: {erro}")
    st.stop()

# ==============================
# FUNÇÃO PARA ESTILIZAR GRÁFICO
# ==============================

def configurar_grafico(fig, ax):
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#161B22")

    ax.tick_params(colors="#C9D1D9")
    ax.xaxis.label.set_color("#C9D1D9")
    ax.yaxis.label.set_color("#C9D1D9")
    ax.title.set_color("#FAFAFA")

    ax.grid(True, color="#30363D", linestyle="--", linewidth=0.7)

    for spine in ax.spines.values():
        spine.set_color("#30363D")


# ==============================
# CABEÇALHO
# ==============================

st.markdown('<h1 class="titulo-principal">₿ BTC Analyzer</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Dashboard de análise histórica e simulação futura do Bitcoin</p>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-box">
    Este sistema analisa o preço passado do Bitcoin e gera simulações futuras com base na média
    e no desvio padrão das variações históricas. A simulação não representa garantia de preço futuro.
</div>
""", unsafe_allow_html=True)

preco_atual = dados_diario.iloc[-1]["Close"]
ultima_data = dados_diario.iloc[-1]["Dia"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Preço mais recente", f"US$ {preco_atual:,.2f}")

with col2:
    st.metric("Última data registrada", ultima_data.strftime("%d/%m/%Y"))

with col3:
    st.metric("Dias no banco de dados", len(dados_diario))

# ==============================
# ABAS PRINCIPAIS
# ==============================

aba_passado, aba_futuro = st.tabs(["Análise do Passado", "Previsão Futura"])

# ==============================
# ABA 1 - ANÁLISE DO PASSADO
# ==============================

with aba_passado:
    st.markdown('<div class="section-title">Análise do Passado</div>', unsafe_allow_html=True)

    st.write("Escolha quantos dias do histórico do Bitcoin deseja analisar.")

    dias = st.number_input(
        "Quantidade de dias para análise:",
        min_value=1,
        max_value=len(dados_diario),
        value=30,
        step=1
    )

    executar_passado = st.button("Analisar histórico do Bitcoin")

    if executar_passado:
        dados_periodo = dados_diario.tail(dias)

        preco_inicial = dados_periodo.iloc[0]["Close"]
        preco_final = dados_periodo.iloc[-1]["Close"]
        variacao_periodo = ((preco_final - preco_inicial) / preco_inicial) * 100

        maior_preco = dados_periodo["Close"].max()
        menor_preco = dados_periodo["Close"].min()
        media_preco = dados_periodo["Close"].mean()

        st.markdown(f"### Resultado dos últimos {dias} dias")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Preço inicial", f"US$ {preco_inicial:,.2f}")

        with col2:
            st.metric("Preço final", f"US$ {preco_final:,.2f}")

        with col3:
            st.metric("Variação no período", f"{variacao_periodo:.2f}%")

        with st.expander("Mais detalhes"):
            col4, col5, col6 = st.columns(3)

            with col4:
                st.metric("Maior preço", f"US$ {maior_preco:,.2f}")

            with col5:
                st.metric("Menor preço", f"US$ {menor_preco:,.2f}")

            with col6:
                st.metric("Preço médio", f"US$ {media_preco:,.2f}")

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.plot(
            dados_periodo["Dia"],
            dados_periodo["Close"],
            color="#F7931A",
            linewidth=2.5
        )

        ax.fill_between(
            dados_periodo["Dia"],
            dados_periodo["Close"],
            color="#F7931A",
            alpha=0.15
        )

        ax.set_title("Histórico do Preço do Bitcoin")
        ax.set_xlabel("Data")
        ax.set_ylabel("Preço em dólar")

        configurar_grafico(fig, ax)

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        with st.expander("Ver tabela dos dados analisados"):
            st.dataframe(dados_periodo, use_container_width=True)

# ==============================
# ABA 2 - PREVISÃO FUTURA
# ==============================

with aba_futuro:
    st.markdown('<div class="section-title">Previsão Futura</div>', unsafe_allow_html=True)

    st.write("Escolha quantos dias no futuro deseja prever e quantas simulações deseja realizar.")

    col_input1, col_input2 = st.columns(2)

    with col_input1:
        dias_futuro = st.number_input(
            "Quantidade de dias para previsão:",
            min_value=1,
            max_value=3650,
            value=30,
            step=1
        )

    with col_input2:
        quantidade_previsoes = st.number_input(
            "Quantidade de previsões:",
            min_value=1,
            max_value=1000,
            value=100,
            step=1
        )

    executar_futuro = st.button("Gerar previsões futuras")

    if executar_futuro:
        media = dados_diario["Variacao_%"].mean()
        desvio = dados_diario["Variacao_%"].std()

        datas_futuro = [
            ultima_data + pd.Timedelta(days=i)
            for i in range(1, dias_futuro + 1)
        ]

        todas_previsoes = []

        for simulacao in range(quantidade_previsoes):
            preco = preco_atual
            precos_simulados = []

            for i in range(1, dias_futuro + 1):
                variacao = np.random.normal(media, desvio)
                preco = preco * (1 + variacao / 100)
                precos_simulados.append(preco)

            todas_previsoes.append(precos_simulados)

        todas_previsoes = np.array(todas_previsoes)

        media_previsoes = todas_previsoes.mean(axis=0)
        preco_final_medio = media_previsoes[-1]

        precos_finais = todas_previsoes[:, -1]

        menor_preco_final = precos_finais.min()
        maior_preco_final = precos_finais.max()

        variacao_media = ((preco_final_medio - preco_atual) / preco_atual) * 100

        subidas = (dados_diario["Variacao_%"] > 0).sum()
        quedas = (dados_diario["Variacao_%"] < 0).sum()
        total = len(dados_diario)

        prob_subir = (subidas / total) * 100
        prob_cair = (quedas / total) * 100

        previsoes_acima_preco_atual = (precos_finais > preco_atual).sum()
        previsoes_abaixo_preco_atual = (precos_finais < preco_atual).sum()

        prob_simulada_subir = (previsoes_acima_preco_atual / quantidade_previsoes) * 100
        prob_simulada_cair = (previsoes_abaixo_preco_atual / quantidade_previsoes) * 100

        st.markdown(
            f"### Resultado de {quantidade_previsoes} previsões para os próximos {dias_futuro} dias"
        )

        # ==============================
        # CORES DOS RESULTADOS
        # ==============================

        if variacao_media >= 0:
            cor_resultado = "#3FB950"  # verde
            sinal_variacao = "+"
        else:
            cor_resultado = "#F85149"  # vermelho
            sinal_variacao = ""

        # ==============================
        # RESULTADOS PRINCIPAIS
        # ==============================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Preço atual", f"US$ {preco_atual:,.2f}")

        with col2:
            st.markdown(f"""
            <div class="custom-card">
                <div class="custom-card-label">Preço final médio</div>
                <div class="custom-card-value" style="color: {cor_resultado};">
                    US$ {preco_final_medio:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="custom-card">
                <div class="custom-card-label">Variação média estimada</div>
                <div class="custom-card-value" style="color: {cor_resultado};">
                    {sinal_variacao}{variacao_media:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ==============================
        # MAIS DETALHES
        # ==============================

        with st.expander("Mais detalhes"):
            col4, col5 = st.columns(2)

            with col4:
                st.metric("Cenário pessimista", f"US$ {menor_preco_final:,.2f}")

            with col5:
                st.metric("Cenário otimista", f"US$ {maior_preco_final:,.2f}")

            col6, col7 = st.columns(2)

            with col6:
                st.metric("Chance simulada de terminar acima", f"{prob_simulada_subir:.2f}%")

            with col7:
                st.metric("Chance simulada de terminar abaixo", f"{prob_simulada_cair:.2f}%")

            col8, col9 = st.columns(2)

            with col8:
                st.metric("Probabilidade histórica de subir em um dia", f"{prob_subir:.2f}%")

            with col9:
                st.metric("Probabilidade histórica de cair em um dia", f"{prob_cair:.2f}%")

        # ==============================
        # GRÁFICO DAS PREVISÕES
        # ==============================

        fig, ax = plt.subplots(figsize=(12, 5))

        for previsao in todas_previsoes:
            ax.plot(
                datas_futuro,
                previsao,
                color="#8B949E",
                alpha=0.12,
                linewidth=1
            )

        ax.plot(
            datas_futuro,
            media_previsoes,
            color="#F7931A",
            linewidth=3,
            label="Média das previsões"
        )

        ax.axhline(
            y=preco_atual,
            color="#58A6FF",
            linestyle="--",
            linewidth=1.5,
            label="Preço atual"
        )

        ax.set_title("Múltiplas Simulações Futuras do Bitcoin")
        ax.set_xlabel("Data futura")
        ax.set_ylabel("Preço estimado em dólar")
        ax.legend()

        configurar_grafico(fig, ax)

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # ==============================
        # TABELAS
        # ==============================

        dados_media_futuro = pd.DataFrame({
            "Data": datas_futuro,
            "Preço médio estimado": media_previsoes
        })

        dados_resultado_final = pd.DataFrame({
            "Simulação": range(1, quantidade_previsoes + 1),
            "Preço final": precos_finais
        })

        with st.expander("Ver tabela com a média das previsões por dia"):
            st.dataframe(dados_media_futuro, use_container_width=True)

        with st.expander("Ver preço final de cada previsão"):
            st.dataframe(dados_resultado_final, use_container_width=True)

# ==============================
# RODAPÉ
# ==============================

st.markdown("""
<div class="footer">
    Desenvolvido em Python com Streamlit, Pandas, NumPy e Matplotlib.
</div>
""", unsafe_allow_html=True)