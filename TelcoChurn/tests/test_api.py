import sys
from pathlib import Path

# garante que o pytest encontra o módulo da API, independente de onde for executado
sys.path.append(str(Path(__file__).resolve().parent.parent / "api"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# --- Payload de exemplo reutilizável entre os testes ---
VALID_CUSTOMER = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 5,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 351.75
}


# ============================================================
# TESTES DO /health
# ============================================================
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ============================================================
# TESTES DO /predict — caminho feliz
# ============================================================
def test_predict_valid_input_returns_200():
    response = client.post("/predict", json=VALID_CUSTOMER)
    assert response.status_code == 200


def test_predict_response_has_expected_fields():
    response = client.post("/predict", json=VALID_CUSTOMER)
    data = response.json()

    assert "churn_probability" in data
    assert "risk_level" in data
    assert "will_churn" in data
    assert "top_reasons" in data


def test_predict_probability_is_valid_range():
    response = client.post("/predict", json=VALID_CUSTOMER)
    data = response.json()

    assert 0.0 <= data["churn_probability"] <= 1.0


def test_predict_risk_level_is_valid_category():
    response = client.post("/predict", json=VALID_CUSTOMER)
    data = response.json()

    assert data["risk_level"] in ["Baixo", "Médio", "Alto"]


def test_predict_top_reasons_has_three_items():
    response = client.post("/predict", json=VALID_CUSTOMER)
    data = response.json()

    assert len(data["top_reasons"]) == 3


def test_predict_high_risk_profile_month_to_month_new_customer():
    """Cliente com perfil classicamente arriscado (contrato mensal, pouco tempo de casa,
    poucos serviços) deve retornar probabilidade de churn mais alta que a média."""
    high_risk_customer = {**VALID_CUSTOMER, "tenure": 1, "Contract": "Month-to-month"}
    response = client.post("/predict", json=high_risk_customer)
    data = response.json()

    assert data["churn_probability"] > 0.3  # ajuste esse limiar conforme seu modelo


def test_predict_low_risk_profile_long_contract_loyal_customer():
    """Cliente com contrato de 2 anos e muito tempo de casa deve ter risco baixo."""
    low_risk_customer = {
        **VALID_CUSTOMER, "tenure": 60, "Contract": "Two year",
        "OnlineSecurity": "Yes", "TechSupport": "Yes"
    }
    response = client.post("/predict", json=low_risk_customer)
    data = response.json()

    assert data["churn_probability"] < 0.5  # ajuste esse limiar conforme seu modelo


# ============================================================
# TESTES DO /predict — validação de entrada (dados inválidos)
# ============================================================
def test_predict_missing_required_field_returns_422():
    incomplete_customer = VALID_CUSTOMER.copy()
    del incomplete_customer["tenure"]

    response = client.post("/predict", json=incomplete_customer)
    assert response.status_code == 422  # erro de validação do Pydantic


def test_predict_invalid_contract_value_returns_422():
    invalid_customer = {**VALID_CUSTOMER, "Contract": "Weekly"}  # valor não existe no schema

    response = client.post("/predict", json=invalid_customer)
    assert response.status_code == 422


def test_predict_negative_monthly_charges_returns_422():
    invalid_customer = {**VALID_CUSTOMER, "MonthlyCharges": -50.0}

    response = client.post("/predict", json=invalid_customer)
    assert response.status_code == 422


def test_predict_empty_body_returns_422():
    response = client.post("/predict", json={})
    assert response.status_code == 422


# ============================================================
# TESTES DO /predict/batch
# ============================================================
def test_predict_batch_with_multiple_customers():
    payload = [VALID_CUSTOMER, VALID_CUSTOMER]
    response = client.post("/predict/batch", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_predict_batch_empty_list_returns_empty_result():
    response = client.post("/predict/batch", json=[])
    assert response.status_code == 200
    assert response.json() == []


def test_predict_batch_with_one_invalid_customer_returns_422():
    payload = [VALID_CUSTOMER, {**VALID_CUSTOMER, "Contract": "Weekly"}]
    response = client.post("/predict/batch", json=payload)

    assert response.status_code == 422