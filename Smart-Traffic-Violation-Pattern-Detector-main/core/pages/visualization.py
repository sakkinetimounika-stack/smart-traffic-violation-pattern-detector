from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px
from core.visualization import _light_layout, PLOTLY_TEMPLATE
from core.analysis import apply_filters, predict_risk_clusters

def render_visualization_page(df: pd.DataFrame) -> None:
    st.title("📊 Data Visualization")
    st.markdown("Deep dive into traffic violation patterns using interactive charts. Select independent dates and states for each graph section below.")
    
    # Custom CSS to highlight the selection areas gracefully
    st.markdown("""
        <style>
        [data-testid="stDateInput"], [data-testid="stSelectbox"] {
            background: var(--background-color) !important;
            padding: 0.85rem 1.25rem;
            border-radius: 16px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-left: 5px solid color-mix(in srgb, var(--primary-color) 80%, var(--text-color));
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.06);
            margin-bottom: 0.75rem;
        }
        [data-testid="stDateInput"] label p, [data-testid="stSelectbox"] label p {
            color: var(--text-color) !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.01em;
        }
        </style>
    """, unsafe_allow_html=True)

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    states = sorted(df["location"].dropna().unique().tolist())

    def get_filters(key_prefix: str, show_state: bool = False):
        col1, col2 = st.columns([1, 1])
        with col1:
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key=f"{key_prefix}_date"
            )
            start_d, end_d = (date_range[0], date_range[1]) if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)
        
        selected_state = "All States"
        if show_state:
            with col2:
                selected_state = st.selectbox(
                    "Select State (India)", 
                    ["All States"] + states, 
                    key=f"{key_prefix}_state"
                )
        
        return start_d, end_d, selected_state

    # 1) Top 5 Location having the most violation
    st.markdown("### 1. Top 5 Locations with Most Violations")
    sd1, ed1, _ = get_filters("g1", show_state=False)
    df1 = df[(df["date"].dt.date >= sd1) & (df["date"].dt.date <= ed1)]
    if df1.empty:
        st.warning("No records for this date range.")
    else:
        loc_counts = df1.groupby("location").size().reset_index(name="count").sort_values("count", ascending=False).head(5)
        fig1 = px.bar(
            loc_counts,
            x="location",
            y="count",
            color="count",
            color_continuous_scale="Viridis",
            labels={"location": "State", "count": "Violation Count"},
            title=f"Top 5 States ({sd1} to {ed1})"
        )
        st.plotly_chart(_light_layout(fig1), use_container_width=True)

    # 2) A bar graph plotting against violation type and number of violations
    st.markdown("---")
    st.markdown("### 2. Violations by Type")
    sd2, ed2, state2 = get_filters("g2", show_state=True)
    df2 = df[(df["date"].dt.date >= sd2) & (df["date"].dt.date <= ed2)]
    if state2 != "All States":
        df2 = df2[df2["location"] == state2]
    if df2.empty:
        st.warning("No records found.")
    else:
        v_counts2 = df2.groupby("violation_type").size().reset_index(name="count").sort_values("count", ascending=False)
        fig2 = px.bar(
            v_counts2,
            x="violation_type",
            y="count",
            color="violation_type",
            title=f"Violation Distribution: {state2}",
            labels={"violation_type": "Type", "count": "Count"}
        )
        st.plotly_chart(_light_layout(fig2), use_container_width=True)

    # 3) A pie chart showing the percentage of each violation
    st.markdown("---")
    st.markdown("### 3. Violation Percentage")
    sd3, ed3, state3 = get_filters("g3", show_state=True)
    df3 = df[(df["date"].dt.date >= sd3) & (df["date"].dt.date <= ed3)]
    if state3 != "All States":
        df3 = df3[df3["location"] == state3]
    if df3.empty:
        st.warning("No records found.")
    else:
        v_counts3 = df3.groupby("violation_type").size().reset_index(name="count")
        fig3 = px.pie(
            v_counts3,
            names="violation_type",
            values="count",
            title=f"Category Split: {state3}",
            hole=0.4
        )
        fig3.update_traces(textinfo="percent+label")
        st.plotly_chart(_light_layout(fig3), use_container_width=True)

    # 4) Provide a graph plotting against number of age groups v/s risk level (high, medium, low)
    st.markdown("---")
    st.markdown("### 4. Age Group vs Risk Level")
    sd4, ed4, _ = get_filters("g4", show_state=False)
    df4 = df[(df["date"].dt.date >= sd4) & (df["date"].dt.date <= ed4)].copy()
    if df4.empty:
        st.warning("No records found.")
    else:
        risk_df = predict_risk_clusters(df) 
        risk_map = dict(zip(risk_df["location"], risk_df["risk_level"]))
        df4["risk_level"] = df4["location"].map(risk_map).fillna("Low")
        age_bins = [0, 18, 25, 40, 60, 100]
        age_labels = ["<18", "18-25", "26-40", "41-60", "60+"]
        df4["age_group"] = pd.cut(df4["Driver_Age"], bins=age_bins, labels=age_labels)
        age_risk = df4.groupby(["age_group", "risk_level"], observed=True).size().reset_index(name="count")
        fig4 = px.bar(
            age_risk,
            x="age_group",
            y="count",
            color="risk_level",
            barmode="group",
            title="Risk Level Profile Across Age Groups",
            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
        )
        st.plotly_chart(_light_layout(fig4), use_container_width=True)

    # 5) Horizontal bar graph: Road types v/s number of over speed count
    st.markdown("---")
    st.markdown("### 5. Over-speeding by Road Condition")
    sd5, ed5, state5 = get_filters("g5", show_state=True)
    df5 = df[(df["date"].dt.date >= sd5) & (df["date"].dt.date <= ed5)].copy()
    if state5 != "All States":
        df5 = df5[df5["location"] == state5]
    os_df = df5[df5["violation_type"].str.contains("speeding", case=False, na=False)].copy()
    
    if os_df.empty:
        st.info("No over-speeding incidents found.")
    else:
        road_mapping = {
            "Potholes": "pothole",
            "Under Construction": "1line road",
            "Slippery": "2 lineroad",
            "Wet": "3 line road",
            "Dry": "Normal road"
        }
        os_df["road_type_mapped"] = os_df["Road_Condition"].map(road_mapping).fillna("Other")
        road_os = os_df.groupby("road_type_mapped").size().reset_index(name="count").sort_values("count", ascending=True)
        fig5 = px.bar(
            road_os,
            y="road_type_mapped",
            x="count",
            orientation='h',
            color="count",
            color_continuous_scale="Reds",
            title=f"Over-speeding Intensity: {state5}",
            labels={"road_type_mapped": "Road Conditions", "count": "Incident Count"}
        )
        st.plotly_chart(_light_layout(fig5), use_container_width=True)

