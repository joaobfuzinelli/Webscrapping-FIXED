#Bibilotecas importadas (Requests, BeautifulSoup, Time)
import requests
from bs4 import BeautifulSoup
import time

# URL inicial
url = "https://dadosabertos.pgfn.gov.br/"

# Headers corrigidos 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# HREF (Para verificar)
href = "Dados_abertos_Nao_Previdenciario.zip"
url_list = [url]

while True:
    # Loop para baixar os arquivos .zip (Nao previdenciário)
    for url_to_check in url_list:
        response = requests.get(url_to_check, headers=headers, stream=True)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Processar ou salvar o conteúdo, se necessário
            print(f"Download bem-sucedido para: {url_to_check}")
            with open(f"Dados_abertos_{url_to_check.split('/')[-2]}.zip", 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            print(f"Falha no download para: {url_to_check}")

    # Extrair links mais recentes
    novos_links = set()
    for url_to_check in url_list:
        response = requests.get(url_to_check, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links_atuais = set(a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip'))
            novos_links.update(links_atuais)

    # Comparar com os links existentes
    links_existentes = set(url_list)
    links_adicionados = novos_links - links_existentes

    if links_adicionados:
        print("Novas pastas adicionadas:")
        for link_adicionado in links_adicionados:
            print(link_adicionado)

        # Atualizar a lista de URLs com os novos links
        url_list.extend(links_adicionados)

    # Aguardar antes da próxima verificação (por exemplo, 1 hora)
    time.sleep(3600)
