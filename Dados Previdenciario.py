import zipfile
import pandas as pd
import os

# Nome do arquivo zip a ser lido
zip_filename = "Caminho/Para/Dados_abertos_Nao_Previdenciario.zip"

# Pasta de destino para extrair o conteúdo
extract_folder = "Caminho/Para/Extrair/Conteudo"

# Garante que a pasta de extração exista ou cria se não existir
os.makedirs(extract_folder, exist_ok=True)

def extract_and_save_excel(zip_filename, extract_folder):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        # Obtém uma lista de nomes de arquivos dentro do zip
        file_names = zip_ref.namelist()

        for file_name in file_names:
            # Extrai cada arquivo para a pasta de destino
            zip_ref.extract(file_name, extract_folder)

            # Verifica se o arquivo é um arquivo Excel (.xlsx)
            if file_name.endswith('.xlsx'):
                # Lê o arquivo Excel usando pandas
                excel_df = pd.read_excel(os.path.join(extract_folder, file_name))

                # Salva as informações (ou realiza o processamento desejado)
                save_path = os.path.join("Caminho/Para/Salvar", f"{file_name.replace('.xlsx', '.csv')}")
                excel_df.to_csv(save_path, index=False, encoding='utf-8')

                print(f"Conteúdo do arquivo Excel {file_name} salvo como CSV em {save_path}")

# Chama a função para extrair e salvar o conteúdo Excel
extract_and_save_excel(zip_filename, extract_folder)
