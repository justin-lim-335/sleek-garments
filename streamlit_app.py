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
    "Sustainability & Customization": 10,
    "Seasonality": 10
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
# Uniform type selection
uniform_type = st.radio("Select Uniform Type:", ["Security", "Medical", "School"])

# Dummy Data for Expansion Scores
data = {
    "Country": countries,
    "Market Size - Security": [1.0, 0.1, 0.004, 0.0428, 0.4, 0.0933, 0.0333, 0.0007, 0.0023, 0.0127, 0.0002, 0.0004],
    "Market Size - Medical": [0.8, 0.2, 0.005, 0.038, 0.35, 0.1, 0.03, 0.0005, 0.002, 0.01, 0.00015, 0.0003],
    "Market Size - School": [0.9, 0.15, 0.006, 0.04, 0.37, 0.11, 0.032, 0.0006, 0.0021, 0.011, 0.00018, 0.00035],
    "Willingness - Security": [0.62, 1.00, 0.88, 0.79, 0.76, 0.83, 0.33, 0.43, 0.42, 0.45, 0.78, 0.45],
    "Willingness - Medical": [0.6, 0.98, 0.85, 0.75, 0.72, 0.8, 0.31, 0.4, 0.39, 0.43, 0.75, 0.42],
    "Willingness - School": [0.65, 1.02, 0.9, 0.82, 0.78, 0.85, 0.35, 0.45, 0.44, 0.48, 0.8, 0.48],
    "Sustainability": [64.08, 84.92, 51.91, 49.71, 79.92, 67.09, 62.65, 38.56, 31.83, 34.03, 40.88, 39.59],
    "Tariff & Shipping": [62.2, 66.7, 58.9, 58.9, 58.9, 61.3, 62.6, 33.3, 67.4, 72.1, 53.3, 38.5], 
    "Seasonality": [0.33, 0.62, 0.39, 0.38, 0.4, 0.38, 0.66, 0.66, 0.69, 0.64, 0.63, 0.62]
}

df = pd.DataFrame(data)

# Dynamically set the columns based on user selection
market_size_col = f"Market Size - {uniform_type}"
willingness_col = f"Willingness - {uniform_type}"

# Compute weighted contributions
df["Market Size Score"] = weights["Market Size"] * df[market_size_col]
df["Willingness Score"] = weights["Willingness to Pay"] * df[willingness_col]
df["Sustainability Score"] = weights["Sustainability & Customization"] * (df["Sustainability"] / 100)
df["Tariff Score"] = weights["Tariff & Shipping"] * (df["Tariff & Shipping"] / 100)
df["Seasonality Score"] = weights["Seasonality"] * (df["Seasonality"] / 100)

# Compute final score
df["Final Score"] = (
    df["Market Size Score"] +
    df["Willingness Score"] +
    df["Sustainability Score"] +
    df["Tariff Score"] +
    df["Seasonality Score"]
)

df = df.round(3)

# Melt DataFrame for stacked bar chart
df_melted = df.melt(id_vars=["Country"], 
                    value_vars=["Market Size Score", "Willingness Score", "Sustainability Score", 
                                "Tariff Score", "Seasonality Score"],
                    var_name="Factor", 
                    value_name="Score")

# Display Data
st.title("Sleek Garments Expansion Score Dashboard")
st.write("Adjust the weights in the sidebar and select a uniform type to view the updated scores.")
st.dataframe(df)

# Plotly Stacked Bar Chart
fig = px.bar(df_melted, 
             x="Score", 
             y="Country", 
             color="Factor", 
             orientation='h', 
             title=f"Final Expansion Scores Breakdown - {uniform_type} Uniforms",
             text_auto=True, 
             barmode="stack",
             color_discrete_map={
                 "Market Size Score": "blue",
                 "Willingness Score": "green",
                 "Sustainability Score": "orange",
                 "Tariff Score": "red",
                 "Seasonality Score": "purple"
             })

fig.update_layout(yaxis=dict(categoryorder='total ascending'))
st.plotly_chart(fig)