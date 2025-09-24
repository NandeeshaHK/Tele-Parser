#!/usr/bin/env python3
"""
Train a simple TF model using Parquet files in PARQUET_OUTPUT_DIR.
This is a small example — replace featurization & preprocessing with your production logic.
"""
import os
import glob
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
from src.common.config import PARQUET_OUTPUT_DIR, SAVED_MODEL_DIR
from src.training.model import build_model

def load_parquets(dirpath):
    files = glob.glob(os.path.join(dirpath, "*.parquet"))
    if not files:
        raise RuntimeError("No parquet files found in " + dirpath)
    dfs = [pq.read_table(f).to_pandas() for f in files]
    df = pd.concat(dfs, ignore_index=True)
    return df

def select_features(df):
    # pick numeric features for demo
    feature_cols = []
    for c in ['speed', 'throttle', 'brake', 'gear', 'track_temp', 'speed_mean']:
        if c in df.columns:
            feature_cols.append(c)
    X = df[feature_cols].astype(float).values
    # target: if predicted_lap_time exists use else derive (here we suppose lap_time column)
    if 'predicted_lap_time' in df.columns and df['predicted_lap_time'].notnull().any():
        y = df['predicted_lap_time'].astype(float).values
    elif 'lap_time' in df.columns:
        y = df['lap_time'].astype(float).values
    else:
        # synthetic target for example (not for production)
        y = (100.0 / (X[:, 0] + 1.0)).astype(float)
    return X, y

def train():
    df = load_parquets(PARQUET_OUTPUT_DIR)
    print("Loaded rows:", len(df))
    X, y = select_features(df)
    model = build_model(X.shape[1])
    model.fit(X, y, epochs=10, batch_size=64, validation_split=0.1)
    Path(SAVED_MODEL_DIR).mkdir(parents=True, exist_ok=True)
    export_path = Path(SAVED_MODEL_DIR) / "1"
    model.save(export_path.as_posix(), save_format="tf")
    print("Saved model to", export_path)

if __name__ == "__main__":
    train()
