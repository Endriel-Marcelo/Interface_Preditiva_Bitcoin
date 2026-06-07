import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# 1. CARREGAR DADOS
# ==============================

dados = pd.read_csv("bitcoin_data.csv")

# ==============================
# 2. TRATAR DADOS
# ==============================

dados['Date'] = pd.to_datetime(dados['Timestamp'], unit='s')
dados['Dia'] = dados['Date'].dt.date

dados_diario = dados.groupby('Dia').agg({
    'Close': 'last'
}).reset_index()

dados_diario['Dia'] = pd.to_datetime(dados_diario['Dia'])
dados_diario = dados_diario.sort_values(by='Dia')

# ==============================
# 3. VARIAÇÃO DIÁRIA
# ==============================

# adiciona na tabela a coluna variação e calcula a variação em porcentagem
dados_diario['Variacao_%'] = dados_diario['Close'].pct_change() * 100

# remove linhas sem valores
# o primeiro dia da tabela não terá valor de variação
dados_diario = dados_diario.dropna()

# ==============================
# 4. ESCOLHA DO USUÁRIO
# ==============================

modo = input("Digite '1' para análise do passado ou '2' para previsão futura: ")

# ==============================
# 5. GRÁFICO DO PASSADO
# ==============================

if modo == '1':
    dias = int(input("Quantos dias deseja analisar? "))

    dados_periodo = dados_diario.tail(dias)

    plt.figure(figsize=(10, 5))                         # cria um espaço branco
    plt.plot(dados_periodo['Dia'], dados_periodo['Close'])  # atribui Dia como eixo X e Close como eixo Y

    plt.title('Histórico do Bitcoin')
    plt.xlabel('Data')
    plt.ylabel('Preço')

    plt.xticks(rotation=45)                             # inclina o eixo X
    plt.tight_layout()                                  # organiza o layout do gráfico

    plt.show()                                          # mostra o gráfico

# ==============================
# 6. PREVISÃO COM MÚLTIPLAS SIMULAÇÕES
# ==============================

elif modo == '2':
    dias_futuro = int(input("Quantos dias no futuro deseja prever? "))
    quantidade_previsoes = int(input("Quantas previsões deseja realizar? "))

    preco_atual = dados_diario.iloc[-1]['Close']        # pega o último preço do banco

    media = dados_diario['Variacao_%'].mean()           # calcula a média das variações
    desvio = dados_diario['Variacao_%'].std()           # calcula o desvio padrão das variações

    ultima_data = dados_diario.iloc[-1]['Dia']

    # Cria as datas futuras
    datas_futuro = [
        ultima_data + pd.Timedelta(days=i)
        for i in range(1, dias_futuro + 1)
    ]

    # Lista que vai armazenar todas as previsões
    todas_previsoes = []

    # Loop para realizar várias previsões
    for simulacao in range(quantidade_previsoes):
        preco = preco_atual
        precos_simulados = []

        for i in range(1, dias_futuro + 1):
            # cria uma variação aleatória baseada na média e no desvio histórico
            variacao = np.random.normal(media, desvio)

            # calcula o novo preço com base na variação
            preco = preco * (1 + variacao / 100)

            # guarda o preço simulado
            precos_simulados.append(preco)

        # guarda uma simulação completa
        todas_previsoes.append(precos_simulados)

    # Transforma a lista em array para facilitar os cálculos
    todas_previsoes = np.array(todas_previsoes)

    # Calcula a média das previsões em cada dia futuro
    media_previsoes = todas_previsoes.mean(axis=0)

    # Pega os preços finais de todas as simulações
    precos_finais = todas_previsoes[:, -1]

    preco_final_medio = media_previsoes[-1]
    menor_preco_final = precos_finais.min()
    maior_preco_final = precos_finais.max()

    variacao_media = ((preco_final_medio - preco_atual) / preco_atual) * 100

    # ==============================
    # PROBABILIDADE HISTÓRICA
    # ==============================

    subidas = (dados_diario['Variacao_%'] > 0).sum()    # quantos dias subiu
    quedas = (dados_diario['Variacao_%'] < 0).sum()     # quantos dias caiu
    total = len(dados_diario)

    prob_subir = (subidas / total) * 100
    prob_cair = (quedas / total) * 100

    # ==============================
    # RESULTADOS NO TERMINAL
    # ==============================

    print("\n===== PREVISÃO COM MÚLTIPLAS SIMULAÇÕES =====")
    print(f"Preço atual: {preco_atual:.2f}")
    print(f"Quantidade de previsões realizadas: {quantidade_previsoes}")
    print(f"Dias previstos: {dias_futuro}")

    print(f"\nPreço final médio estimado: {preco_final_medio:.2f}")
    print(f"Cenário pessimista: {menor_preco_final:.2f}")
    print(f"Cenário otimista: {maior_preco_final:.2f}")

    print(f"\nVariação média estimada: {variacao_media:.2f}%")

    print(f"\nProbabilidade histórica de subir: {prob_subir:.2f}%")
    print(f"Probabilidade histórica de cair: {prob_cair:.2f}%")

    # ==============================
    # GRÁFICO
    # ==============================

    plt.figure(figsize=(10, 5))

    # Plota todas as previsões individuais em cinza
    for previsao in todas_previsoes:
        plt.plot(
            datas_futuro,
            previsao,
            color='gray',
            alpha=0.15,
            linewidth=1
        )

    # Plota a média das previsões em destaque
    plt.plot(
        datas_futuro,
        media_previsoes,
        color='orange',
        linewidth=3,
        label='Média das previsões'
    )

    plt.title('Previsão do Bitcoin com Múltiplas Simulações')
    plt.xlabel('Data futura')
    plt.ylabel('Preço estimado')
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

else:
    print("Opção inválida!")