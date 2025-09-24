from ariadne import QueryType
import numpy as np
import os
from typing import List
from src.common.config import SAVED_MODEL_DIR
import tensorflow as tf

query = QueryType()

# lazy-load model
_TF_MODEL = None

def _load_model():
    global _TF_MODEL
    if _TF_MODEL is None:
        model_path = os.getenv("SAVED_MODEL_DIR", SAVED_MODEL_DIR) + "/1"
        if not tf.io.gfile.exists(model_path):
            print("Model path not found:", model_path)
            _TF_MODEL = None
            return None
        _TF_MODEL = tf.keras.models.load_model(model_path)
    return _TF_MODEL

@query.field("health")
def resolve_health(_, info):
    return "ok"

@query.field("predict")
def resolve_predict(_, info, features: List[float]):
    model = _load_model()
    if model is None:
        return None
    arr = np.array(features, dtype=float).reshape(1, -1)
    pred = model.predict(arr)
    return float(pred[0][0])
