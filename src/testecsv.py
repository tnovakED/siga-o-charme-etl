import pandas as pd
from pathlib import Path

# Caminho do arquivo CSV
arquivo_csv = Path(r'G:\Meu Drive\SigaoCharmeETL\data\files_processed\vendas2024.csv')

# Lê o CSV
df_csv = pd.read_csv(arquivo_csv)

# Mostra as primeiras linhas e colunas
print(df_csv.head())
print("\nColunas:", df_csv.columns)

# Verifica coluna de valor monetário
if 'Valor total' not in df_csv.columns:
    raise ValueError("A coluna 'Valor total' não existe no CSV.")
    
# Converte para número, caso haja strings ou vírgulas
df_csv['Valor total'] = pd.to_numeric(df_csv['Valor total'], errors='coerce')

# Soma e contagem
total_valor = df_csv['Valor total'].sum()
total_linhas = len(df_csv)

print(f"\n💰 Total de valor_total: R$ {total_valor:,.2f}")
print(f"📊 Total de linhas: {total_linhas}")
