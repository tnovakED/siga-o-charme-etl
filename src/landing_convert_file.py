import pandas as pd
from pathlib import Path
import shutil

input_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\landing_files")
output_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\landing_files")
processed_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\files_processed")

output_path.mkdir(parents=True, exist_ok=True)
processed_path.mkdir(parents=True, exist_ok=True)

try:
    for arquivo in input_path.glob("*.xls"):
        print(f"1-Lendo arquivo: {arquivo.name}")
        
        # Força o pandas a ler como HTML (funciona para XLS com tags <table>)
        df = pd.read_html(arquivo, decimal=",", thousands=".")[0]
        print(f"2-Arquivo lido com sucesso: {arquivo.name}")

        # Salva em XLSX
        nome_arquivo = output_path / (arquivo.stem + ".xlsx")
        df.to_excel(nome_arquivo, index=False)
        print(f"3-Arquivo salvo em: {nome_arquivo}")

        # Move o original
        shutil.move(str(arquivo), processed_path / arquivo.name)
        print(f"4-Arquivo movido para: {processed_path / arquivo.name}")

except Exception as e:
    print(f"Erro ao processar: {e}")
