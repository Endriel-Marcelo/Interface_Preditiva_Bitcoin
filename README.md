# BTC Analyzer

BTC Analyzer é um dashboard desenvolvido em Python para análise histórica e simulação futura do preço do Bitcoin.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Funcionalidades

- Análise do preço passado do Bitcoin
- Simulação futura com múltiplas previsões
- Gráficos interativos
- Interface em tema escuro
- Exibição de cenários otimista e pessimista

## Como executar o projeto

Instale as dependências:

```bash
pip install -r requirements.txt

## Banco de dados

O banco de dados utilizado neste projeto foi obtido no Kaggle, no dataset **Bitcoin Historical Data**.

Por conta do tamanho do arquivo original, o arquivo `bitcoin_data.csv` não foi incluído diretamente neste repositório.

Para executar o projeto, baixe o dataset no Kaggle, renomeie o arquivo para:

```text
bitcoin_data.csv ```
Coloque o arquivo bitcoin_data.csv na mesma pasta do app.py.
Execute o projeto pelo terminal/CMD:
streamlit run app.py
