#!/usr/bin/env python3
"""
Simple helper: copy saved model to expected TF Serving layout.
Usage:
  python src/serving/export_model.py --model-dir ./saved_model/1
"""
import argparse
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--model-dir", required=True)
parser.add_argument("--out", default="tf_serving_models/lap_model/1")
args = parser.parse_args()

src = Path(args.model_dir)
dst = Path(args.out)
dst.parent.mkdir(parents=True, exist_ok=True)
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print("Copied", src, "->", dst)
