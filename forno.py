import streamlit as st
import numpy as np
import time
import pandas as pd
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa os históricos na sessão, se necessário
if "historico" not in st.session_state:
    st.session_state.historico = []
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "ultima_temp" not in st.session_state:
    st.session_state.ultima_temp = 150  # Inicia em 150°C para simular o aquecimento

# Função para gerar dados simulados com aquecimento progressivo
def gerar_dado():
    temperatura = st.session_state.ultima_temp

    # Se estiver abaixo de 250°C, sobe gradualmente
    if temperatura < 250:
        temperatura += np.random.uniform(2, 5)
    else:
        # Após estabilizar, pequenas variações normais (+-3°C)
        temperatura += np.random.uniform(-3, 3)

        # Para gerar um pico eventual, o aumento acontece progressivamente
        if np.random.rand() < 0.03:  # 3% de chance de começar um aumento
            temperatura += np.random.uniform(5, 10)  # Pequenos aumentos até passar de 300°C

    # Garante que a temperatura não passe de 350°C
    temperatura = min(temperatura, 350)

    # Atualiza o estado da última temperatura
    st.session_state.ultima_temp = temperatura

    status = "Aquecendo" if temperatura < 200 else "Estável"

    # Se a temperatura passar de 300°C, gera um alerta
    if temperatura > 300:
        st.session_state.alertas.append({"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura})

    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": temperatura, "status": status}

# Função para gerar a imagem com o gradiente
def gerar_imagem(temperatura):
    img_path = "planta_do_forno.png"  # Caminho da imagem da planta
    img = Image.open(img_path).convert("RGBA")
    
    # Redimensiona a imagem para 525x525
    img = img.resize((525, 525))
    
    # Geração do gradiente para a indicação da temperatura
    gradient = np.zeros((525, 525, 4), dtype=np.uint8)
    
    # A cor do gradiente será dependente da temperatura
    r, g, b = 0, 0, 255  # Inicializa com azul
    
    if temperatura > 250:
        r = min(255, (temperatura - 250) * 2)  # Intensifica o vermelho à medida que a temperatura sobe
        g = max(0, 255 - r)  # Diminui o verde
    if temperatura > 300:
        r = 255  # Alcança o vermelho total acima de 300°C
        g = 0
    
    gradient[:, :, 0] = r  # Red
    gradient[:, :, 1] = g  # Green
    gradient[:, :, 2] = b  # Blue
    gradient[:, :, 3] = 128  # Transparência parcial para não cobrir completamente
    
    # Cria uma imagem PIL a partir do array de gradiente
    gradient_img = Image.fromarray(gradient)
    
    # Aplica o gradiente à imagem da planta
    img = Image.alpha_composite(img, gradient_img)
    
    return img

# Layout em colunas
col1, col2 = st.columns([1, 2])  # Coluna 1 menor (Status + Alertas), Coluna 2 maior (Planta + Gráfico)

# ---- STATUS ----
with col1:
    st.subheader("📊 Status Atual")
    status_metric = st.empty()

    # ---- ALERTAS ----
    st.subheader("⚠️ Alertas de Temperatura (>300°C)")
    alertas_display = st.empty()

# ---- PLANTA COM GRADIENTE ----
with col2:
    st.subheader("🌍 Planta do Forno com Temperatura")
    # Exibe a planta com o gradiente de temperatura
    planta_display = st.empty()

# ---- GRÁFICO ----
st.subheader("📈 Evolução da Temperatura")
grafico_display = st.empty()

# Loop infinito para gerar e atualizar os dados
while True:
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

    # Atualiza a planta com o gradiente
    img_atualizada = gerar_imagem(novo_dado["temperature"])
    planta_display.image(img_atualizada, use_column_width=False)

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
