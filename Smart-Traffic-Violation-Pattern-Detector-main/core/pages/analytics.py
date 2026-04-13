from __future__ import annotations

import pandas as pd
import streamlit as st

from core.analysis import (
    compute_kpis,
    detect_patterns,
    heatmap_summary,
    location_summary,
    vehicle_type_summary,
    violation_type_summary,
)
from core.page_helpers import summarize_counts
from core.ui import (
    render_analysis_cards,
    render_analysis_text_panel,
    render_chart_panel,
    render_section_header,
)
from core.visualization import location_heatmap, violation_bar_chart


def render_advanced_analytics(filtered_df: pd.DataFrame) -> None:
    kpis = compute_kpis(filtered_df)
    patterns = detect_patterns(filtered_df)
    type_df = violation_type_summary(filtered_df)
    location_df = location_summary(filtered_df)
    vehicle_df = vehicle_type_summary(filtered_df)

    top_violation = type_df.iloc[0]["violation_type"] if not type_df.empty else "N/A"
    top_violation_count = int(type_df.iloc[0]["count"]) if not type_df.empty else 0
    second_violation = type_df.iloc[1]["violation_type"] if len(type_df) > 1 else "N/A"
    top_location = location_df.iloc[0]["location"] if not location_df.empty else "N/A"
    top_location_count = int(location_df.iloc[0]["count"]) if not location_df.empty else 0
    top_vehicle = vehicle_df.iloc[0]["vehicle_type"] if not vehicle_df.empty else "N/A"
    top_vehicle_count = int(vehicle_df.iloc[0]["count"]) if not vehicle_df.empty else 0

    payment_df = summarize_counts(filtered_df, "Fine_Paid")
    gender_df = summarize_counts(filtered_df, "Driver_Gender")
    weather_df = summarize_counts(filtered_df, "Weather_Condition")

    paid_pct = 0.0
    if not payment_df.empty and payment_df["count"].sum() > 0:
        paid_count = int(payment_df.loc[payment_df["Fine_Paid"] == "Yes", "count"].sum())
        paid_pct = (paid_count / int(payment_df["count"].sum())) * 100

    gender_leader = gender_df.iloc[0]["Driver_Gender"] if not gender_df.empty else "N/A"
    weather_leader = weather_df.iloc[0]["Weather_Condition"] if not weather_df.empty else "N/A"

    render_analysis_cards(
        [
            {
                "label": "Leading Violation",
                "icon": "&#9888;",
                "value": f"{top_violation} ({top_violation_count})",
                "note": "This violation currently appears most often in the filtered dataset and should be prioritized in enforcement review.",
            },
            {
                "label": "Primary Hotspot",
                "icon": "&#128205;",
                "value": f"{top_location} ({top_location_count})",
                "note": "This location is contributing the highest concentration of violations in the current analytical view.",
            },
            {
                "label": "Dominant Vehicle",
                "icon": "&#128663;",
                "value": f"{top_vehicle} ({top_vehicle_count})",
                "note": "This vehicle category is the strongest contributor to recorded violations across the filtered sample.",
            },
        ]
    )

    render_analysis_cards(
        [
            {
                "label": "Peak Hour",
                "icon": "&#9200;",
                "value": str(patterns["peak_hour"]),
                "note": "This time window shows the highest traffic-violation intensity and can guide focused monitoring.",
            },
            {
                "label": "Peak Day",
                "icon": "&#128197;",
                "value": str(patterns["peak_day"]),
                "note": "This weekday currently produces the highest overall violation volume in the selected records.",
            },
            {
                "label": "Payment Completion",
                "icon": "&#128176;",
                "value": f"{paid_pct:.1f}% paid",
                "note": "This indicates the current fine-settlement rate and helps assess payment compliance behavior.",
            },
        ]
    )

    render_section_header("Narrative Summary", "&#128221;", "Operational Reading", "These short findings are designed for quick briefings, status updates, and analytical interpretation without needing to inspect every chart in detail.")

    render_analysis_text_panel(
        "Key Findings",
        [
            f"Top enforcement concern: <b>{top_violation}</b> is the leading violation type, while <b>{second_violation}</b> also appears prominently in the current filtered view.",
            f"Location pressure is highest in <b>{top_location}</b>, suggesting a concentrated hotspot rather than a fully uniform distribution across regions.",
            f"Vehicle exposure is led by <b>{top_vehicle}</b>, which may indicate category-specific non-compliance or route concentration effects.",
        ],
        icon="&#128161;",
    )

    render_analysis_text_panel(
        "Behavior & Compliance Insights",
        [
            f"Violation activity peaks during <b>{patterns['peak_hour']}</b>, which can support shift planning and patrol deployment decisions.",
            f"The strongest day-level concentration currently falls on <b>{patterns['peak_day']}</b>, which may reflect recurring commute or enforcement patterns.",
            f"Fine payment completion is currently estimated at <b>{paid_pct:.1f}%</b>, providing a simple read on compliance after enforcement action.",
        ],
        icon="&#129504;",
    )

    render_analysis_text_panel(
        "Contextual Interpretation",
        [
            f"The most represented driver segment in the filtered records is <b>{gender_leader}</b>, while the most common weather context is <b>{weather_leader}</b>.",
            f"Average recorded speed is <b>{kpis['avg_speed']:.2f} km/h</b>, which helps frame whether the filtered set reflects routine violations or more severe movement-related risk.",
            "This page is intentionally text-led so the findings can be read quickly in meetings, reviews, and progress discussions before deeper chart exploration.",
        ],
        icon="&#128269;",
    )

    st.markdown("### Supporting Views")
    support_col1, support_col2 = st.columns(2)
    with support_col1:
        render_chart_panel(violation_bar_chart(type_df))
    with support_col2:
        render_chart_panel(location_heatmap(heatmap_summary(filtered_df)))

    st.markdown("### Record Preview")
    preview_cols = [col for col in ["date", "location", "violation_type", "vehicle_type", "speed", "Fine_Paid"] if col in filtered_df.columns]
    st.dataframe(filtered_df[preview_cols].head(20) if preview_cols else filtered_df.head(20), use_container_width=True, hide_index=True)
