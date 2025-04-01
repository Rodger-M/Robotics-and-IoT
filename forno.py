import streamlit as st
import numpy as np
import time
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa os históricos na sessão, se necessário
if "historico" not in st.session_state:
    st.session_state.historico = []
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "ultima_temp" not in st.session_state:  
    st.session_state.ultima_temp = 200  # Começa com 200°C para evitar picos bruscos

# Função para gerar dados simulados com oscilações mais suaves
def gerar_dado():
    variacao = np.random.uniform(-10, 10)  # Pequena variação de temperatura
    temperatura = max(100, min(350, st.session_state.ultima_temp + variacao))  # Mantém dentro do intervalo
    st.session_state.ultima_temp = temperatura  # Atualiza para a próxima iteração

    status = "Aquecendo" if temperatura < 200 else "Estável"
    
    # Se a temperatura passar de 300°C, gera um alerta
    if temperatura > 300:
        st.session_state.alertas.append({"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura})

    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Layout em colunas
col1, col2 = st.columns([1, 2])  # Coluna 1 menor (Status + Alertas), Coluna 2 maior (Histórico)

# ---- STATUS ----
with col1:
    st.subheader("📊 Status Atual")
    status_metric = st.empty()  

    # ---- ALERTAS ----
    st.subheader("⚠️ Alertas de Temperatura (>300°C)")
    alertas_display = st.empty()

# ---- HISTÓRICO ----
with col2:
    st.subheader("📋 Histórico de Dados")
    historico_display = st.empty()  

# ---- GRÁFICO ----
st.subheader("📈 Evolução da Temperatura")
grafico_display = st.empty()

# Loop para gerar e atualizar os dados
for _ in range(100):  # Pode ser ajustado
    novo_dado = gerar_dado()

    # Adiciona ao histórico
    st.session_state.historico.append(novo_dado)

    # Limita o histórico a 20 registros
    if len(st.session_state.historico) > 20:
        st.session_state.historico.pop(0)

    # Converte o histórico para DataFrame
    df = pd.DataFrame(st.session_state.historico)

    # Atualiza o status
    status_metric.subheader(f"Temperatura: {novo_dado['temperature']:.2f} °C")
    status_metric.subheader(f"Status: {novo_dado['status']}")

    # Atualiza a tabela de histórico
    historico_display.dataframe(df[::-1])

    # Atualiza o gráfico
    if len(df) > 1:
        grafico_display.line_chart(df.set_index("timestamp")["temperature"])

    # Atualiza a tabela de alertas
    if len(st.session_state.alertas) > 0:
        df_alertas = pd.DataFrame(st.session_state.alertas)
        alertas_display.dataframe(df_alertas[::-1])
    else:
        alertas_display.text("Nenhum alerta registrado.")

    # Pausa para atualização
    time.sleep(1)
