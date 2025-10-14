import pandas as pd
import pathlib as Path

drive_path = Path(r"C:\Users\Tiago\Google Drive\SigaoCharmeETL\data")

landing_path = drive_path / "landing_files"
bronze_path = drive_path / "bronze"


csv_files = landing_path / "vendas_itens.csv"
df = pd.read_csv(csv_files, sep=',', encoding='utf-8')

parquet_file = bronze_path / "vendas_item.parquet"

bronze_path.mkdir(parents=True, exist_ok=True)
df.to_parquet(parquet_file, index=False)

print(f"Arquivo salvo em: {parquet_file}")