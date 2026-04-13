from __future__ import annotations

import streamlit as st

from core.analysis import predict_fine_payment_status
from core.data_services import get_payment_model


def render_prediction_module(source_df):
    st.markdown("### Prediction")
    st.caption(
        "Estimate whether a driver is likely to pay their traffic fine based on driver, speed, and violation-related details."
    )

    model_bundle = get_payment_model(source_df)
    if model_bundle is None:
        st.warning("The current dataset does not contain enough valid `Fine_Paid` training data for prediction.")
        return

    metrics = model_bundle["metrics"]
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Model Accuracy", f"{metrics['accuracy'] * 100:.1f}%")
    metric_col2.metric("ROC AUC", f"{metrics['roc_auc']:.3f}")
    metric_col3.metric("Training Rows", f"{metrics['train_rows']:,}")

    with st.form("fine_payment_prediction_form"):
        st.markdown("#### Driver & Violation Details")
        options = model_bundle["choices"]
        numeric_ranges = model_bundle["numeric_ranges"]

        row1 = st.columns(3)
        vehicle_type = row1[0].selectbox("Vehicle Type", options["Vehicle_Type"])
        registration_state = row1[1].selectbox("Registration State", options["Registration_State"])
        driver_age = row1[2].number_input(
            "Driver Age",
            min_value=numeric_ranges["Driver_Age"]["min"],
            max_value=numeric_ranges["Driver_Age"]["max"],
            value=numeric_ranges["Driver_Age"]["default"],
            step=1.0,
        )

        row2 = st.columns(3)
        license_type = row2[0].selectbox("License Type", options["License_Type"])
        penalty_points = row2[1].number_input(
            "Penalty Points",
            min_value=numeric_ranges["Penalty_Points"]["min"],
            max_value=numeric_ranges["Penalty_Points"]["max"],
            value=numeric_ranges["Penalty_Points"]["default"],
            step=1.0,
        )
        weather_condition = row2[2].selectbox("Weather Condition", options["Weather_Condition"])

        row3 = st.columns(3)
        speed_limit = row3[0].number_input(
            "Speed Limit",
            min_value=numeric_ranges["Speed_Limit"]["min"],
            max_value=numeric_ranges["Speed_Limit"]["max"],
            value=numeric_ranges["Speed_Limit"]["default"],
            step=1.0,
        )
        recorded_speed = row3[1].number_input(
            "Recorded Speed",
            min_value=numeric_ranges["Recorded_Speed"]["min"],
            max_value=numeric_ranges["Recorded_Speed"]["max"],
            value=numeric_ranges["Recorded_Speed"]["default"],
            step=1.0,
        )
        previous_violations = row3[2].number_input(
            "Previous Violations",
            min_value=numeric_ranges["Previous_Violations"]["min"],
            max_value=numeric_ranges["Previous_Violations"]["max"],
            value=numeric_ranges["Previous_Violations"]["default"],
            step=1.0,
        )

        submitted = st.form_submit_button("Run Prediction", use_container_width=True)

    if submitted:
        payload = {
            "Vehicle_Type": vehicle_type,
            "Registration_State": registration_state,
            "Driver_Age": driver_age,
            "License_Type": license_type,
            "Penalty_Points": penalty_points,
            "Weather_Condition": weather_condition,
            "Speed_Limit": speed_limit,
            "Recorded_Speed": recorded_speed,
            "Previous_Violations": previous_violations,
        }
        prediction = predict_fine_payment_status(model_bundle, payload)
        result_col1, result_col2 = st.columns([1.2, 1])
        if prediction["pay_probability"] >= 50:
            result_col1.success(
                f"Prediction: {prediction['label']} ({prediction['pay_probability']:.2f}% probability)"
            )
        else:
            result_col1.error(
                f"Prediction: {prediction['label']} ({prediction['non_pay_probability']:.2f}% non-payment probability)"
            )
        result_col2.metric("Pay Probability", f"{prediction['pay_probability']:.2f}%")
        st.progress(min(max(prediction["pay_probability"] / 100, 0.0), 1.0))
