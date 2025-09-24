#!/usr/bin/env python3
"""
Read NDJSON raw batches and perform minimal feature extraction using PyArrow & Pandas.
Writes Parquet files per run to PARQUET_OUTPUT_DIR.
"""
import os
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import glob
import json
from src.common.config import RAW_OUTPUT_DIR, PARQUET_OUTPUT_DIR

Path(PARQUET_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def ndjson_to_parquet():
    files = sorted(glob.glob(os.path.join(RAW_OUTPUT_DIR, "*.ndjson")))
    if not files:
        print("No ndjson files found in", RAW_OUTPUT_DIR)
        return
    for fpath in files:
        rows = []
        with open(fpath, "r") as fh:
            for line in fh:
                try:
                    rows.append(json.loads(line))
                except:
                    continue
        if not rows:
            continue
        df = pd.DataFrame(rows)
        # minimal feature engineering: compute rolling speed average per car if available
        if 'speed' in df.columns:
            df['speed_mean'] = df.groupby('car_id')['speed'].transform(lambda s: s.rolling(3, min_periods=1).mean())
        # fillna and casting
        df = df.fillna(0)
        outname = Path(PARQUET_OUTPUT_DIR) / (Path(fpath).stem + ".parquet")
        table = pa.Table.from_pandas(df)
        pq.write_table(table, outname)
        print("Wrote", outname)
        # optionally remove raw file after processing
        # os.remove(fpath)

if __name__ == "__main__":
    ndjson_to_parquet()
