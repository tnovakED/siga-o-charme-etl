import pandas as pd
from unidecode import unidecode
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq


input_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data\bronze")
output_path = Path(r"G:\Meu Drive\SigaoCharmeETL\data")

# Nome da pasta a ser criada
silver_folder = output_path / "silver"

silver_folder.mkdir(parents=True, exist_ok=True)

# Armazena os dataframes criados de acordo com os arquivos processados.
dfs = []

# Itera sobre a pasta onde estão os arquivos a serem processados.
for arquivo in input_path.glob("*.csv"):
    df = pd.read_csv(arquivo)
    
    # transfomação das colunas
    df.columns = [unidecode(col).lower().replace(' ', '_') for col in df.columns]
    df = df.rename(columns={'titulo': 'id_venda'})

    # Converter tipos de colunas
    df['id_venda'] = pd.to_numeric(df['id_venda'], errors='coerce').astype('Int64')
    df['emissao'] = pd.to_datetime(df['emissao'], dayfirst=True, errors='coerce')
    df['vendedor'] = pd.to_numeric(df['vendedor'], errors='coerce')
    df['item'] = pd.to_numeric(df['item'], errors='coerce').round(0).astype('Int64')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').round(0).astype('Int64')
    df['valor_unitario'] = pd.to_numeric(df['valor_unitario'], errors='coerce')
    df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
    
    # Coluna de controle
    df['data_proc'] = pd.Timestamp.now()
        
    #deleta linhas com valores nulos
    lista_colunas = ['id_venda','emissao','vendedor','item','quantidade','valor_unitario','valor_total']
    df = df.dropna(subset=lista_colunas)

    dfs.append((arquivo.stem,df))

# Gravação em Parquet
for nome, df in dfs:
    table = pa.Table.from_pandas(df)
    parquet_path = silver_folder / f"{nome}_silver_parquet" 
    
    pq.write_to_dataset(
        table,
        root_path=parquet_path,
        compression = 'snappy'
    )
    
    print(f"Arquivo salvo: {parquet_path}")
