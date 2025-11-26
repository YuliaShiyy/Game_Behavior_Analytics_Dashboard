# 📊 Standard Game Analytics Dashboard (V1)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-green.svg)
![Status](https://img.shields.io/badge/Status-Descriptive-success.svg)

> **Foundational Version:** This project establishes a robust framework for **Descriptive Analytics**, focusing on visualizing historical player behavior, retention rates, and conversion funnels.

---

## 🎯 Key Capabilities

This version addresses the core question: **"What happened in the past?"**. It provides essential KPIs for game operation monitoring.

### 1. 📈 Retention & Funnel Analysis
* **Retention:** Visualizes player stickiness using classic Day 1, Day 7, and Day 30 retention metrics.
* **Conversion Funnel:** Tracks the user journey from *Total Players* → *Active Users* → *Highly Engaged* → *Paying Users*.
* **Business Value:** Helps identify where players drop off in the lifecycle.

### 2. 🗓️ Simulated Trend Analysis
* **Time-Series Visualization:** Generates simulated monthly trends for:
    * New Player Acquisition.
    * Revenue (Paying Players).
    * Engagement (Average Sessions).
* **Function:** Allows analysts to observe seasonal patterns and growth trajectories.

### 3. 🔗 Statistical Correlation
* **Tech Stack:** Pearson & Spearman Correlation (SciPy).
* **Function:** A heatmap and scatter plot module to analyze relationships between variables (e.g., *"Does higher Age correlate with higher Spend?"*).
* **Significance Test:** Includes P-value testing to ensure statistical validity.

---

## 📂 Project Structure

```text
    Game_Data_Analyze/
    │── data/                                     # Datasets
    │ ├── gaming_data_cleaned.csv
    │ ├── gaming_data_europe.csv
    │ └── online_gaming_behavior_dataset.csv
    │
    │── notebooks/                                # Jupyter notebooks
    │ └── data_clean.ipynb
    │
    │── src/                                      # Source code
    │ ├── app.py                                  # Main dashboard entry
    │ ├── clustering.py                           # Cluster analysis module
    │ ├── correlation.py                          # Correlation analysis module
    │ ├── data_loader.py                          # Data loading & preprocessing
    │ ├── overview.py                             # Overview module
    │ ├── prediction.py                           # Predictive modeling
    │ ├── report_export.py                        # Export to PDF
    │ ├── retention.py                            # Retention & funnel analysis
    │ └── simulation_trend.py                     # Trend simulation
    │
    │── requirements.txt                          # Dependencies
    └── README.md                                 # Project documentation
```
---

## ⚡ Installation

Clone this repo and install dependencies:

    ```bash
    git clone https://github.com/YuliaShiyy/Game_Data_Analyze.git
    cd Game_Data_Analyze
    pip install -r requirements.txt
---

## 🚀 How to Run

1.Navigate to the source directory: (Important: The app must be run from the src folder)
```bash
    streamlit run app.py
```
2.Run the Streamlit App:
```bash
streamlit run app.py
```
3.Explore the Modules:

- Go to the Sidebar.

- Select "Retention & Funnel" to view lifecycle metrics.

- Select "Correlation Analysis" to view statistical heatmaps.

--- 

📊 Methodology Details
| Metric | Definition | Logic Used |
| :--- | :--- | :--- |
| **Day 1 Retention** | Users playing ≥1 session/week | `Sessions >= 1` |
| **Day 7 Retention** | Users playing ≥2 sessions/week | `Sessions >= 2` |
| **Conversion Funnel** | Step-by-step user drop-off | Count(Total) → Count(Active) → Count(Paid) |
| **Correlation** | Linear relationship strength | Pearson Coefficient (r) + P-value |

---

## 📂 Data

Dataset used: Kaggle - Predict Online Gaming Behaviour Dataset
.
For demo purposes, pre-cleaned datasets are placed in the data/ folder.

---

## 📌 To Do / Possible Extensions

    · Add time-series forecasting for player retention
    
    · Deploy the dashboard online (e.g., Streamlit Cloud / Heroku)
    
    · Add more machine learning models (e.g., Random Forest, XGBoost)
    
    · Multi-language support 
