import pandas as pd
from unidecode import unidecode
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import shutil

# Paths
input_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\bronze")
output_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data")
file_processed = Path(r"G:\Meu Drive\SigaoCharmeETL\data\files_processed")
silver_folder = output_path / "silver"

# Criar pastas se não existirem
silver_folder.mkdir(parents=True, exist_ok=True)
file_processed.mkdir(parents=True, exist_ok=True)

dfs = []

for arquivo in input_path.glob("venda*.csv"):
    df = pd.read_csv(arquivo, dtype=str)  # lê tudo como string

    # Normaliza colunas
    df.columns = [unidecode(col).lower().replace(' ', '_') for col in df.columns]
    df = df.rename(columns={'titulo': 'id_venda'})

    # Limpa e converte colunas numéricas
    numeric_cols = ['id_venda','vendedor','item','quantidade','valor_unitario','valor_total']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r'[^\d,.-]', '', regex=True)
                .str.replace(',', '.', regex=False)
            )
            if col in ['id_venda','vendedor','item','quantidade']:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(0).astype('Int64')
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # Coluna de controle
    df['data_proc'] = pd.Timestamp.now()

    dfs.append((arquivo.stem, df))

# Salvar em Parquet
for nome, df in dfs:
    table = pa.Table.from_pandas(df)
    parquet_path = silver_folder / f"{nome}_silver_parquet"

    pq.write_to_dataset(
        table,
        root_path=parquet_path,
        compression='snappy'
    )

    
    # Mover arquivo processado
    shutil.move(input_path / f"{nome}.csv", file_processed / f"{nome}.csv")
