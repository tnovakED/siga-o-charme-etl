# This Python script is performing the following tasks:
import pandas as pd
import shutil
from pathlib import Path

drive_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data")
landing_path = drive_path / "landing_files"
bronze_path = drive_path / "bronze"
file_processed_folder = drive_path / "files_processed"

# Criar as pastas se nao existirem
bronze_path.mkdir(parents=True, exist_ok=True)
file_processed_folder.mkdir(parents=True, exist_ok=True)

for arquivo in landing_path.glob("*.xlsx"):
#excel_files = landing_path / "venda_itens.xlsx"

    df = pd.read_excel(arquivo)
    print(f"Arquivo excel lido")
    
    '''Verificando a quantidade de linhas que tem a palavra CONSUMIDOR, previamente verificada, para excluí-las
    num_oc = df['Título'].astype(str).str.upper().str.contains('CONSUMIDOR').sum()
    print(f'numerom de ocorrencias: {num_oc}')'''

 #   Eliminando essas linhas - Parte Atualizada para tratar diversos tipos de caracteres nessa coluna
    df = df[~df['Título'].astype(str).str.contains(r'^.*\s-\s')]

    #salvando em csv para a pasta bronze para depois tratar tipos de dados
    csv_file = bronze_path / (arquivo.stem + ".csv")
    df.to_csv(csv_file, index=False)

    shutil.move(arquivo, file_processed_folder / arquivo.name)
