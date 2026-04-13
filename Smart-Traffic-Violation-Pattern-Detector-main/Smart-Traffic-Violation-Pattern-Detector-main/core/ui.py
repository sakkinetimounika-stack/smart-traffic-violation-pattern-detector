from __future__ import annotations

import pandas as pd
import streamlit as st

from core.app_config import METRIC_STYLES, NAV_ITEMS


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { color: var(--text-color); }
        .stApp * { box-sizing: border-box; }
        .block-container {
            padding-top: 1.45rem; padding-bottom: 2.1rem; margin-top: 3.5rem;
            max-width: 100% !important; padding-left: 2rem !important; padding-right: 2rem !important;
        }
        section[data-testid="stSidebar"] {
            background-color: var(--secondary-background-color) !important;
            border-right: 1px solid rgba(128, 128, 128, 0.2);
        }
        section[data-testid="stSidebar"] * { color: var(--text-color) !important; }
        [data-testid="stSidebarNav"] { display: none; }
        div[role="radiogroup"] > label { padding: 0.7rem 0.8rem; margin-bottom: 0.32rem; border-radius: 14px; }
        div[role="radiogroup"] > label:hover { background: rgba(128, 128, 128, 0.1); }
        div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child { display: none; }
        div[role="radiogroup"] label[data-baseweb="radio"] span { font-size: 1.02rem; font-weight: 600; }
        
        .status-card, section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background: var(--background-color); border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 18px; padding: 1rem; margin-top: 2rem;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] section { padding: 0.5rem; min-height: auto; }
        
        .topbar {
            display: flex; align-items: center; background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 22px;
            padding: 0.7rem 0.95rem 0.35rem 0.95rem; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); margin-bottom: 1rem;
        }
        .topbar .stTextInput, .topbar .stTextInput > div { width: 100%; }
        .topbar .stTextInput input {
            background: var(--background-color); border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 14px; color: var(--text-color) !important; font-size: 0.95rem; padding: 0.85rem 1rem;
        }
        
        .filter-shell {
            background: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 20px; padding: 1rem 1rem 0.25rem 1rem; margin-bottom: 1rem;
        }
        .filter-title { font-size: 1.05rem; font-weight: 700; color: var(--text-color); margin-bottom: 0.8rem; }
        
        .hero-banner {
            background: color-mix(in srgb, var(--secondary-background-color) 85%, var(--primary-color));
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 24px;
            padding: 1.75rem 1.6rem 1.7rem 1.6rem; margin-bottom: 1.15rem;
        }
        .hero-title { font-size: 1.8rem; font-weight: 800; line-height: 1.22; margin: 0 0 0.65rem 0; color: var(--text-color); }
        .hero-copy { color: var(--text-color); opacity: 0.8; max-width: 44rem; font-size: 1rem; line-height: 1.65; margin: 0; }
        
        .metric-card { color: white; border-radius: 20px; padding: 1rem 1.1rem; min-height: 140px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .metric-icon { width: 50px; height: 50px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; background: rgba(255, 255, 255, 0.16); margin-bottom: 0.7rem; }
        .metric-label { font-size: 0.95rem; opacity: 0.9; color: white !important; }
        .metric-value { font-size: 2rem; font-weight: 800; margin: 0.2rem 0; color: white !important; }
        .metric-note { font-size: 0.9rem; opacity: 0.88; color: white !important; }
        
        .panel-card, .analysis-text-panel, .home-card, .analysis-card {
            background: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 20px; padding: 1.1rem 1.2rem; width: 100%; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 1rem;
        }
        .panel-title, .analysis-panel-title, .home-card-title, .analysis-value { font-size: 1.12rem; font-weight: 700; color: var(--text-color) !important; margin-bottom: 0.5rem; }
        
        .section-shell {
            background: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 22px; padding: 1rem 1.15rem; margin: 1.25rem 0 0.95rem 0;
        }
        .section-kicker {
            display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.28rem 0.7rem; border-radius: 999px;
            background: color-mix(in srgb, var(--primary-color) 15%, transparent); color: var(--primary-color);
            font-size: 0.78rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.65rem;
        }
        .section-heading-row, .analysis-card-head, .analysis-panel-head { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.4rem; }
        .section-icon, .analysis-card-icon, .analysis-panel-icon, .home-card-icon {
            width: 44px; height: 44px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center;
            font-size: 1.2rem; background: color-mix(in srgb, var(--primary-color) 15%, transparent); color: var(--primary-color); flex-shrink: 0;
        }
        .section-title { font-size: 1.32rem; font-weight: 800; color: var(--text-color); margin: 0; }
        .section-copy, .analysis-note, .analysis-bullet, .home-feature-list, .analysis-label { color: var(--text-color); opacity: 0.8; margin: 0; }
        .home-feature-list { padding-left: 1.1rem; } .home-feature-list li { margin-bottom: 0.48rem; line-height: 1.45; }
        
        div[data-testid="column"], div[data-testid="column"] > div, div[data-testid="stPlotlyChart"], div[data-testid="stPlotlyChart"] > div, .stDataFrame, [data-testid="stDataFrame"] { width: 100% !important; }
        .progress-row { margin-bottom: 1rem; }
        .progress-line { height: 10px; border-radius: 999px; background: rgba(128,128,128,0.2); overflow: hidden; margin-top: 0.35rem; }
        .progress-fill { height: 100%; border-radius: 999px; }
        .insight-card { border-radius: 16px; padding: 1rem; margin-bottom: 0.8rem; border: 1px solid rgba(128, 128, 128, 0.2); }
        .insight-warn { background: color-mix(in srgb, #ef4444 15%, transparent); }
        .insight-info { background: color-mix(in srgb, #3b82f6 15%, transparent); }
        @media (max-width: 768px) {
            .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
        }
        
        [st-theme-mode="dark"] .stApp, 
        [st-theme-mode="dark"] header[data-testid="stHeader"],
        [st-theme-mode="dark"] .block-container {
            background-color: #000000 !important;
        }
        [st-theme-mode="dark"] section[data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
        }
        [st-theme-mode="dark"] .topbar,
        [st-theme-mode="dark"] .filter-shell,
        [st-theme-mode="dark"] .hero-banner,
        [st-theme-mode="dark"] .panel-card,
        [st-theme-mode="dark"] .analysis-text-panel,
        [st-theme-mode="dark"] .home-card,
        [st-theme-mode="dark"] .analysis-card,
        [st-theme-mode="dark"] .section-shell,
        [st-theme-mode="dark"] .status-card,
        [st-theme-mode="dark"] .insight-card {
            background: #000000 !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            background-image: none !important;
            box-shadow: none !important;
        }
        [st-theme-mode="dark"] .topbar .stTextInput input,
        [st-theme-mode="dark"] section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background: #0a0a0a !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
        }
        [st-theme-mode="dark"] .metric-icon,
        [st-theme-mode="dark"] .section-icon,
        [st-theme-mode="dark"] .analysis-card-icon,
        [st-theme-mode="dark"] .analysis-panel-icon,
        [st-theme-mode="dark"] .home-card-icon,
        [st-theme-mode="dark"] .section-kicker {
            background: rgba(255, 255, 255, 0.12) !important;
            color: #ffffff !important;
        }
        [st-theme-mode="dark"] .stApp *,
        [st-theme-mode="dark"] .section-title,
        [st-theme-mode="dark"] .panel-title,
        [st-theme-mode="dark"] .filter-title,
        [st-theme-mode="dark"] .analysis-value,
        [st-theme-mode="dark"] .analysis-panel-title,
        [st-theme-mode="dark"] .home-card-title,
        [st-theme-mode="dark"] .hero-title,
        [st-theme-mode="dark"] .metric-value,
        [st-theme-mode="dark"] .metric-label,
        [st-theme-mode="dark"] .metric-note {
            color: #ffffff !important;
        }
        [st-theme-mode="dark"] .section-copy,
        [st-theme-mode="dark"] .analysis-note,
        [st-theme-mode="dark"] .analysis-bullet,
        [st-theme-mode="dark"] .home-feature-list,
        [st-theme-mode="dark"] .analysis-label,
        [st-theme-mode="dark"] .hero-copy {
            color: #dddddd !important;
            opacity: 1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_dashboard_header() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">Smart Traffic Violation Summary Dashboard &#128202;</div>
            <div class="hero-copy">An icon-led summary dashboard for understanding traffic patterns, hotspots, speed behavior, payments, and category trends across the dataset.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_analytics_header() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">&#128200; Advanced Analytics</div>
            <div class="hero-copy">A text-first interpretation layer that turns filtered traffic records into short, readable findings for operational review and stakeholder reporting.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_dashboard_filters(df, title: str = "Dashboard Filters"):
    st.markdown('<div class="filter-shell">', unsafe_allow_html=True)
    st.markdown(f'<div class="filter-title">{title}</div>', unsafe_allow_html=True)

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    col1, col2, col3 = st.columns([1.2, 1, 1])

    date_range = col1.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="dashboard_date_range",
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = min_date

    locations = col2.multiselect(
        "Location",
        options=sorted(df["location"].dropna().unique().tolist()),
        key="dashboard_locations",
    )
    violation_types = col3.multiselect(
        "Violation type",
        options=sorted(df["violation_type"].dropna().unique().tolist()),
        key="dashboard_violation_types",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    return start_date, end_date, locations, violation_types

def render_sidebar_nav() -> str:
    page = st.sidebar.radio("Navigation", NAV_ITEMS, label_visibility="collapsed")
    st.sidebar.markdown(
        """
        <div class="status-card">
            <div style="font-size:1rem; font-weight:700; color:white; margin-bottom:0.35rem;">System Status</div>
            <div style="color:#cbd5e1; font-size:0.9rem;">Insights, filters, reports, and prediction tools are available.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return page

def render_metric_card(style_key: str, label: str, value: str, note: str) -> None:
    style = METRIC_STYLES[style_key]
    st.markdown(
        f"""
        <div class="metric-card" style="background:{style['bg']};">
            <div class="metric-icon">{style['icon']}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_top_violation_panel(type_df: pd.DataFrame) -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Top Violation Types</div>', unsafe_allow_html=True)
    if type_df.empty:
        st.info("No violation data available.")
    else:
        total = max(int(type_df["count"].sum()), 1)
        colors = ["#ef4444", "#f97316", "#f59e0b", "#22c55e", "#3b82f6"]
        for idx, row in enumerate(type_df.head(5).itertuples(index=False)):
            share = (row.count / total) * 100
            color = colors[idx % len(colors)]
            st.markdown(
                f"""
                <div class="progress-row">
                    <div style="display:flex; justify-content:space-between; gap:1rem; font-weight:600; color:#0f172a;">
                        <span>{row.violation_type}</span>
                        <span>{row.count} ({share:.1f}%)</span>
                    </div>
                    <div class="progress-line">
                        <div class="progress-fill" style="width:{share:.1f}%; background:{color};"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

def render_ai_insights(patterns: dict[str, object], risk_df: pd.DataFrame) -> None:
    top_area = risk_df.iloc[0]["location"] if not risk_df.empty else "N/A"
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">AI Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="insight-card insight-warn">
            <div style="font-weight:700; margin-bottom:0.35rem;">Peak Violation Hours</div>
            <div>Violations are most active around <b>{patterns['peak_hour']}</b>. Consider increasing patrol coverage during this window.</div>
        </div>
        <div class="insight-card insight-info">
            <div style="font-weight:700; margin-bottom:0.35rem;">High Risk Focus Area</div>
            <div><b>{top_area}</b> appears as a leading risk zone in the current filtered view. This area may benefit from more monitoring or signage.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def render_recent_violations(df: pd.DataFrame) -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Recent Violations</div>', unsafe_allow_html=True)
    recent = df.sort_values(["date", "time"], ascending=[False, False]).head(6).copy()
    if recent.empty:
        st.info("No recent records available.")
    else:
        id_col = "Violation_ID" if "Violation_ID" in recent.columns else None
        if id_col is None:
            recent.insert(0, "Violation_ID", [f"TV{1000+i}" for i in range(len(recent))])
            id_col = "Violation_ID"
        recent_table = recent[[id_col, "location", "violation_type", "time"]].rename(
            columns={id_col: "ID", "location": "Location", "violation_type": "Type", "time": "Time"}
        )
        if "Fine_Paid" in recent.columns:
            recent_table["Status"] = recent["Fine_Paid"].replace({"Yes": "Paid", "No": "Pending"})
        st.dataframe(recent_table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_chart_panel(fig) -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_section_header(kicker: str, icon: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="section-shell">
            <div class="section-kicker">{kicker}</div>
            <div class="section-heading-row">
                <div class="section-icon">{icon}</div>
                <div class="section-title">{title}</div>
            </div>
            <p class="section-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_analysis_cards(cards: list[dict[str, str]]) -> None:
    columns = st.columns(len(cards))
    for column, card in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="analysis-card">
                    <div class="analysis-card-head">
                        <div class="analysis-card-icon">{card.get('icon', '&#128202;')}</div>
                        <div class="analysis-label">{card['label']}</div>
                    </div>
                    <div class="analysis-value">{card['value']}</div>
                    <div class="analysis-note">{card['note']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

def render_analysis_text_panel(title: str, bullets: list[str], icon: str = "&#128221;") -> None:
    bullet_html = "".join(f'<div class="analysis-bullet">{item}</div>' for item in bullets)
    st.markdown(
        f"""
        <div class="analysis-text-panel">
            <div class="analysis-panel-head">
                <div class="analysis-panel-icon">{icon}</div>
                <div class="analysis-panel-title">{title}</div>
            </div>
            {bullet_html}
        </div>
        """,
        unsafe_allow_html=True,
    )



