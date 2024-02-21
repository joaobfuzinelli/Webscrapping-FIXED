#Bibliotecas usadas para fazer o WS
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# URL inicial
url = "https://dadosabertos.pgfn.gov.br/"

# Headers corrigidos 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

url_list = [url]

# Conjunto para armazenar as URLs já verificadas
checked_urls = set()

def download_zip(url_to_check):
    response = requests.get(url_to_check, headers=headers, stream=True)
    
    if response.status_code == 200:
        filename = urlparse(url_to_check).path.split('/')[-2]
        
        # Verifica se a URL já foi verificada anteriormente e se a pasta é nova
        if url_to_check not in checked_urls and "Dados_abertos_Nao_Previdenciario.zip" in filename:
            with open(f"Dados_abertos_{filename}.zip", 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
            print(f"Download bem-sucedido para: {url_to_check}")
            
            # Adiciona a URL ao conjunto de URLs verificadas
            checked_urls.add(url_to_check)
        else:
            print(f"URL já verificada anteriormente ou a pasta não corresponde à variável desejada: {url_to_check}")
    else:
        print(f"Falha no download para: {url_to_check}")

def extract_links(url_to_check):
    response = requests.get(url_to_check, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    else:
        return []

while True:
    novas_pastas = set()

    for url_to_check in url_list:
        novas_pastas.update(extract_links(url_to_check))

    links_adicionados = novas_pastas - set(url_list)

    if links_adicionados:
        print("Novas pastas adicionadas:")
        for link_adicionado in links_adicionados:
            url_list.append(link_adicionado)
            print(link_adicionado)

    for url_to_check in links_adicionados:
        download_zip(url_to_check)

    # Aguardar antes da próxima verificação (por exemplo, 1 hora)
    time.sleep(3600)
