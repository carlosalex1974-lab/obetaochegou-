import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Validador de Estratégia Esportiva", layout="centered")

st.title("📊 Validador de Estratégia Esportiva Georginho Tips")
st.write("Faça upload de uma planilha Excel com colunas `ganhos` e `perdas` para validar sua estratégia.")

uploaded_file = st.file_uploader("📁 Envie sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        if 'ganhos' in df.columns and 'perdas' in df.columns:
            ganhos = df['ganhos'].dropna().count()
            perdas = df['perdas'].dropna().count()

            lucro_total = ganhos * 70 - perdas * 100
            unidades_ganhas = lucro_total / 100

            st.success("✅ Análise concluída com sucesso!")
            st.metric("Total de Ganhos", ganhos)
            st.metric("Total de Perdas", perdas)
            st.metric("Lucro Total (R$)", f"{lucro_total}")
            st.metric("Unidades Ganhas", f"{unidades_ganhas:.2f}")

            # Criar lista de resultados
            resultados = []
            for i in range(len(df)):
                if pd.notna(df.at[i, 'ganhos']):
                    resultados.append(70)
                elif pd.notna(df.at[i, 'perdas']):
                    resultados.append(-100)

            # Gráfico 1: Lucro acumulado
            lucro_acumulado = pd.Series(resultados).cumsum()
            st.subheader("📈 Evolução Acumulada do Lucro")
            st.line_chart(lucro_acumulado)

            # Gráfico 2: Distribuição de ganhos e perdas
            st.subheader("🥧 Distribuição de Ganhos e Perdas")
            fig1, ax1 = plt.subplots()
            ax1.pie([ganhos, perdas], labels=["Ganhos", "Perdas"], autopct='%1.1f%%', colors=['green', 'red'], startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # Gráfico 3: Unidades por bloco de 50 apostas
            st.subheader("📊 Unidades Ganhas por Bloco de 50 Apostas")
            unidades_por_bloco = []
            for i in range(0, len(resultados), 50):
                bloco = resultados[i:i+50]
                unidades_bloco = sum(bloco) / 100
                unidades_por_bloco.append(unidades_bloco)

            st.bar_chart(unidades_por_bloco)

        else:
            st.error("❌ A planilha deve conter as colunas 'ganhos' e 'perdas'.")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
