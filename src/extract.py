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

excel_files = landing_path / "venda_itens.xlsx"

if not excel_files.exists():
    raise FileNotFoundError(f"O Arquivo nao foi encontrado: {excel_files}")

df = pd.read_excel(excel_files)

#Verificando a quantidade de linhas que tem a palavra CONSUMIDOR, previamente verificada, para excluí-las
#num_oc = df['Título'].astype(str).str.upper().str.contains('CONSUMIDOR').sum()
#print(f'numerom de ocorrencias: {num_oc}')

#Eliminando essas linhas
df = df[~df['Título'].astype(str).str.startswith('1 - CONSUMIDOR')]

#salvando em csv para a pasta bronze para depois tratar tipos de dados
csv_file = bronze_path/"venda_itens.csv"
df.to_csv(csv_file, index=False)

arquivo_processado = Path(file_processed_folder)

for arquivo in landing_path.glob("*.xlsx"):
    destino = file_processed_folder / arquivo.name
    shutil.move(arquivo, destino)
