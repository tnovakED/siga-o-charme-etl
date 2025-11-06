import pandas as pd
from unidecode import unidecode
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import shutil

# Paths
input_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\bronze")
file_processed = Path(r"G:\Meu Drive\SigaoCharmeETL\data\files_processed")
silver_folder = Path(r"G:\Meu Drive\SigaoCharmeETL\data\silver")

# Criar pastas se não existirem
silver_folder.mkdir(parents=True, exist_ok=True)
file_processed.mkdir(parents=True, exist_ok=True)

parquet_file = silver_folder / "venda2025_silver.parquet"

dfs = []

# --- Processar todos os CSVs ---
for arquivo in input_path.glob("venda*.csv"):
    df = pd.read_csv(arquivo, dtype=str)

    # Normaliza colunas
    df.columns = [unidecode(col).lower().replace(' ', '_').strip() for col in df.columns]
    df = df.rename(columns={'titulo': 'id_venda', 'item': 'id_produto'})

    # Colunas numéricas
    numeric_cols = ['quantidade', 'valor_unitario', 'valor_total']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[^\d,.-]", "", regex=True)
                .str.replace(",", ".", regex=False)
            )
            if col == "quantidade":
                df[col] = pd.to_numeric(df[col], errors="coerce").round(0).astype("Int64")
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    # Colunas string
    string_cols = ["id_venda", "vendedor", "id_produto", "descricao"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
            if col == "id_produto":
                df[col] = df[col].str.replace("-", "", regex=False)

    # Converter data de emissão
    if "emissao" in df.columns:
        df["emissao"] = pd.to_datetime(df["emissao"], format="%d/%m/%Y", errors="coerce")

    # Adicionar data de processamento
    df["data_proc"] = pd.Timestamp.now().round("ms")

    dfs.append(df)

# --- Concatenar todos os CSVs lidos ---
df_novo = pd.concat(dfs, ignore_index=True)

# --- Se o Parquet já existir, faz append ---
if parquet_file.exists():
    df_existente = pd.read_parquet(parquet_file)
    df_final = pd.concat([df_existente, df_novo], ignore_index=True)
else:
    df_final = df_novo  # <- cria df_final mesmo se o arquivo não existir

# --- Definir schema ---
schema = pa.schema([
    (col, pa.string()) if df_final[col].dtype == "object" else
    (col, pa.int64()) if df_final[col].dtype.name.startswith("Int") else
    (col, pa.float64()) if df_final[col].dtype.name.startswith("float") else
    (col, pa.timestamp("ms")) if df_final[col].dtype.name.startswith("datetime") else
    (col, pa.string())
    for col in df_final.columns
])

# --- Salvar em Parquet ---
table = pa.Table.from_pandas(df_final, schema=schema, preserve_index=False)
pq.write_table(table, parquet_file, compression="snappy")

# --- Mover CSVs processados ---
for arquivo in input_path.glob("venda*.csv"):
    shutil.move(arquivo, file_processed / arquivo.name)
    print(f"✅ {arquivo.name} processado e salvo em {parquet_file}")
