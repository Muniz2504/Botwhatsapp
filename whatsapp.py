import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import urllib.parse
import os

# Função para configurar o WebDriver com base no navegador padrão
def get_browser_driver():
    try:
        browser = webbrowser.get()  # Obtém o navegador padrão
        print(f"Navegador padrão detectado: {browser.name}")
        
        # Ajuste manual do WebDriver (procura na pasta atual)
        driver_path = os.path.join(os.getcwd(), "chromedriver.exe")  # Padrão para Chrome
        if "firefox" in browser.name.lower():
            driver_path = os.path.join(os.getcwd(), "geckodriver.exe")
        elif "edge" in browser.name.lower():
            driver_path = os.path.join(os.getcwd(), "msedgedriver.exe")
        
        if not os.path.exists(driver_path):
            raise Exception(f"WebDriver não encontrado em {driver_path}. Instale o WebDriver correspondente na pasta do script ou especifique o caminho.")
        
        if "chrome" in browser.name.lower():
            return webdriver.Chrome(executable_path=driver_path)
        elif "firefox" in browser.name.lower():
            return webdriver.Firefox(executable_path=driver_path)
        elif "edge" in browser.name.lower():
            return webdriver.Edge(executable_path=driver_path)
        else:
            raise Exception("Navegador padrão não suportado. Use Chrome, Firefox ou Edge.")
    except Exception as e:
        print(f"Erro ao configurar o WebDriver: {str(e)}. Certifique-se de ter o WebDriver correspondente instalado na pasta do script.")
        exit()

# Configurar o navegador
try:
    driver = get_browser_driver()
except Exception as e:
    print(f"Falha na configuração: {str(e)}")
    exit()

# Abrir WhatsApp Web no navegador padrão (sem pausa para QR code)
webbrowser.open("https://web.whatsapp.com")
print("Abrindo WhatsApp Web no navegador padrão. Certifique-se de que a sessão já está logada.")
time.sleep(5)  # Pequena pausa para o navegador abrir

# Verificar se o WhatsApp Web está logado
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Novo chat"]'))
    )
    print("Sessão do WhatsApp Web detectada como logada.")
except Exception:
    print("Erro: Sessão do WhatsApp Web não detectada. Certifique-se de que o WhatsApp Web está logado antes de executar o script.")
    driver.quit()
    exit()

# Função para enviar mensagem
def enviar_mensagem(numero, mensagem):
    try:
        # Codificar a mensagem e criar a URL do WhatsApp
        mensagem_encoded = urllib.parse.quote(mensagem)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_encoded}"
        driver.get(url)
        print(f"Aguardando o chat carregar para {numero}...")
        
        # Aguardar até que o chat esteja carregado
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="_21Szn"]'))
        )
        
        # Aguardar até que o campo de texto esteja clicável
        campo_texto = WebDriverWait(driver, 40).until(
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