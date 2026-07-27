from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import joblib
import shap
import pandas as pd
from xgboost import XGBClassifier

from schemas import Customer, PredictionResponse
from preprocessing import preprocess

app = FastAPI(
    title="Telco Churn Prediction API",
    description="Prevê o risco de cancelamento de clientes de telecom.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Carregamento do modelo, threshold e explainer (uma única vez, na subida da API) ---
model = XGBClassifier()
model.load_model(str(BASE_DIR / "models" / "xgb_churn_model.json"))

threshold = joblib.load(BASE_DIR / "models" / "best_threshold.pkl")

explainer = shap.TreeExplainer(model)


def classify_risk(proba: float) -> str:
    if proba >= 0.7:
        return "Alto"
    elif proba >= threshold:
        return "Médio"
    else:
        return "Baixo"


def get_top_reasons(df_processed: pd.DataFrame, n: int = 3) -> dict:
    shap_values = explainer.shap_values(df_processed)
    contrib = pd.Series(shap_values[0], index=df_processed.columns)
    top = contrib.sort_values(key=abs, ascending=False).head(n)
    return {k: round(float(v), 4) for k, v in top.items()}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: Customer):
    try:
        df_processed = preprocess(customer.model_dump())
        proba = float(model.predict_proba(df_processed)[0][1])
        reasons = get_top_reasons(df_processed)

        return PredictionResponse(
            churn_probability=round(proba, 4),
            risk_level=classify_risk(proba),
            will_churn=proba >= threshold,
            top_reasons=reasons
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/batch")
def predict_batch(customers: list[Customer]):
    results = []
    for customer in customers:
        df_processed = preprocess(customer.model_dump())
        proba = float(model.predict_proba(df_processed)[0][1])
        results.append({
            "churn_probability": round(proba, 4),
            "risk_level": classify_risk(proba),
            "will_churn": proba >= threshold
        })
    return JSONResponse(content=results)