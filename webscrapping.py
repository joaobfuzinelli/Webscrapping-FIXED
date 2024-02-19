import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

"""
Script para baixar arquivos .zip de uma URL e verificar periodicamente novos arquivos.
"""

# URL inicial
url = "https://dadosabertos.pgfn.gov.br/"

# Headers corrigidos 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

url_list = [url]

def download_zip(url_to_check):
    response = requests.get(url_to_check, headers=headers, stream=True)
    
    if response.status_code == 200:
        filename = urlparse(url_to_check).path.split('/')[-2]
        with open(f"Dados_abertos_{filename}.zip", 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"Download bem-sucedido para: {url_to_check}")
    else:
        print(f"Falha no download para: {url_to_check}")

def extract_links(url_to_check):
    response = requests.get(url_to_check, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip'))
    else:
        return set()

while True:
    for url_to_check in url_list:
        download_zip(url_to_check)

    novos_links = set()
    for url_to_check in url_list:
        novos_links.update(extract_links(url_to_check))
    
    links_adicionados = novos_links - set(url_list)

    if links_adicionados:
        print("Novas pastas adicionadas:")
        for link_adicionado in links_adicionados:
            url_list.append(link_adicionado)
            print(link_adicionado)

    # Aguardar antes da próxima verificação (por exemplo, 1 hora)
    time.sleep(3600)
