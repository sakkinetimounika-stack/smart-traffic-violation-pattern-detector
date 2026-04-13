from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PLOTLY_TEMPLATE = "plotly_white"


def _light_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=56, b=20),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False, zerolinecolor="rgba(128,128,128,0.2)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", zerolinecolor="rgba(128,128,128,0.2)")
    return fig


def violation_bar_chart(summary_df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        summary_df.head(8),
        x="violation_type",
        y="count",
        color="count",
        color_continuous_scale=["#fee2e2", "#dc2626"],
        template=PLOTLY_TEMPLATE,
        title="Top Violation Types",
    )
    fig.update_layout(xaxis_title="Violation Type", yaxis_title="Count", coloraxis_showscale=False)
    return _light_layout(fig)


def violations_line_chart(time_df: pd.DataFrame) -> go.Figure:
    fig = px.area(
        time_df,
        x="date",
        y="count",
        template=PLOTLY_TEMPLATE,
        title="Violation Trend Over Time",
    )
    fig.update_traces(line=dict(color="#dc2626", width=3), fillcolor="rgba(220, 38, 38, 0.12)")
    fig.update_layout(xaxis_title="Date", yaxis_title="Violations")
    return _light_layout(fig)


def vehicle_pie_chart(vehicle_df: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        vehicle_df,
        names="vehicle_type",
        values="count",
        hole=0.62,
        template=PLOTLY_TEMPLATE,
        title="Vehicle Distribution",
        color_discrete_sequence=["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#e11d48", "#0891b2"],
    )
    fig.update_traces(textinfo="percent")
    return _light_layout(fig)


def location_heatmap(heatmap_df: pd.DataFrame) -> go.Figure:
    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        color_continuous_scale=["#eff6ff", "#93c5fd", "#3b82f6", "#1d4ed8"],
        template=PLOTLY_TEMPLATE,
        title="Location Heatmap",
        labels=dict(x="Violation Type", y="Location", color="Count"),
    )
    return _light_layout(fig)


def risk_cluster_chart(risk_df: pd.DataFrame) -> go.Figure:
    color_map = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
    fig = px.scatter(
        risk_df,
        x="violations",
        y="avg_speed",
        size="violations",
        color="risk_level",
        hover_name="location",
        template=PLOTLY_TEMPLATE,
        title="High Risk Locations",
        color_discrete_map=color_map,
    )
    fig.update_traces(marker=dict(line=dict(color="white", width=1), opacity=0.85))
    fig.update_layout(xaxis_title="Violation Count", yaxis_title="Average Recorded Speed")
    return _light_layout(fig)



def categorical_bar_chart(
    summary_df: pd.DataFrame,
    label_col: str,
    value_col: str,
    title: str,
    color_scale: list[str] | None = None,
) -> go.Figure:
    colors = color_scale or ["#dbeafe", "#2563eb"]
    fig = px.bar(
        summary_df,
        x=label_col,
        y=value_col,
        color=value_col,
        color_continuous_scale=colors,
        template=PLOTLY_TEMPLATE,
        title=title,
    )
    fig.update_layout(
        xaxis_title=label_col.replace('_', ' ').title(),
        yaxis_title=value_col.replace('_', ' ').title(),
        coloraxis_showscale=False,
    )
    return _light_layout(fig)


def categorical_donut_chart(
    summary_df: pd.DataFrame,
    label_col: str,
    value_col: str,
    title: str,
) -> go.Figure:
    fig = px.pie(
        summary_df,
        names=label_col,
        values=value_col,
        hole=0.58,
        template=PLOTLY_TEMPLATE,
        title=title,
        color_discrete_sequence=["#2563eb", "#10b981", "#f97316", "#7c3aed", "#e11d48", "#0891b2", "#f59e0b"],
    )
    fig.update_traces(textinfo="percent+label")
    return _light_layout(fig)


def histogram_chart(
    df: pd.DataFrame,
    column: str,
    title: str,
    nbins: int = 24,
    color: str = "#2563eb",
) -> go.Figure:
    plot_df = df.copy()
    plot_df[column] = pd.to_numeric(plot_df[column], errors="coerce")
    plot_df = plot_df.dropna(subset=[column])
    fig = px.histogram(
        plot_df,
        x=column,
        nbins=nbins,
        template=PLOTLY_TEMPLATE,
        title=title,
    )
    fig.update_traces(marker_color=color, marker_line_color="white", marker_line_width=1)
    fig.update_layout(xaxis_title=column.replace('_', ' ').title(), yaxis_title="Count")
    return _light_layout(fig)
