import streamlit as st
import pandas as pd
import joblib

# Load saved model and feature list
model = joblib.load("household_expenditure_model.pkl")
features = joblib.load("model_features.pkl")

st.set_page_config(
    page_title="Household Expenditure Predictor",
    layout="wide"
)

st.title("Household Expenditure Prediction Tool")
st.write(
    "This app estimates annual household expenditure using income, demographic, "
    "and household characteristics."
)

st.sidebar.header("Enter Household Details")

# User inputs
year = st.sidebar.selectbox("Year", [2024, 2025, 2026])

region = st.sidebar.selectbox(
    "Region",
    ["South", "Midwest", "Northeast", "West"]
)

urban_type = st.sidebar.selectbox(
    "Urban Type",
    ["Urban", "Rural"]
)

age_group = st.sidebar.selectbox(
    "Age Group",
    ["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]
)

education_level = st.sidebar.selectbox(
    "Education Level",
    ["Less than HS", "High School", "Some College", "Bachelor+", "Graduate"]
)

housing_tenure = st.sidebar.selectbox(
    "Housing Tenure",
    ["Own", "Rent"]
)

marital_status = st.sidebar.selectbox(
    "Marital Status",
    ["Single", "Married", "Other"]
)

race_group = st.sidebar.selectbox(
    "Race Group",
    ["White", "Black", "Asian", "Other"]
)

hispanic_origin = st.sidebar.selectbox(
    "Hispanic Origin",
    ["Yes", "No"]
)

household_size = st.sidebar.number_input(
    "Household Size",
    min_value=1,
    max_value=6,
    value=2
)

number_of_earners = st.sidebar.number_input(
    "Number of Earners",
    min_value=0,
    max_value=6,
    value=1
)

wages = st.sidebar.number_input(
    "Wages/Salaries (USD)",
    min_value=0,
    value=60000
)

retirement = st.sidebar.number_input(
    "Retirement/Social Security (USD)",
    min_value=0,
    value=5000
)

transfers = st.sidebar.number_input(
    "Public Assistance Transfers (USD)",
    min_value=0,
    value=1000
)

interest = st.sidebar.number_input(
    "Interest/Dividends (USD)",
    min_value=0,
    value=500
)

income_before_tax = st.sidebar.number_input(
    "Total Income Before Tax (USD)",
    min_value=0,
    value=70000
)

taxes = st.sidebar.number_input(
    "Estimated Taxes (USD)",
    min_value=0,
    value=10000
)

income_after_tax = st.sidebar.number_input(
    "Income After Tax (USD)",
    min_value=0,
    value=60000
)

# Create input row
input_data = pd.DataFrame([{
    "Year": year,
    "Region": region,
    "Urban_Type": urban_type,
    "Age_Group": age_group,
    "Education_Level": education_level,
    "Housing_Tenure": housing_tenure,
    "Marital_Status": marital_status,
    "Race_Group": race_group,
    "Hispanic_Origin": hispanic_origin,
    "Household_Size": household_size,
    "Number_of_Earners": number_of_earners,
    "Wages_Salaries_USD": wages,
    "Retirement_SocSec_USD": retirement,
    "Transfers_PublicAssist_USD": transfers,
    "Interest_Dividends_USD": interest,
    "Total_Income_Before_Tax_USD": income_before_tax,
    "Taxes_Estimated_USD": taxes,
    "Income_After_Tax_USD": income_after_tax
}])

# Keep only columns used by the model
# This prevents errors if extra fields exist
input_data = input_data.reindex(columns=features)

st.subheader("Input Summary")
st.dataframe(input_data)

if st.button("Predict Household Expenditure"):
    prediction = model.predict(input_data)[0]

    st.metric(
        "Predicted Annual Household Expenditure",
        f"${prediction:,.2f}"
    )

    if prediction > income_after_tax:
        st.warning(
            "Predicted expenditure is higher than after-tax income. "
            "This may indicate financial pressure."
        )
    else:
        st.success(
            "Predicted expenditure is within the household's after-tax income."
        )