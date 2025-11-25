# @Author : Yulia
# @File   : ai_persona.py
# @Time   : 2025/9/6

import pandas as pd


def apply_persona_tags(df, cluster_col='Cluster'):
    """
    Simulates Generative AI (LLM) tagging based on cluster centroids.
    Maps cluster IDs (0-4) to 5 meaningful personas as stated in the resume.
    """
    if cluster_col not in df.columns:
        return df

    # Persona names generated after simulating GPT-4 analysis of cluster centers
    llm_personas = {
        0: "Whale 🐳 (High Spender)",  # High recharge, high activity
        1: "Socialite 💬 (Community Driven)",  # Medium-sized top-ups, high-frequency top-ups
        2: "Grinder ⚔️ (Hardcore F2P)",  # 0 recharge, super long playtime
        3: "Casual 🍵 (Low Engagement)",  # Low duration, low recharge
        4: "Risk ⚠️ (Churn Candidate)"  # Extremely low activity, about to churn
    }

    # Detailed description of the corresponding tooltip (for tooltips)
    persona_desc = {
        "Whale 🐳 (High Spender)": "Top 1% revenue contributors. Needs VIP support.",
        "Socialite 💬 (Community Driven)": "Active in chat/guilds. Retention driver.",
        "Grinder ⚔️ (Hardcore F2P)": "High playtime but low spend. Content consumers.",
        "Casual 🍵 (Low Engagement)": "Logs in occasionally. Hard to monetize.",
        "Risk ⚠️ (Churn Candidate)": "High probability of leaving. Needs re-engagement."
    }

    # 1. Mapping name
    df['Persona'] = df[cluster_col].map(llm_personas)

    # To prevent K-Means results from exceeding expectations (e.g., K=6)
    df['Persona'] = df['Persona'].fillna("Standard Player")

    # 2. Mapping description
    df['Persona_Desc'] = df['Persona'].map(persona_desc)


    return df
