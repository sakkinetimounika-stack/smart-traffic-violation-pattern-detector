from __future__ import annotations

import pandas as pd
import streamlit as st

from core.data_services import load_data_from_upload


def render_upload_page(active_df: pd.DataFrame, active_source_label: str) -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">Upload Dataset</div>
            <div class="hero-copy">Drag and drop a CSV file to replace the active dataset for dashboarding, analytics, reports, and predictions.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload a CSV dataset",
        type=["csv"],
        help="Drag and drop your CSV file here, or click to browse.",
        key="upload_dataset_page",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        try:
            uploaded_df = load_data_from_upload(file_bytes)
            st.session_state["uploaded_dataset_bytes"] = file_bytes
            st.session_state["uploaded_dataset_name"] = uploaded_file.name
            active_df = uploaded_df
            active_source_label = f"Uploaded dataset: {uploaded_file.name}"
            st.success(f"Dataset uploaded successfully: {uploaded_file.name}")
        except Exception as exc:
            st.error(f"Unable to process uploaded file: {exc}")

    info_col1, info_col2 = st.columns([1.35, 1])
    with info_col1:
        st.markdown(f"**Active Source:** {active_source_label}")
        st.caption("The currently active dataset is used across the dashboard, analytics, predictions, and reports pages.")
    with info_col2:
        if st.button("Use Local dataset.csv", use_container_width=True):
            st.session_state.pop("uploaded_dataset_bytes", None)
            st.session_state.pop("uploaded_dataset_name", None)
            st.rerun()

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Rows", f"{len(active_df):,}")
    metric_col2.metric("Columns", f"{len(active_df.columns):,}")
    metric_col3.metric("Locations", f"{active_df['location'].nunique():,}" if "location" in active_df.columns else "0")

    preview_cols = [col for col in ["date", "location", "violation_type", "vehicle_type", "speed"] if col in active_df.columns]
    st.markdown("### Dataset Preview")
    st.dataframe(active_df[preview_cols].head(15) if preview_cols else active_df.head(15), use_container_width=True, hide_index=True)
