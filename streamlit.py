import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration

st.set_page_config(
    page_title="Agricultural Monitoring",
    layout="wide"
)

st.title("Agricultural Monitoring Dashboard")
st.caption("Monitoring vegetation development across agricultural fields using PlanetScope NDVI data")

# Load and prepare data

@st.cache_data
def load_data():
    df = pd.read_csv("Analysis_PlanetScope_Sandbox_All - All data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["field_id", "date"])

    # Calculate change in NDVI for each field
    df["ndvi_change"] = (
        df.groupby("field_id")["mean"].diff()
    )

    return df

df = load_data()

# Sidebar filters

st.sidebar.header("Dashboard Filters")

available_fields = sorted(df["field_id"].unique())

selected_fields = st.sidebar.multiselect(
    "Select agricultural fields",
    available_fields,
    default=available_fields
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Observation period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

filtered_df = df[
    (df["field_id"].isin(selected_fields)) &
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date)
].copy()

if filtered_df.empty:
    st.warning("No observations found for the selected filters.")
    st.stop()

# Overview metrics

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Fields selected",
    filtered_df["field_id"].nunique()
)

col2.metric(
    "Observations",
    len(filtered_df)
)

col3.metric(
    "Average NDVI",
    f"{filtered_df['mean'].mean():.3f}"
)

col4.metric(
    "Highest NDVI",
    f"{filtered_df['mean'].max():.3f}"
)

# Interactive NDVI chart

st.subheader("Vegetation Development")

fig = px.line(
    filtered_df,
    x="date",
    y="mean",
    color="field_id",
    markers=True,
    hover_data=["min", "max", "median"],
    labels={
        "date": "Observation date",
        "mean": "Mean NDVI",
        "field_id": "Agricultural field"
    }
)

fig.update_layout(
    hovermode="x unified",
    legend_title="Field",
    yaxis_title="Mean NDVI",
    xaxis_title="Date"
)

st.plotly_chart(fig, width="stretch")

# Field-level analysis

st.subheader("Explore Individual Fields")

selected_field = st.selectbox(
    "Choose a field",
    sorted(filtered_df["field_id"].unique())
)

field_df = filtered_df[
    filtered_df["field_id"] == selected_field
].copy()

field_col1, field_col2, field_col3 = st.columns(3)

field_col1.metric(
    "Average NDVI",
    f"{field_df['mean'].mean():.3f}"
)

field_col2.metric(
    "Maximum NDVI",
    f"{field_df['mean'].max():.3f}"
)

field_col3.metric(
    "Minimum NDVI",
    f"{field_df['mean'].min():.3f}"
)

tab1, tab2, tab3 = st.tabs([
    "NDVI trend",
    "NDVI distribution",
    "Data quality"
])

with tab1:
    fig_field = px.line(
        field_df,
        x="date",
        y="mean",
        markers=True,
        title=f"NDVI Development — {selected_field}"
    )
    st.plotly_chart(fig_field, width="stretch")

with tab2:
    fig_dist = px.histogram(
        field_df,
        x="mean",
        nbins=20,
        title=f"NDVI Distribution — {selected_field}",
        labels={"mean": "Mean NDVI"}
    )
    st.plotly_chart(fig_dist, width="stretch")

with tab3:
    quality_columns = [
        col for col in [
            "cloudcoveragepercent",
            "samplecount",
            "nodatacount"
        ]
        if col in field_df.columns
    ]

    if quality_columns:
        st.dataframe(
            field_df[["date", "mean"] + quality_columns],
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No data quality columns were found in this dataset.")

# Unusual NDVI changes

st.subheader("Potentially Unusual Changes")

threshold = st.slider(
    "Flag observations with absolute NDVI change greater than",
    min_value=0.05,
    max_value=0.80,
    value=0.30,
    step=0.05
)

anomalies = filtered_df[
    filtered_df["ndvi_change"].abs() >= threshold
].copy()

st.caption(
    "These are statistical flags for further investigation, "
    "not confirmed agricultural events."
)

if anomalies.empty:
    st.info("No observations exceed the selected threshold.")
else:
    st.dataframe(
        anomalies[
            ["date", "field_id", "mean", "ndvi_change"]
        ].sort_values(
            "ndvi_change",
            key=lambda x: x.abs(),
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

# Download filtered data

st.subheader("Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered observations",
    data=csv,
    file_name="filtered_ndvi_observations.csv",
    mime="text/csv"
)
