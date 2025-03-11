import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

# Initialize default weights
weight_defaults = {
    "Market Size": 30,
    "Tariff & Shipping": 20,
    "Willingness": 30,
    "Sustainability & Customization": 10,
    "Seasonality": 10
}

# Initialize default dataframe
df_provided = pd.DataFrame({
        "Country": ["USA", "UK", "Denmark", "Netherlands", "Germany", "France", "South Africa",
                    "Botswana", "Nigeria", "Kenya", "Bahamas", "Guyana"],
        "Market Size - Security": [1, 0.178, 0.004, 0.036, 0.289, 0.203, 0.667, 0.003, 0.922, 0.444, 0.002, 0.003],
        "Market Size - Medical": [1, 0.1, 0.004, 0.043, 0.4, 0.093, 0.033, 0.001, 0.002, 0.013, 0, 0],
        "Market Size - School": [0.371, 0.257, 0, 0, 0.006, 0.003, 0.286, 0.014, 1, 0.429, 0.001, 0.005],
        "Willingness - Security": [0.8, 0.64, 0.82, 0.74, 0.72, 0.83, 0.52, 0.68, 0.33, 0.34, 1, 0.58],
        "Willingness - Medical": [0.62, 1, 0.88, 0.79, 0.76, 0.83, 0.33, 0.43, 0.42, 0.45, 0.78, 0.45],
        "Willingness - School": [0.8, 0.69, 0.78, 0.7, 0.68, 0.71, 0.42, 0.59, 0.39, 0.42, 1, 0.58],
        "Sustainability & Customization": [0.64, 0.85, 0.52, 0.50, 0.80, 0.67, 0.63, 0.39, 0.32, 0.34, 0.41, 0.40],
        "Tariff & Shipping": [0.62, 0.67, 0.59, 0.59, 0.59, 0.61, 0.63, 0.33, 0.67, 0.72, 0.53, 0.39], 
        "Seasonality": [0.33, 0.62, 0.39, 0.38, 0.4, 0.38, 0.66, 0.66, 0.69, 0.64, 0.63, 0.62]
    })

# Create tool description
st.sidebar.subheader("Instructions")
st.sidebar.text("To use this tool, first select what market data to use. You have the option to use either the original dataset from this project or one of your own. *Note: Please ensure the format is the same as the provided dataset or the tool will not analyze what you upload.")
st.sidebar.text("Once a data source is chosen, you have the option to choose what clothing markets to analyze and in what display type to view the data in (as a chart or as a dataset of calculated scores).")
st.sidebar.text("There is also a set of sliders that contribute to the calculation of the final score. Feel free to adjust these depending on how much they are valued within the overall score and the calculated values will adjust in kind. ")
st.sidebar.divider()
st.sidebar.subheader("Interpreting the Score")
st.sidebar.text("The 'expansion score' is a calculated value of all of the different performance metrics a given country performs in. Based on the selected market and assigned weights, the dashboard will display what the expansion scores look like under the specific filters and ranked ")
st.sidebar.divider()
st.sidebar.subheader("About the Tool")
st.sidebar.text("This dashboard tool was created for the Winter 2025 MS&E 108 Senior Project Class at Stanford University by students Daniel Bishop, Manpreet Kaur, and Justin Lim for the use of Ghanian-based company, Sleek Garments.")
st.sidebar.text("This site analyzes data/metrics about the global garments market and computes an expansion score dataset as a resource for the client, Sleek Garments, to help them determine the best countries to pursue on their goal to expand the range of their operations.")
st.sidebar.text("The original code, instructions, and information on data sources for this tool are all located in the corresponding github repository accessible at this link")

# Create tool title
st.title("Sleek Garments Expansion Score Dashboard")

# File upload option
data_option = st.radio("**Select Data Source**", ["Use Provided Data", "Upload CSV File"])

# File check
expected_columns = [
    "Country",
    "Market Size - Security", "Market Size - Medical", "Market Size - School",
    "Willingness - Security", "Willingness - Medical", "Willingness - School",
    "Sustainability & Customization", "Tariff & Shipping", "Seasonality"
]
def validate_uploaded_data(df):
    # Check if all expected columns are present
    if set(expected_columns) != set(df.columns):
        st.error("Uploaded file is invalid: Missing or extra columns detected.")
        return False

    # Check if all numeric values are between 0 and 1 (excluding 'Country' column)
    numeric_columns = [col for col in expected_columns if col != "Country"]
    if df[numeric_columns].isnull().any().any():
        st.error("Uploaded file contains missing values.")
        return False

    if ((df[numeric_columns] < 0) | (df[numeric_columns] > 1)).any().any():
        st.error("Uploaded file contains values outside the range [0,1].")
        return False

    # Ensure at least one row exists
    if df.shape[0] == 0:
        st.error("Uploaded file has no data.")
        return False

    return True

# If the user selects to upload their own file
uploaded_file = None
df = df_provided
if data_option == "Upload CSV File":
    with st.container(border=True):
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)

            if validate_uploaded_data(df_uploaded):
                df = df_uploaded
                st.success("Custom data loaded successfully!")
            else:
                st.warning("Reverting to provided data due to invalid upload.")

        except Exception as e:
            st.error(f"Error reading the file: {e}")
            st.warning("Reverting to provided data.")

