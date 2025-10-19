import pandas as pd
from pathlib import Path

# Caminho da pasta do dataset Parquet
caminho = Path(r'G:\Meu Drive\SigaoCharmeETL\data\silver\vendas2024_silver2.parquet')

# Ler o dataset Parquet inteiro (pasta)
df = pd.read_parquet(caminho)

# Exibir as primeiras linhas e colunas
print(df.head())
print(df.columns)

# Converter a coluna para número (ajuste o nome conforme aparecer)
df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')

# Calcular total
total = df['valor_total'].sum()

print(f"\n💰 Total de Vendas (coluna ValorTotal): R$ {total:,.2f}")
print(f"📊 Total de linhas: {len(df)}")
