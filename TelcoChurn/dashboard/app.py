import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Telco Churn - Dashboard de Retenção",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Risco de Churn")
st.markdown("Ferramenta de apoio ao time de vendas para identificar clientes em risco de cancelamento.")

# --- Abas: consulta individual vs. em lote ---
tab1, tab2 = st.tabs(["🔍 Consultar Cliente", "📁 Análise em Lote (CSV)"])

# ============================================================
# ABA 1: CONSULTA INDIVIDUAL
# ============================================================
with tab1:
    st.subheader("Dados do cliente")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gênero", ["Female", "Male"])
        senior = st.selectbox("Idoso (65+)", ["Não", "Sim"])
        partner = st.selectbox("Possui parceiro(a)", ["Yes", "No"])
        dependents = st.selectbox("Possui dependentes", ["Yes", "No"])
        tenure = st.number_input("Meses de casa (tenure)", min_value=0, max_value=100, value=12)
        contract = st.selectbox("Tipo de contrato", ["Month-to-month", "One year", "Two year"])

    with col2:
        phone_service = st.selectbox("Serviço de telefone", ["Yes", "No"])
        multiple_lines = st.selectbox("Múltiplas linhas", ["Yes", "No", "No phone service"])
        internet_service = st.selectbox("Serviço de internet", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Segurança online", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Backup online", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Proteção de dispositivo", ["Yes", "No", "No internet service"])

    with col3:
        tech_support = st.selectbox("Suporte técnico", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox("Streaming Filmes", ["Yes", "No", "No internet service"])
        paperless = st.selectbox("Fatura sem papel", ["Yes", "No"])
        payment_method = st.selectbox("Método de pagamento", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly_charges = st.number_input("Cobrança mensal (R$)", min_value=0.0, value=70.0, step=0.5)

    total_charges = st.number_input("Total já cobrado (R$)", min_value=0.0, value=float(monthly_charges * tenure), step=1.0)

    if st.button("🔎 Analisar risco de churn", type="primary"):
        payload = {
            "gender": gender,
            "SeniorCitizen": 1 if senior == "Sim" else 0,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            st.divider()
            col_a, col_b, col_c = st.columns(3)

            proba_pct = result["churn_probability"] * 100
            risk = result["risk_level"]

            color_map = {"Alto": "🔴", "Médio": "🟡", "Baixo": "🟢"}

            col_a.metric("Probabilidade de Churn", f"{proba_pct:.1f}%")
            col_b.metric("Nível de Risco", f"{color_map.get(risk, '')} {risk}")
            col_c.metric("Ação recomendada", "Contatar" if result["will_churn"] else "Monitorar")

            st.subheader("Principais fatores de risco")
            reasons_df = pd.DataFrame(
                list(result["top_reasons"].items()),
                columns=["Fator", "Impacto"]
            ).sort_values("Impacto", key=abs, ascending=True)

            fig = px.bar(
                reasons_df, x="Impacto", y="Fator", orientation="h",
                color="Impacto", color_continuous_scale=["#2E7D32", "#C62828"],
                title="Impacto de cada fator na predição (SHAP)"
            )
            st.plotly_chart(fig, use_container_width=True)

        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar à API. Verifique se ela está rodando em " + API_URL)
        except requests.exceptions.HTTPError as e:
            st.error(f"Erro na API: {e.response.json().get('detail', str(e))}")

# ============================================================
# ABA 2: ANÁLISE EM LOTE
# ============================================================
with tab2:
    st.subheader("Envie um CSV com sua carteira de clientes")
    st.caption("O arquivo deve conter as mesmas colunas do dataset original (sem customerID e sem Churn).")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"**{len(df)} clientes carregados.**")
        st.dataframe(df.head())

        if st.button("🚀 Rodar análise em lote", type="primary"):
            customers_payload = df.to_dict(orient="records")

            try:
                response = requests.post(f"{API_URL}/predict/batch", json=customers_payload, timeout=60)
                response.raise_for_status()
                results = response.json()

                results_df = pd.DataFrame(results)
                final_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)

                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Total de clientes", len(final_df))
                col2.metric("Risco Alto", (final_df["risk_level"] == "Alto").sum())
                col3.metric("Risco Médio", (final_df["risk_level"] == "Médio").sum())

                st.subheader("Distribuição de risco na carteira")
                fig = px.pie(final_df, names="risk_level", title="Clientes por nível de risco",
                             color="risk_level",
                             color_discrete_map={"Alto": "#C62828", "Médio": "#F9A825", "Baixo": "#2E7D32"})
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Clientes com maior risco (priorizar contato)")
                priority = final_df.sort_values("churn_probability", ascending=False).head(20)
                st.dataframe(
                    priority[["churn_probability", "risk_level", "will_churn"] + 
                             [c for c in df.columns if c in ["tenure", "Contract", "MonthlyCharges"]]],
                    use_container_width=True
                )

                csv_export = final_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Baixar resultado completo (CSV)",
                    csv_export,
                    "churn_predictions.csv",
                    "text/csv"
                )

            except requests.exceptions.ConnectionError:
                st.error("Não foi possível conectar à API. Verifique se ela está rodando em " + API_URL)
            except requests.exceptions.HTTPError as e:
                st.error(f"Erro na API: {e.response.text}")