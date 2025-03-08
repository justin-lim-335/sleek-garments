import streamlit as st
import pandas as pd
import plotly.express as px

# Dataset
countries = ["USA", "UK", "Denmark", "Netherlands", "Germany", "France", "South Africa",
             "Botswana", "Nigeria", "Kenya", "Bahamas", "Guyana"]

# Initialize default weights
weight_defaults = {
    "Market Size": 30,
    "Tariff & Shipping": 20,
    "Willingness to Pay": 30,
    "Seasonality": 0,
    "Sustainability & Customization": 20
}

# Sidebar sliders for weight adjustments
st.sidebar.header("Adjust Weights")
weights = {}
total_weight = 0

for key in weight_defaults:
    weights[key] = st.sidebar.slider(key, 0, 100, weight_defaults[key])
    total_weight += weights[key]

# Normalize weights to sum to 100 if they don't already
if total_weight != 100:
    factor = 100 / total_weight
    weights = {key: round(value * factor) for key, value in weights.items()}

# Dummy Data for Expansion Scores
data = {
    "Country": countries,
    "Market Size": [1.0, 0.1, 0.004, 0.0428, 0.4, 0.0933, 0.0333, 0.0007, 0.0023, 0.0127, 0.0002, 0.0004],
    "Willingness to Pay": [0.62, 1.00, 0.88, 0.79, 0.76, 0.83, 0.33, 0.43, 0.42, 0.45, 0.78, 0.45],
    "Sustainability": [64.08, 84.92, 51.91, 49.71, 79.92, 67.09, 62.65, 38.56, 31.83, 34.03, 40.88, 39.59],
    "Tariff & Shipping": [62.2, 66.7, 58.9, 58.9, 58.9, 61.3, 62.6, 33.3, 67.4, 72.1, 53.3, 38.5], 
    "Seasonality": [0.33, 0.62, 0.39, 0.38, 0.4, 0.38, 0.66, 0.66, 0.69, 0.64, 0.63, 0.62]
}

df = pd.DataFrame(data)

# Compute expansion score
df["Final Score"] = (
    weights["Market Size"] * df["Market Size"] +
    weights["Willingness to Pay"] * df["Willingness to Pay"] +
    weights["Sustainability & Customization"] * (df["Sustainability"] / 100) +
    weights["Tariff & Shipping"] * (df["Tariff & Shipping"] / 100) +
    weights["Seasonality"] * (df["Seasonality"] / 100)
)

df = df.round(3)

# Display Data
st.title("Sleek Garments Expansion Score Dashboard")
st.write("Adjust the weights in the sidebar and view the updated scores below.")
st.dataframe(df)

# Plotly Visualization
fig = px.bar(df, x="Final Score", y="Country", orientation='h', title="Final Expansion Scores",
             text=df["Final Score"], color=df["Final Score"], color_continuous_scale="blues")
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig)
