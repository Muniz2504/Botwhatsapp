import webbrowser
import pyautogui
import pandas as pd
import time
import urllib.parse

# Abrir WhatsApp Web no navegador padrão
webbrowser.open("https://web.whatsapp.com")
print("Escaneie o QR code no WhatsApp Web e pressione Enter no terminal...")
input()  # Aguarda o usuário escanear o QR code

# Função para enviar mensagem
def enviar_mensagem(numero, mensagem):
    try:
        # Criar a URL do WhatsApp
        mensagem_encoded = urllib.parse.quote(mensagem)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_encoded}"
        webbrowser.open(url)
        print(f"Aguardando o chat carregar para {numero}...")
        time.sleep(10)  # Aguarda o chat carregar
        
        # Simular clique no campo de texto (ajuste as coordenadas conforme necessário)
        pyautogui.click(x=700, y=800)  # Coordenadas aproximadas do campo de texto
        time.sleep(1)
        pyautogui.press('enter')  # Pressiona Enter
        print(f"Mensagem enviada para {numero}")
        time.sleep(2)  # Pausa após o envio
    except Exception as e:
        print(f"Erro ao enviar para {numero}: {str(e)}")

# Carregar a lista de contatos do arquivo CSV
try:
    contatos_df = pd.read_csv("contatos.csv", dtype={'numero': str})
except FileNotFoundError:
    print("Erro: O arquivo 'contatos.csv' não foi encontrado.")
    exit()

# Verificar as colunas do CSV
print("Colunas encontradas no CSV:", contatos_df.columns.tolist())
if "numero" not in contatos_df.columns:
    print("Erro: A coluna 'numero' não foi encontrada.")
    exit()

# Verificar os números carregados
print("Números carregados do CSV:")
print(contatos_df['numero'].tolist())

# Mensagem a ser enviada
mensagem = "Olá, esta é uma mensagem automática enviada pelo bot!"

# Iterar sobre os números e enviar mensagens
for index, row in contatos_df.iterrows():
    numero = row["numero"]
    if not numero.startswith('+'):
        numero = '+' + numero
    print(f"Enviando mensagem para {numero}...")
    enviar_mensagem(numero, mensagem)
    time.sleep(10)  # Pausa entre envios para evitar bloqueios

print("Envio de mensagens concluído!")