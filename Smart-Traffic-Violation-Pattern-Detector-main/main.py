from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.app_config import (
    APP_ICON,
    APP_TITLE,
    PAGE_ADVANCED,
    PAGE_DASHBOARD,
    PAGE_HOME,
    PAGE_PREDICTIONS,
    PAGE_REPORTS,
    PAGE_UPLOAD,
    PAGE_VISUALIZATION,
    PAGE_TRENDS,
)
from core.data_services import load_data_from_path, load_data_from_upload
from core.homepage import render_home_page
from core.pages import (
    render_advanced_analytics,
    render_dashboard,
    render_prediction_module,
    render_reports_page,
    render_upload_page,
    render_visualization_page,
    render_trend_analysis_page,
)
from core.ui import (
    inject_styles,
    render_analytics_header,
    render_dashboard_filters,
    render_dashboard_header,
    render_sidebar_nav,
)
from core.analysis import apply_filters


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)



def main() -> None:
    inject_styles()

    default_path = Path("dataset.csv")
    active_source_label = "Local dataset: dataset.csv"

    try:
        uploaded_bytes = st.session_state.get("uploaded_dataset_bytes")
        if uploaded_bytes:
            df = load_data_from_upload(uploaded_bytes)
            uploaded_name = st.session_state.get("uploaded_dataset_name", "uploaded_file.csv")
            active_source_label = f"Uploaded dataset: {uploaded_name}"
            st.sidebar.caption(f"Using uploaded dataset: `{uploaded_name}`")
        else:
            df = load_data_from_path(str(default_path))
            st.sidebar.caption("Using local dataset: `dataset.csv`")
    except Exception as exc:
        st.error(f"Unable to load dataset: {exc}")
        st.stop()

    if df.empty:
        st.warning("No valid records were found in the dataset.")
        st.stop()

    page = render_sidebar_nav()

    filtered_df = df
    pages_with_filters = {
        PAGE_DASHBOARD,
        PAGE_ADVANCED,
        PAGE_REPORTS,
    }
    if page in pages_with_filters:
        if page == PAGE_DASHBOARD:
            render_dashboard_header()
        elif page == PAGE_ADVANCED:
            render_analytics_header()
        filter_title = "Analytics Filter" if page == PAGE_ADVANCED else "Dashboard Filters"
        start_date, end_date, locations, violation_types = render_dashboard_filters(df, filter_title)
        filtered_df = apply_filters(df, start_date, end_date, locations, violation_types)

        if filtered_df.empty:
            st.warning("No records match the selected filters. Try broadening the date range or filter selection.")
            st.stop()

    if page == PAGE_HOME:
        render_home_page()
    elif page == PAGE_DASHBOARD:
        render_dashboard(filtered_df)
    elif page == PAGE_ADVANCED:
        render_advanced_analytics(filtered_df)
    elif page == PAGE_PREDICTIONS:
        render_prediction_module(df)
    elif page == PAGE_REPORTS:
        render_reports_page(filtered_df)
    elif page == PAGE_UPLOAD:
        render_upload_page(df, active_source_label)
    elif page == PAGE_VISUALIZATION:
        render_visualization_page(df)
    elif page == PAGE_TRENDS:
        render_trend_analysis_page(df)


if __name__ == "__main__":
    main()
