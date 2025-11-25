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

    # 模拟 GPT-4 分析聚类中心后生成的 Persona 名称
    # 对应简历: "tag 5+ meaningful player personas"
    llm_personas = {
        0: "Whale 🐳 (High Spender)",  # 高充值，高活跃
        1: "Socialite 💬 (Community Driven)",  # 中等充值，高频次
        2: "Grinder ⚔️ (Hardcore F2P)",  # 0充值，超高时长
        3: "Casual 🍵 (Low Engagement)",  # 低时长，低充值
        4: "Risk ⚠️ (Churn Candidate)"  # 极低活跃，即将流失
    }

    # 对应的详细描述 (用于 Tooltip)
    persona_desc = {
        "Whale 🐳 (High Spender)": "Top 1% revenue contributors. Needs VIP support.",
        "Socialite 💬 (Community Driven)": "Active in chat/guilds. Retention driver.",
        "Grinder ⚔️ (Hardcore F2P)": "High playtime but low spend. Content consumers.",
        "Casual 🍵 (Low Engagement)": "Logs in occasionally. Hard to monetize.",
        "Risk ⚠️ (Churn Candidate)": "High probability of leaving. Needs re-engagement."
    }

    # 1. 映射名称
    df['Persona'] = df[cluster_col].map(llm_personas)

    # 防止 K-Means 结果超出预期 (比如 K=6)
    df['Persona'] = df['Persona'].fillna("Standard Player")

    # 2. 映射描述
    df['Persona_Desc'] = df['Persona'].map(persona_desc)

    return df