from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.parse

# Configurar o navegador
driver = webdriver.Chrome()  # Certifique-se de ter o ChromeDriver instalado
driver.get("https://web.whatsapp.com")
print("Escaneie o QR code no WhatsApp Web e pressione Enter no terminal...")
input()  # Aguarda o usuário escanear o QR code

# Função para enviar mensagem
def enviar_mensagem(numero, mensagem):
    try:
        # Codificar a mensagem e criar a URL do WhatsApp
        mensagem_encoded = urllib.parse.quote(mensagem)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_encoded}"
        driver.get(url)
        print(f"Aguardando o chat carregar para {numero}...")
        
        # Aguardar até que o campo de texto esteja clicável
        campo_texto = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@title="Digite uma mensagem"]'))
        )
        print(f"Campo de texto encontrado para {numero}, clicando...")
        campo_texto.click()  # Clica no campo de texto para garantir o foco
        campo_texto.send_keys(Keys.ENTER)  # Pressiona Enter para enviar
        print(f"Mensagem enviada para {numero}")
        time.sleep(2)  # Pausa após o envio
    except Exception as e:
        print(f"Erro ao enviar para {numero}: {str(e)}")

# Carregar a lista de contatos do arquivo CSV
try:
    contatos_df = pd.read_csv("contatos.csv", dtype={'numero': str})
except FileNotFoundError:
    print("Erro: O arquivo 'contatos.csv' não foi encontrado.")
    driver.quit()
    exit()

# Verificar as colunas do CSV
print("Colunas encontradas no CSV:", contatos_df.columns.tolist())
if "numero" not in contatos_df.columns:
    print("Erro: A coluna 'numero' não foi encontrada.")
    driver.quit()
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
driver.quit()