import requests
import time
import sys
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# --- 1. CONFIGURAÇÕES PRINCIPAIS (Lendo do Jenkins) ---

# O Jenkins vai injetar a credencial 'CRASHKEN_API_KEY' na variável 'CRASHKEN_SECRET'
API_KEY = os.environ.get("CRASHKEN_SECRET")

# Se o segredo não for encontrado, o script para
if not API_KEY:
    print("ERRO CRÍTICO: A variável de ambiente 'CRASHKEN_SECRET' não foi definida no Jenkins!")
    sys.exit(1)

 Base da URL da API
CRASHKEN_BASE_URL = "https://hmlg.crashken.com/" 

#URL do seu servidor Appium (onde o Jenkins irá se conectar)
APPIUM_SERVER_URL = "http://127.0.0.1:4723" # Pode ser "https://vivo.crashken.com/wd/hub"

# Informações do dispositivo
DEVICE_ID = "6613f12555b9f5763b80fc21"
DEVICE_SERIAL = "RXCTA04ANWB" 

# Headers da API
HEADERS = {
    "Content-Type": "application/json"
}

# Endpoints da API
ALLOC_URL = f"{CRASHKEN_BASE_URL}/services/device/ticket/alloc"


RELEASE_URL = f"{CRASHKEN_BASE_URL}/services/device/ticket/release" 


# --- 2. INÍCIO DA EXECUÇÃO ---

driver = None
ticket_alocado = False

try:
    # --- 3. PARTE 1: RESERVAR O DISPOSITIVO (ALOCAR TICKET) ---
    print(f"Tentando alocar ticket para o dispositivo ID: {DEVICE_ID}...")
    
    # Payload para alocar (baseado na sua imagem)
    alloc_payload = {
        "apiKey": API_KEY,
        "deviceId": DEVICE_ID
    }

    response = requests.post(ALLOC_URL, json=alloc_payload, headers=HEADERS, timeout=30)
    
    # Verifica se a resposta foi 200 (Sucesso)
    if response.status_code == 200:
        print("Ticket alocado com sucesso!")
        ticket_alocado = True
    else:
        # Se der erro (400, 403, 500), mostra e para
        print(f"Erro ao alocar dispositivo. Status Code: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        raise requests.exceptions.RequestException(f"Falha na API: {response.text}")

    # --- 4. PARTE 2: CONFIGURAR E CONECTAR O APPIUM ---
    print(f"Configurando sessão Appium para o serial: {DEVICE_SERIAL}...")
    
    options = UiAutomator2Options()
    options.platform_name = "Android"
    
    # Usamos o 'serial' para o Appium saber qual dispositivo físico usar
    options.udid = DEVICE_SERIAL 
    
    # App da Calculadora (exemplo)
    options.app_package = "com.google.android.calculator"
    options.app_activity = "com.android.calculator2.Calculator"
    options.automation_name = "UiAutomator2"
    options.no_reset = True
    
    print(f"Conectando ao Appium em {APPIUM_SERVER_URL}...")
    driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(10)
    print("Conexão Appium estabelecida!")

    # --- 5. PARTE 3: EXECUTAR O TESTE ---
    print("Iniciando teste da calculadora (5 + 3 = 8)...")
    
    el_cinco = driver.find_element(by=AppiumBy.ID, value="com.google.android.calculator:id/digit_5")
    el_cinco.click()

    el_soma = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="plus")
    el_soma.click()

    el_tres = driver.find_element(by=AppiumBy.ID, value="com.google.android.calculator:id/digit_3")
    el_tres.click()

    el_igual = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="equals")
    el_igual.click()
    
    time.sleep(1)
    
    el_resultado = driver.find_element(by=AppiumBym.ID, value="com.google.android.calculator:id/result_final")
    
    assert el_resultado.text == "8"
    print("TESTE CONCLUÍDO COM SUCESSO!")

except requests.exceptions.RequestException as e:
    print(f"ERRO DE API (Crashken): {e}")
    sys.exit(1) # Sai com código de erro

except Exception as e:
    print(f"ERRO DURANTE O TESTE (Appium): {e}")
    sys.exit(1) # Sai com código de erro

finally:
    # --- 6. PARTE 4: LIBERAR O DISPOSITIVO (CRÍTICO!) ---
    
    # PASSO 1: Encerrar a sessão do Appium
    if driver:
        print("Fechando a sessão do Appium...")
        driver.quit()
        
    # PASSO 2: Liberar o ticket no Crashken
    if ticket_alocado:
        print(f"Liberando o ticket do dispositivo {DEVICE_ID} no Crashken...")
        try:
            release_payload = {
                "apiKey": API_KEY,
                "deviceId": DEVICE_ID
            }
            response = requests.post(RELEASE_URL, json=release_payload, headers=HEADERS, timeout=30)
            print("Dispositivo liberado com sucesso.")
        except requests.exceptions.RequestException as e:
            print(f"ALERTA: Falha ao liberar o dispositivo! {e}")