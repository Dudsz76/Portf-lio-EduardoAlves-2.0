import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # sobe de api/ para a raiz do projeto
MODEL_COLUMNS = joblib.load(BASE_DIR / "models" / "model_columns.pkl")

SERVICE_COLS = [
    'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies'
]

def count_services(row):
    count = 0
    for col in SERVICE_COLS:
        if row[col] not in ['No', 'No internet service', 'No phone service']:
            count += 1
    return count

def tenure_group(t):
    if t <= 12: return '0-1 ano'
    elif t <= 24: return '1-2 anos'
    elif t <= 48: return '2-4 anos'
    else: return '4+ anos'

def preprocess(customer_dict: dict) -> pd.DataFrame:
    df = pd.DataFrame([customer_dict])

    # mesmas features criadas no treino
    df['NumServices'] = df.apply(count_services, axis=1)
    df['AvgChargePerTenure'] = df['TotalCharges'] / df['tenure'].replace(0, 1)
    df['IsNewCustomer'] = (df['tenure'] <= 6).astype(int)
    df['IsMonthToMonth'] = (df['Contract'] == 'Month-to-month').astype(int)
    df['TenureGroup'] = df['tenure'].apply(tenure_group)

    # mesmo one-hot encoding do treino
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # alinha com as colunas do treino: adiciona colunas faltantes com 0,
    # remove colunas extras, e garante a MESMA ORDEM
    df_encoded = df_encoded.reindex(columns=MODEL_COLUMNS, fill_value=0)

    return df_encoded