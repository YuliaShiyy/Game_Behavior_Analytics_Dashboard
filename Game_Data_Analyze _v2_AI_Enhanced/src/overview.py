# @Author : Yulia
# @File   : overview.py
# @Time   : 2025/9/6

import streamlit as st
import plotly.express as px


def render_smart_insights(df):
    """
    Rule-based NLG (Natural Language Generation) insights dashboard,
    automatically generating conclusions based on the currently filtered data.
    """
    if df.empty:
        return

    st.markdown("### 💡 AI Smart Insights")

    # 1. Prepare data indicators
    avg_session = df["SessionsPerWeek"].mean()
    pay_rate = df["InGamePurchases"].mean()
    total_users = len(df)

    # Check if there is any risk data predicted by AI.
    if "Risk_Level" in df.columns:
        high_risk_count = len(df[df["Risk_Level"] == "High Risk 🔴"])
        risk_ratio = high_risk_count / total_users if total_users > 0 else 0
    else:
        high_risk_count = 0
        risk_ratio = 0

    insights = []

    # 2. Rule-Based Logic

    # -- A. Activity Insights --
    if avg_session >= 5:
        insights.append(
            f"🚀 **High Engagement:** The selected user group is highly active, averaging **{avg_session:.1f} sessions/week**.")
    elif avg_session < 2:
        insights.append(
            f"⚠️ **Engagement Alert:** Activity is low (**{avg_session:.1f} sessions/week**). Re-engagement campaigns recommended.")
    else:
        insights.append(
            f"ℹ️ **Stable Activity:** User engagement is within normal range (**{avg_session:.1f} sessions/week**).")

    # -- B. Commercialization Insights--
    if pay_rate > 0.2:  # Assuming a 20% paying rate is very high
        insights.append(f"💰 **Strong Monetization:** **{pay_rate:.1%}** of these players are making purchases.")
    elif pay_rate > 0:
        insights.append(f"💳 **Monetization:** Paying user rate is **{pay_rate:.1%}**.")
    else:
        insights.append("📉 **Non-Spenders:** No purchases detected in this segment.")

    # -- C. AI attrition warning--
    if risk_ratio > 0.15:
        insights.append(
            f"🚨 **Churn Risk Warning:** Our predictive model flagged **{high_risk_count} users ({risk_ratio:.1%})** as 'High Risk'. Immediate action required.")
    elif risk_ratio > 0:
        insights.append(f"✅ **Retention Health:** Only {risk_ratio:.1%} of users are flagged as high risk.")

    # 3. Render panel (using the Info box)
    for msg in insights:
        st.info(msg)

    st.divider()


def render_overview(filtered_data, selected_region, render=True):
    """
    Render overview page
    """
    if render:
        # 1. First, demonstrate intelligent insights.
        render_smart_insights(filtered_data)
        st.subheader("🧭 Data Overview")

    # Calculate basic indicators
    metrics = {
        "Total number of players": len(filtered_data),
        "Average age": round(filtered_data["Age"].mean(), 1),
        "Proportion of paying players": f"{filtered_data['InGamePurchases'].mean() * 100:.1f}%",
        "Average number of sessions": round(filtered_data["SessionsPerWeek"].mean(), 1),
        "Proportion of highly engaged players": f"{(filtered_data['EngagementLevel'] == 'High').mean() * 100:.1f}%" if 'EngagementLevel' in filtered_data.columns else "N/A"
    }

    # Generate figures
    fig_location = px.histogram(filtered_data, x="Location", title=f"Geography ({selected_region})", text_auto=True)
    fig_age = px.histogram(filtered_data, x="Age", nbins=20, title="Age Distribution")
    fig_gender = px.pie(filtered_data, names="Gender", title="Gender Distribution")
    fig_sessions = px.histogram(filtered_data, x="SessionsPerWeek", title="Weekly Sessions Distribution")

    # Compatibility check: Some columns may not exist.
    figs = {
        "Geography": fig_location,
        "Age": fig_age,
        "Gender": fig_gender,
        "Weekly Sessions": fig_sessions
    }

    if "EngagementLevel" in filtered_data.columns:
        fig_engagement = px.pie(filtered_data, names="EngagementLevel", title="Engagement Level")
        figs["Engagement Level"] = fig_engagement
    else:
        fig_engagement = None

    if "PlayerLevel" in filtered_data.columns:
        fig_purchase = px.histogram(filtered_data, x="PlayerLevel", color="InGamePurchases",
                                    barmode="group", title="Paying Players by Level")
        figs["Level vs Payment"] = fig_purchase
    else:
        fig_purchase = None

    if "GameGenre" in filtered_data.columns:
        fig_genre_purchase = px.histogram(filtered_data, x="GameGenre", color="InGamePurchases",
                                          barmode="group", title="Paying Players by Game Type")
        figs["Genre vs Payment"] = fig_genre_purchase
    else:
        fig_genre_purchase = None

    if render:
        # Rendering Metrics Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Players", metrics["Total number of players"])
        col2.metric("Avg Age", metrics["Average age"])
        col3.metric("Paying Rate", metrics["Proportion of paying players"])
        col4.metric("Avg Sessions", metrics["Average number of sessions"])
        col5.metric("High Engagement", metrics["Proportion of highly engaged players"])

        st.divider()

        # Rendering charts
        st.plotly_chart(fig_location, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_age, use_container_width=True)
        with c2:
            st.plotly_chart(fig_gender, use_container_width=True)

        st.plotly_chart(fig_sessions, use_container_width=True)

        if fig_engagement: st.plotly_chart(fig_engagement, use_container_width=True)

        c3, c4 = st.columns(2)
        if fig_purchase:
            with c3: st.plotly_chart(fig_purchase, use_container_width=True)
        if fig_genre_purchase:
            with c4: st.plotly_chart(fig_genre_purchase, use_container_width=True)

    return metrics, figs