# Display dataset in expander
expander = st.expander("View Data")
expander.dataframe(df)
expander.caption("Source: Uploaded file" if uploaded_file is not None else "Source: This data is from the original dataset this project was inspired by. It pulls from multiple publicly available sources, the details of which can be found in the 'About the Tool' section")

# Display currently used data source
if uploaded_file is not None & validate_uploaded_data(df_uploaded):
    data_source_text = f"<span style='color:#16AD43;'>{uploaded_file.name}</span>"
else:
    data_source_text = "<span style='color:#6F9CEB;'>Provided Data</span>"
st.markdown(f"Currently Using: {data_source_text}", unsafe_allow_html=True)

# Market Type Selection
uniform_type = "Security"
st.markdown("**Market Type**")
left, middle, right = st.columns(3)
if left.button("Security", use_container_width=True):
    uniform_type = "Security"
if middle.button("Medical", use_container_width=True):
    uniform_type = "Medical"
if right.button("School", use_container_width=True):
    uniform_type = "School"

# Sidebar sliders for weight adjustments
col1, col2 = st.columns([1, 4])
with col1:
    with st.container(border = True):
        st.markdown("**Adjust Weights**")
        weights = {}
        for key in weight_defaults:
            weights[key] = st.slider(key, 0, 100, weight_defaults[key])

# Remove Seasonality if not School
if uniform_type != "School":
    del weights["Seasonality"]  # Remove Seasonality weight
    total_weight = sum(weights.values())  # Sum of remaining weights
    weights = {key: round((value / total_weight) * 100) for key, value in weights.items()}  # Renormalize to 100

# Dynamically set the columns based on user selection
market_size_col = f"Market Size - {uniform_type}"
willingness_col = f"Willingness - {uniform_type}"

# Compute weighted contributions
df_scores = pd.DataFrame()
df_scores["Country"] = df["Country"]
df_scores["Market Size Score"] = weights["Market Size"] * df[market_size_col]
df_scores["Willingness Score"] = weights["Willingness"] * df[willingness_col]
df_scores["S&C Score"] = weights["Sustainability & Customization"] * (df["Sustainability & Customization"])
df_scores["Tariff Score"] = weights["Tariff & Shipping"] * (df["Tariff & Shipping"])

# Only include Seasonality if School is selected
if uniform_type == "School":
    df_scores["Seasonality Score"] = weights["Seasonality"] * df["Seasonality"]

# Compute final score
df_scores["Final Score"] = (
    df_scores["Market Size Score"] +
    df_scores["Willingness Score"] +
    df_scores["S&C Score"] +
    df_scores["Tariff Score"]
)

if uniform_type == "School":
    df_scores["Final Score"] += df_scores["Seasonality Score"]

# Round all numeric columns to one decimal place
df_scores.iloc[:, 1:] = df_scores.iloc[:, 1:].round(1)

# Melt DataFrame for stacked bar chart
melt_vars = ["Market Size Score", "Willingness Score", "S&C Score", "Tariff Score"]
if uniform_type == "School":
    melt_vars.append("Seasonality Score")

df_melted = df_scores.melt(id_vars=["Country"], 
                           value_vars=melt_vars,
                           var_name="Factor", 
                           value_name="Score")

# Create a separate DataFrame to store only total scores for display on the bars
df_total_scores = df_scores[["Country", "Final Score"]]

# Plotly Stacked Bar Chart
fig = px.bar(
    df_melted,
    x="Score",
    y="Country",
    color="Factor",
    orientation='h',
    barmode="stack",
    color_discrete_map={
        "Market Size Score": "#141B41",
        "Willingness Score": "#306BAC",
        "S&C Score": "#6F9CEB",
        "Tariff Score": "#98B9F2",
        "Seasonality Score": "#918EF4"
    },
    hover_data={"Score": True, "Factor": True, "Country": True},  # Ensure hover info remains
    text=None  # Disable automatic text on stacked sections
)

# Add only the Final Score as text annotations on the bars
for i, row in df_scores.iterrows():
    fig.add_annotation(
        x=row["Final Score"],  # Place text at the total score position
        y=row["Country"],
        text=str(round(row["Final Score"], 1)),  # Rounded total score
        showarrow=False,  # Hide arrows
        font=dict(size=14, color="white"),
        xanchor="left",  # Adjust placement to the right of the bar
        yanchor="middle"  # Adjust vertical placement
    )

# Ensure the categories stay sorted properly
fig.update_layout(yaxis=dict(categoryorder='total ascending'))

# Provide options for how to display
with col2: 
    tab1, tab2 = st.tabs(["Chart", "Table"])
    with tab1:
        st.subheader(f"Final Expansion Scores Breakdown - {uniform_type} Uniforms")    
        st.plotly_chart(fig)
    with tab2:
        st.subheader(f"Final Expansion Scores Breakdown - {uniform_type} Uniforms")
        st.dataframe(df_scores)