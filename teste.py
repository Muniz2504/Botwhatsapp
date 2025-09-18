import webbrowser
import pyautogui
import pandas as pd
import time
import urllib.parse
import random

# Configurar pyautogui para ser mais rápido
pyautogui.PAUSE = 0.3

# Abrir WhatsApp Web no navegador padrão
webbrowser.open("https://web.whatsapp.com")
print("Escaneie o QR code ou clique em 'Usar nesta janela' se necessário, então pressione Enter no terminal...")
input()  # Aguarda autenticação

# Função para enviar mensagem
def enviar_mensagem(numero, mensagem):
    try:
        mensagem_encoded = urllib.parse.quote(mensagem)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_encoded}"
        webbrowser.open(url)
        print(f"Aguardando o chat carregar para {numero}...")
        time.sleep(7)  # Aumentado para 7s
        
        # Forçar foco e enviar
        pyautogui.press('tab')  # Tenta focar no campo
        time.sleep(0.5)
        pyautogui.press('enter')  # Envia
        print(f"Mensagem enviada para {numero}")
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')  # Fecha a guia
    except Exception as e:
        print(f"Erro ao enviar para {numero}: {str(e)}")

# Carregar a lista de contatos
try:
    contatos_df = pd.read_csv("contatos.csv", dtype={'numero': str})
except FileNotFoundError:
    print("Erro: O arquivo 'contatos.csv' não foi encontrado.")
    exit()

print("Colunas encontradas no CSV:", contatos_df.columns.tolist())
if "numero" not in contatos_df.columns:
    print("Erro: A coluna 'numero' não foi encontrada.")
    exit()

print("Números carregados do CSV:")
print(contatos_df['numero'].tolist())

mensagem = "Olá, esta é uma mensagem automática enviada pelo bot!"

for index, row in contatos_df.iterrows():
    numero = row["numero"].strip()
    if not numero.startswith('+'):
        numero = '+' + numero
    if not numero[1:].isdigit():
        print(f"Número inválido: {numero}")
        continue
    print(f"Enviando mensagem para {numero}...")
    enviar_mensagem(numero, mensagem)
    time.sleep(random.uniform(6, 8))  # Aumentado para 6-8s

print("Envio de mensagens concluído!")