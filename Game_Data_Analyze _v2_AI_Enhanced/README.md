# 🚀 AI-Enhanced Game Analytics Dashboard (V2)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-orange.svg)
![Status](https://img.shields.io/badge/Status-Predictive-success.svg)

> **Advanced Version:** This project builds upon the standard analytics framework by integrating **Machine Learning pipelines** and **Simulated LLM logic** to provide predictive and prescriptive insights.

---

## 🎯 Key Capabilities

Unlike the V1 (Standard) version which focuses on *historical data* ("What happened?"), this AI-Enhanced version focuses on **prediction and segmentation** ("What will happen?").

### 1. 🤖 AI-Driven User Segmentation (Clustering)
* **Tech Stack:** K-Means Clustering (Scikit-Learn).
* **Function:** Automatically groups players into **5 distinct personas** based on behavior (e.g., playtime, spend, session frequency) rather than simple rule-based grouping.
* **AI Tagging:** Integrates an **Offline LLM Mapping** layer (`ai_persona.py`) to assign semantic, business-friendly labels to clusters:
    * 🐳 **Whales:** High spenders.
    * ⚔️ **Grinders:** High activity, low spend.
    * ⚠️ **Risk:** Low engagement patterns.

### 2. 🔮 Predictive Churn Analytics
* **Tech Stack:** Logistic Regression.
* **Function:** Calculates a real-time **Churn Probability Score (0-1)** for every active player.
* **Actionable Insight:** Identifies a "High Risk Cohort" (players likely to leave in 7 days) and visualizes the risk distribution, enabling proactive retention campaigns.

### 3. 💡 Automated Smart Insights (NLG)
* **Tech Stack:** Rule-Based Natural Language Generation.
* **Function:** Simulates an AI analyst by dynamically generating text summaries based on the filtered dataset. It provides instant context on engagement and monetization health without API latency.

---

## 🏗️ Technical Architecture

This project adopts a **"Hybrid AI Architecture"** optimized for production performance and data privacy:

* **Pre-computation Pipeline (`data_loader.py`):** ML models (Clustering & Prediction) run immediately upon data loading. This ensures that filtering and interaction are instantaneous (0ms latency).
* **Offline Inference:** Instead of calling external LLM APIs (like GPT-4) in real-time, logic is encapsulated locally. This ensures:
    * 🔒 **GDPR Compliance:** No user data leaves the local environment.
    * ⚡ **Performance:** No network latency.
    * 💰 **Cost Efficiency:** Zero API operational costs.

---

## 📂 Project Structure

```text
  Game_Data_Analyze_v2_AI_Enhanced/
  ├── data/                       # Dataset files
  │   ├── gaming_data_cleaned.csv
  │   └── ...
  ├── src/                        # Source Code
  │   ├── app.py                  # Main Application Entry
  │   ├── data_loader.py          # AI Pipeline (Clustering + Prediction)
  │   ├── ai_persona.py           # AI Tagging Logic
  │   ├── clustering.py           # 3D Visualization Module
  │   ├── prediction.py           # Churn Risk Module
  │   └── ...
  └── requirements.txt            # Dependencies
```
---

🚀 How to Run
1.Navigate to the source directory: (Important: The app must be run from the src folder)

```bash
cd src
```
2.Run the Streamlit App:

```bash
streamlit run app.py
```

3.Explore the AI Modules:
- Go to the Sidebar.

- Select "Cluster Analysis" to view the 3D Persona map.

- Select "Predictive Modeling" to view the Churn Risk predictions.

---

📊 Methodology Details
Feature,Method,Features Used
Segmentation,K-Means (k=5),"Age, Sessions/Week, PlayerLevel, Spend"
Churn Prediction,Logistic Regression,"Sessions/Week (Target), Age, Level, Spend"
Persona Naming,Dictionary Mapping,Derived from Cluster Centroid Analysis

