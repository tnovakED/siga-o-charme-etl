import pandas as pd
from pathlib import Path

# Caminho para os arquivos Parquet
parquet_path_2024 = Path(r"G:\Meu Drive\SigaoCharmeETL\data\silver\vendas2024_silver_parquet")
#parquet_path_2025 = Path(r"G:\Meu Drive\SigaoCharmeETL\data\silver\venda_x_item_jan_set_25_silver_parquet")

# Lendo os arquivos Parquet
df_2024 = pd.read_parquet(parquet_path_2024)
#df_2025 = pd.read_parquet(parquet_path_2025)

# Visualizando número de linhas
print(f"Número de linhas 2024: {len(df_2024)}")
#print(f"Número de linhas 2025: {len(df_2025)}")

# Visualizando as primeiras linhas
print("\nPrimeiras linhas 2024:")
print(df_2024.head())

print("\nPrimeiras linhas 2025:")
#print(df_2025.head())

# Opcional: visualizar tipos das colunas
print("\nTipos das colunas 2024:")
print(df_2024.dtypes)

print("\nTipos das colunas 2025:")
#print(df_2025.dtypes)
'''
import pandas as pd
from pathlib import Path

# Caminho da pasta onde estão os arquivos originais
landing_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\landing_files")

# Verifica se a pasta existe
if not landing_path.exists():
    print("⚠️ A pasta especificada não foi encontrada.")
else:
    print(f"📂 Verificando arquivos em: {landing_path}\n")

    total_linhas = 0  # contador geral de linhas

    # Itera sobre todos os arquivos XLSX
    for arquivo in landing_path.glob("*.xlsx"):
        try:
            # Lê apenas a primeira planilha do arquivo
            df = pd.read_excel(arquivo, sheet_name=0)
            linhas, colunas = df.shape

            print(f"🧾 Arquivo: {arquivo.name}")
            print(f"   ➤ Linhas: {linhas:,} | Colunas: {colunas}")
            print(f"   ➤ Primeiras colunas: {list(df.columns[:5])}\n")

            total_linhas += linhas

        except Exception as e:
            print(f"❌ Erro ao ler {arquivo.name}: {e}\n")

    print(f"📊 Total geral de linhas em todos os arquivos: {total_linhas:,}")
''''''
import pandas as pd
from pathlib import Path

landing_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\landing_files")
print(f"📂 Verificando arquivos HTML disfarçados de XLS em: {landing_path}\n")

total_linhas = 0

for arquivo in landing_path.glob("*.xls"):
    try:
        # Lê a primeira tabela HTML do arquivo
        tables = pd.read_html(arquivo)
        if not tables:
            print(f"⚠️ Nenhuma tabela encontrada em {arquivo.name}")
            continue

        df = tables[0]
        linhas = len(df)
        total_linhas += linhas

        print(f"✅ {arquivo.name} -> {linhas} linhas, {len(df.columns)} colunas")

    except Exception as e:
        print(f"❌ Erro ao ler {arquivo.name}: {e}")

print(f"\n📊 Total geral de linhas em todos os arquivos: {total_linhas}")'''
