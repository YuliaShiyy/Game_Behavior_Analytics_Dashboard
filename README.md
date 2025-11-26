# 🎮 Game Player Behavior Analytics Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![Status](https://img.shields.io/badge/Status-Project%20Complete-green)

> **A full-stack data analytics platform enabling Game Studios to understand player lifecycles, improving retention through Descriptive Analytics and Predictive AI.**

---

## 📖 Project Evolution Story

This repository demonstrates the evolution of a data science project from **Foundational Analytics** to **Advanced AI Implementation**. It is structured into two versions to showcase different levels of data maturity:

### 🚀 [V2: AI-Enhanced Version (Recommended)](./Game_Data_Analyze_v2_AI_Enhanced)
> *Focus: Predictive & Prescriptive Analytics ("What will happen?")*

* **Core Tech:** Machine Learning (K-Means, Logistic Regression), Rule-Based NLG.
* **Key Features:**
    * 🤖 **AI Segmentation:** Groups players into 5 personas (e.g., *Whales, Grinders*) using Clustering.
    * 🔮 **Churn Prediction:** Estimates the probability of user churn in real-time.
    * 💡 **Smart Insights:** Auto-generates business insights without API latency.
* **Architecture:** Hybrid Offline-AI pipeline for GDPR compliance and zero-latency performance.

### 📊 [V1: Standard Version](./Game_Data_Analyze_v1)
> *Focus: Descriptive Analytics ("What happened?")*

* **Core Tech:** Statistical Analysis (SciPy), Plotly.
* **Key Features:**
    * 📈 **Retention Funnels:** Visualizes user drop-off rates (Day 1/7/30).
    * 🔗 **Correlation Analysis:** Statistical testing of player behaviors.
    * 📉 **Trend Simulation:** Historical data visualization.

---

## 📂 Repository Structure

```text
Game_Behavior_Analytics/
│
├── 📂 Game_Data_Analyze_v2_AI_Enhanced/  <-- 🌟 Start Here!
│   ├── src/             # Streamlit App & AI Models
│   ├── data/            # Datasets
│   └── README.md        # Detailed Documentation for V2
│
├── 📂 Game_Data_Analyze_v1/              <-- Legacy Version
│   ├── src/             # Streamlit App & Statistical Modules
│   ├── data/            # Datasets
│   └── README.md        # Detailed Documentation for V1
│
└── README.md            # You are here
```
---

## 🛠️ Tech Stack & Skills Demonstrated
| Category | Technologies / Skills |
| :--- | :--- |
| **Language** | Python 3.9+ |
| **Web Framework** | Streamlit (Component-based architecture) |
| **Machine Learning** | Scikit-Learn (K-Means, Logistic Regression) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly Interactive Charts |
| **Engineering** | Modular Design, Offline Inference, GDPR-Aware Architecture |

---

## 🚀 Quick Start
To run the latest AI-Enhanced version:
1.Clone the repo:
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
```
2.Install dependencies:
```bash
pip install -r Game_Data_Analyze_v2_AI_Enhanced/requirements.txt
```
3.Run the app:
```bash
cd Game_Data_Analyze_v2_AI_Enhanced/src
streamlit run app.py
```
