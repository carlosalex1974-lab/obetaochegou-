import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Apostas CornerPro", layout="wide")
st.title("📊 Oportunidades de Apostas - GeorginhoTips")

# Simulação de oportunidades com base em análise anterior
oportunidades = [
    {"Campeonato": "Copa do Brasil", "Times": "Palmeiras vs Grêmio", "Horário": "21:30", "Mercado": "Mais de 10 escanteios", "Justificativa": "Estilo ofensivo e jogo decisivo", "Confiança": "Alta"},
    {"Campeonato": "Libertadores", "Times": "Fluminense vs River Plate", "Horário": "19:00", "Mercado": "Mais de 9.5 escanteios", "Justificativa": "Alta intensidade e jogo pelas pontas", "Confiança": "Alta"},
    {"Campeonato": "Brasileirão Série A", "Times": "Atlético-MG vs Bahia", "Horário": "20:00", "Mercado": "Mais de 10.5 escanteios", "Justificativa": "Atlético-MG força jogadas laterais", "Confiança": "Média"},
    {"Campeonato": "Premier League", "Times": "Chelsea vs Brighton", "Horário": "16:00", "Mercado": "Mais de 10 escanteios", "Justificativa": "Estilo inglês com cruzamentos frequentes", "Confiança": "Alta"},
    {"Campeonato": "La Liga", "Times": "Sevilla vs Getafe", "Horário": "17:00", "Mercado": "Menos de 9 escanteios", "Justificativa": "Jogo centralizado e pouca pressão lateral", "Confiança": "Média"},
]

df_oportunidades = pd.DataFrame(oportunidades)

# Exibir alertas visuais para oportunidades com confiança alta
st.subheader("🔔 Alertas de Oportunidades com Alta Confiança")
for _, row in df_oportunidades[df_oportunidades["Confiança"] == "Alta"].iterrows():
    st.success(f"✅ {row['Times']} ({row['Campeonato']} - {row['Horário']})\n👉 {row['Mercado']} - {row['Justificativa']}")

# Exibir tabela completa
st.subheader("📋 Todas as Oportunidades do Dia")
st.dataframe(df_oportunidades, use_container_width=True)

# Gerar planilha para download
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_oportunidades.to_excel(writer, index=False, sheet_name="Oportunidades")
processed_data = output.getvalue()

hoje = datetime.today().strftime('%d-%m-%Y')
st.download_button(
    label="📥 Baixar planilha de oportunidades (.xlsx)",
    data=processed_data,
    file_name=f"oportunidades_apostas_{hoje}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)