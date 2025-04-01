import streamlit as st
import pandas as pd
import numpy as np
import time
from PIL import Image, ImageDraw

# Configuração da página
st.set_page_config(page_title="Monitoramento de Forno", layout="wide")

# Inicializa os dados na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "alertas" not in st.session_state:
    st.session_state.alertas = []
if "temperatura_atual" not in st.session_state:
    st.session_state.temperatura_atual = 250  # Começa com um valor mais realista

# Função para gerar dados simulados com variação suave
def gerar_dado():
    variacao = np.random.uniform(-5, 5)  # Pequenas variações
    nova_temperatura = st.session_state.temperatura_atual + variacao

    # Simula picos acima de 300°C de vez em quando
    if np.random.rand() < 0.05:  # 5% de chance de um pico
        nova_temperatura += np.random.uniform(20, 40)

    # Mantém a temperatura dentro de limites razoáveis
    nova_temperatura = max(150, min(nova_temperatura, 350))

    status = "Aquecendo" if nova_temperatura < 200 else "Estável"
    
    st.session_state.temperatura_atual = nova_temperatura  # Atualiza o valor global
    
    return {"timestamp": time.strftime("%H:%M:%S"), "temperature": nova_temperatura, "status": status}

# Atualiza os dados continuamente
novo_dado = gerar_dado()
st.session_state.historico.append(novo_dado)

# Mantém o histórico com no máximo 20 registros
if len(st.session_state.historico) > 20:
    st.session_state.historico.pop(0)

# Verifica alertas e armazena se necessário
if novo_dado["temperature"] > 300:
    st.session_state.alertas.append(novo_dado)

    # Mantém no máximo 5 alertas recentes
    if len(st.session_state.alertas) > 5:
        st.session_state.alertas.pop(0)

# Converte os dados para DataFrame
df = pd.DataFrame(st.session_state.historico)
df_alertas = pd.DataFrame(st.session_state.alertas)

# Função para gerar cor baseada na temperatura
def definir_cor(temperatura):
    if temperatura <= 150:
        return (0, 0, 255)  # Azul
    elif temperatura <= 250:
        return (0, 255, 0)  # Verde
    elif temperatura <= 300:
        return (255, 165, 0)  # Laranja
    else:
        return (255, 0, 0)  # Vermelho

# Função para adicionar um gradiente baseado na temperatura
def adicionar_gradiente(imagem, x, y, temperatura, raio=40):
    tamanho = (raio * 2, raio * 2)
    gradiente = Image.new("RGBA", tamanho, (0, 0, 0, 0))

    draw = ImageDraw.Draw(gradiente)
    cor = definir_cor(temperatura)

    for i in range(raio, 0, -1):
        alpha = int(255 * (1 - i / raio))
        draw.ellipse((raio - i, raio - i, raio + i, raio + i), fill=cor + (alpha,))

    imagem.paste(gradiente, (x - raio, y - raio), gradiente)
    return imagem

# Carrega a planta e adiciona o forno na posição correta com a cor dinâmica
img_path = "planta_do_forno.png"  # Ajuste o caminho conforme necessário
forno_x, forno_y = 600, 300  # Posição do forno
img = Image.open(img_path)
img_com_gradiente = adicionar_gradiente(img.copy(), forno_x, forno_y, novo_dado["temperature"])

# Layout do dashboard
col1, col2 = st.columns([2, 1])  # Divide a tela 2/3 e 1/3

with col1:
    st.subheader("🌡️ Monitoramento do Forno")

    # Status atualizado
    st.metric(label="Temperatura Atual", value=f"{novo_dado['temperature']:.2f} °C")
    st.metric(label="Status", value=novo_dado["status"])

    # Exibe a imagem com o forno na cor correta
    st.image(img_com_gradiente, caption="Planta do Forno", use_column_width=True)

with col2:
    st.subheader("📋 Histórico de Dados")
    st.dataframe(df[::-1])  # Mostra os últimos registros primeiro

    if not df_alertas.empty:
        st.subheader("⚠️ Alertas de Temperatura")
        st.dataframe(df_alertas[::-1])

# Gráfico de temperatura
st.subheader("📈 Evolução da Temperatura")
st.line_chart(df.set_index("timestamp")["temperature"])

# Pausa para atualização
time.sleep(1)
st.experimental_rerun()
