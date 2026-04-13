from __future__ import annotations

import pandas as pd
import streamlit as st

from core.analysis import (
    compute_kpis,
    detect_patterns,
    heatmap_summary,
    location_summary,
    predict_risk_clusters,
    vehicle_type_summary,
    violation_type_summary,
    violations_over_time,
)
from core.page_helpers import build_context, summarize_counts
from core.ui import (
    render_chart_panel,
    render_metric_card,
    render_section_header,
)
from core.visualization import (
    categorical_bar_chart,
    categorical_donut_chart,
    histogram_chart,
    location_heatmap,
    risk_cluster_chart,
    vehicle_pie_chart,
    violations_line_chart,
)


def render_dashboard(filtered_df: pd.DataFrame) -> None:
    kpis = compute_kpis(filtered_df)
    patterns = detect_patterns(filtered_df)
    type_df = violation_type_summary(filtered_df)
    time_df = violations_over_time(filtered_df)
    vehicle_df = vehicle_type_summary(filtered_df)
    risk_df = predict_risk_clusters(filtered_df)
    location_df = location_summary(filtered_df).head(10)
    context = build_context(filtered_df, risk_df)

    hourly_df = patterns["hourly_distribution"].copy()
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_df = summarize_counts(filtered_df, "day_name")
    if not day_df.empty:
        day_df["day_name"] = pd.Categorical(day_df["day_name"], categories=day_order, ordered=True)
        day_df = day_df.sort_values("day_name")

    weather_df = summarize_counts(filtered_df, "Weather_Condition", top_n=8)
    road_df = summarize_counts(filtered_df, "Road_Condition")
    state_df = summarize_counts(filtered_df, "Registration_State", top_n=8)
    gender_df = summarize_counts(filtered_df, "Driver_Gender")
    license_df = summarize_counts(filtered_df, "License_Type")
    payment_df = summarize_counts(filtered_df, "Fine_Paid")
    payment_method_df = summarize_counts(filtered_df, "Payment_Method")
    signal_df = summarize_counts(filtered_df, "signal_status")
    helmet_df = summarize_counts(filtered_df, "helmet_detected")
    vehicle_color_df = summarize_counts(filtered_df, "Vehicle_Color", top_n=8)
    breathalyzer_df = summarize_counts(filtered_df, "Breathalyzer_Result")
    seatbelt_df = summarize_counts(filtered_df, "Seatbelt_Worn")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("total", "Total Violations", f"{context['total']:,}", f"Top type: {kpis['top_violation']}")
    with c2:
        render_metric_card("risk", "High Risk Locations", str(context["risk"]), f"Peak day: {patterns['peak_day']}")
    with c3:
        render_metric_card("pending", "Pending Fine Payments", f"{context['pending']:,}", "Current filtered view")
    with c4:
        render_metric_card("speed", "Avg. Recorded Speed", f"{context['speed']:.1f} km/h", f"Peak hour: {patterns['peak_hour']}")

    render_section_header("Core Pattern", "&#128202;", "Violation Type Distribution", "Compare the most common offense categories and understand which traffic violations dominate the current filtered dataset.")
    sec1_col1, sec1_col2 = st.columns([1.2, 1])
    with sec1_col1:
        render_chart_panel(categorical_bar_chart(type_df.head(10), "violation_type", "count", "Violation Type Distribution", ["#fee2e2", "#dc2626"]))
    with sec1_col2:
        render_chart_panel(categorical_donut_chart(type_df.head(6), "violation_type", "count", "Violation Type Share"))

    render_section_header("Spatial Risk", "&#128205;", "Violations by Location", "Review where violations are concentrated and identify hotspots that may need stronger enforcement or operational attention.")
    sec2_col1, sec2_col2 = st.columns(2)
    with sec2_col1:
        if not location_df.empty:
            render_chart_panel(categorical_bar_chart(location_df, "location", "count", "Violations by Location", ["#e0f2fe", "#0891b2"]))
    with sec2_col2:
        if not risk_df.empty:
            render_chart_panel(risk_cluster_chart(risk_df))
        else:
            render_chart_panel(location_heatmap(heatmap_summary(filtered_df)))

    render_section_header("Fleet View", "&#128663;", "Vehicle-Based Analysis", "Break down the dataset by vehicle mix, color patterns, and registration geography to reveal operational and enforcement trends.")
    sec3_col1, sec3_col2, sec3_col3 = st.columns(3)
    with sec3_col1:
        render_chart_panel(vehicle_pie_chart(vehicle_df))
    with sec3_col2:
        if not vehicle_color_df.empty:
            render_chart_panel(categorical_bar_chart(vehicle_color_df, "Vehicle_Color", "count", "Vehicle Color Distribution", ["#dbeafe", "#2563eb"]))
    with sec3_col3:
        if not state_df.empty:
            render_chart_panel(categorical_bar_chart(state_df, "Registration_State", "count", "Registration State Analysis", ["#ede9fe", "#7c3aed"]))

    render_section_header("Behavior Signals", "&#128100;", "Driver Behavior Analysis", "Explore behavioral indicators such as prior violations, seatbelt usage, and demographic distribution to understand driver-side risk patterns.")
    sec4_col1, sec4_col2, sec4_col3 = st.columns(3)
    with sec4_col1:
        if not gender_df.empty:
            render_chart_panel(categorical_donut_chart(gender_df, "Driver_Gender", "count", "Driver Gender Distribution"))
        elif not license_df.empty:
            render_chart_panel(categorical_donut_chart(license_df, "License_Type", "count", "License Type Distribution"))
    with sec4_col2:
        if "Previous_Violations" in filtered_df.columns:
            render_chart_panel(histogram_chart(filtered_df, "Previous_Violations", "Previous Violations History", nbins=15, color="#16a34a"))
    with sec4_col3:
        if not seatbelt_df.empty:
            render_chart_panel(categorical_donut_chart(seatbelt_df, "Seatbelt_Worn", "count", "Seatbelt Usage"))
        elif not helmet_df.empty:
            render_chart_panel(categorical_donut_chart(helmet_df, "helmet_detected", "count", "Helmet Detection Status"))

    render_section_header("Speed Monitoring", "&#9889;", "Speed Analysis", "Inspect speed distributions, time-based intensity, and legal speed thresholds to understand overspeeding exposure across the dataset.")
    sec5_col1, sec5_col2, sec5_col3 = st.columns(3)
    with sec5_col1:
        render_chart_panel(histogram_chart(filtered_df, "speed", "Recorded Speed Distribution", nbins=24, color="#7c3aed"))
    with sec5_col2:
        if not hourly_df.empty:
            render_chart_panel(categorical_bar_chart(hourly_df, "hour", "count", "Hourly Speed-Linked Activity", ["#dbeafe", "#2563eb"]))
    with sec5_col3:
        if "Speed_Limit" in filtered_df.columns:
            render_chart_panel(histogram_chart(filtered_df, "Speed_Limit", "Speed Limit Distribution", nbins=18, color="#f97316"))

    render_section_header("Safety Risk", "&#127863;", "Drunk Driving", "Track alcohol-related signals using alcohol level and breathalyzer outcomes to surface impaired-driving risk in the data.")
    sec6_col1, sec6_col2 = st.columns(2)
    with sec6_col1:
        if "Alcohol_Level" in filtered_df.columns:
            render_chart_panel(histogram_chart(filtered_df, "Alcohol_Level", "Alcohol Level Distribution", nbins=20, color="#ef4444"))
    with sec6_col2:
        if not breathalyzer_df.empty:
            render_chart_panel(categorical_donut_chart(breathalyzer_df, "Breathalyzer_Result", "count", "Breathalyzer Results"))

    render_section_header("Revenue Insights", "&#128176;", "Fine & Payment Insights Analysis", "Evaluate payment completion, amount distribution, and transaction preferences to understand financial closure and collection patterns.")
    sec7_col1, sec7_col2, sec7_col3 = st.columns(3)
    with sec7_col1:
        if not payment_df.empty:
            render_chart_panel(categorical_donut_chart(payment_df, "Fine_Paid", "count", "Fine Payment Status"))
    with sec7_col2:
        if "Fine_Amount" in filtered_df.columns:
            render_chart_panel(histogram_chart(filtered_df, "Fine_Amount", "Fine Amount Distribution", nbins=20, color="#dc2626"))
    with sec7_col3:
        if not payment_method_df.empty:
            render_chart_panel(categorical_bar_chart(payment_method_df, "Payment_Method", "count", "Payment Method Analysis", ["#dcfce7", "#16a34a"]))

    render_section_header("Operating Context", "&#127774;", "Environmental Impact", "Measure how weather, road conditions, and signal context relate to the traffic violations captured in the filtered view.")
    sec8_col1, sec8_col2, sec8_col3 = st.columns(3)
    with sec8_col1:
        if not weather_df.empty:
            render_chart_panel(categorical_bar_chart(weather_df, "Weather_Condition", "count", "Weather Condition Impact", ["#fef3c7", "#f59e0b"]))
    with sec8_col2:
        if not road_df.empty:
            render_chart_panel(categorical_donut_chart(road_df, "Road_Condition", "count", "Road Condition Impact"))
    with sec8_col3:
        if not signal_df.empty:
            render_chart_panel(categorical_donut_chart(signal_df, "signal_status", "count", "Traffic Light Status"))
        elif not day_df.empty:
            render_chart_panel(categorical_bar_chart(day_df, "day_name", "count", "Violations by Day", ["#bfdbfe", "#2563eb"]))
