# @Author : Yulia
# @File   : app.py
# @Time   : 2025/9/6

import streamlit as st
from data_loader import load_data, filter_data
from overview import render_overview
from retention import render_retention_funnel
from simulation_trend import render_trend
from correlation import render_correlation
from clustering import render_clustering
from prediction import render_prediction
from report_export import export_full_report

# Page Setting
st.set_page_config(page_title="AI-Enhanced Game Analytics Dashboard", layout="wide", page_icon="🎮")

# =====================
# 1. Load Data (Backend AI Processing happens here)
# =====================
with st.spinner("Loading data and running AI models..."):
    df, df_europe = load_data()

# =====================
# 2. Sidebar Controls
# =====================
st.sidebar.header("🌍 Filters")

# Region Filter
all_regions = df['Location'].unique().tolist() if 'Location' in df.columns else []
selected_region = st.sidebar.selectbox("Select Region", ["Global"] + all_regions)

# Game Type Filter
all_genres = df["GameGenre"].unique() if 'GameGenre' in df.columns else []
genres = st.sidebar.multiselect("Select Game Type", all_genres)

# Gender Filter
all_genders = df["Gender"].unique() if 'Gender' in df.columns else []
genders = st.sidebar.multiselect("Select Gender", all_genders)

# Purchase Filter
purchase_filter = st.sidebar.selectbox("Paid or Not", ["All", "Paid players", "Not-paid players"])

# Navigation
st.sidebar.markdown("---")
section = st.sidebar.radio(
    "📑 Module Navigation",
    ["Overview",
     "Retention & Funnel",
     "Simulated Trend",
     "Correlation Analysis",
     "Cluster Analysis",
     "Predictive Modeling"],
    index=0
)

# =====================
# 3. Filter Data
# =====================
filtered_data = filter_data(df, selected_region, genres, genders, purchase_filter)

if len(filtered_data) == 0:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    st.stop()

# =====================
# 4. Main Content Rendering
# =====================
st.title("🎮 AI-Enhanced Player Behavior Analytics")
st.markdown(f"**Current View:** {section} | **Players Selected:** {len(filtered_data)}")

# Initialize variables for report export
metrics = None
all_figs = {}
results_df = None
model_acc = None

# --- Routing ---

if section == "Overview":
    metrics, figs_overview = render_overview(filtered_data, selected_region)
    all_figs.update(figs_overview)

elif section == "Retention & Funnel":
    fig_ret, fig_fun = render_retention_funnel(filtered_data)
    if fig_ret: all_figs["Retention Rate"] = fig_ret
    if fig_fun: all_figs["Funnel Analysis"] = fig_fun

elif section == "Simulated Trend":
    fig_new, fig_pay, fig_sess = render_trend(filtered_data)
    if fig_new: all_figs["New Players Trend"] = fig_new
    if fig_pay: all_figs["Paying Players Trend"] = fig_pay
    if fig_sess: all_figs["Session Trend"] = fig_sess

elif section == "Correlation Analysis":
    results_df, fig_corr, fig_scat, fig_box = render_correlation(filtered_data)
    if fig_corr: all_figs["Correlation Heatmap"] = fig_corr
    if fig_scat: all_figs["Correlation Scatter"] = fig_scat
    if fig_box: all_figs["Correlation Boxplot"] = fig_box

elif section == "Cluster Analysis":
    # Note: This is adapted to the new return value of clustering.py.
    fig_cluster, cluster_summary = render_clustering(filtered_data)
    if fig_cluster: all_figs["AI Cluster 3D Plot"] = fig_cluster
    # cluster_summary 是 DataFrame，可以在报告中单独处理，这里暂不放入 figs

elif section == "Predictive Modeling":
    # Note: This is adapted to the new return value of prediction.py.
    acc, fig_churn_dist = render_prediction(filtered_data)
    model_acc = acc
    if fig_churn_dist: all_figs["Churn Risk Distribution"] = fig_churn_dist

# =====================
# 5. Report Export Logic
# =====================
st.sidebar.markdown("---")
st.sidebar.header("📥 Export Report")

# Let user choose charts
if all_figs:
    selected_charts = st.sidebar.multiselect(
        "Select charts to include:",
        list(all_figs.keys()),
        default=list(all_figs.keys())
    )

    if st.sidebar.button("📄 Generate PDF Report"):
        with st.spinner("Generating PDF..."):
            pdf_data = export_full_report(metrics, results_df, all_figs, model_acc, selected_charts)

        st.sidebar.success("Report Ready!")
        st.sidebar.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name=f"Game_Analytics_Report_{section}.pdf",
            mime="application/pdf"
        )
else:
    st.sidebar.info("Navigate to a module to generate charts for export.")