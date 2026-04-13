from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px
from core.visualization import _light_layout


MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def render_trend_analysis_page(df: pd.DataFrame) -> None:
    st.markdown("## Trend Analysis")

    # -------------------------------------------------------------------
    # Derive helper columns from the already-parsed 'date' column
    # -------------------------------------------------------------------
    work = df.copy()
    if "date" in work.columns:
        work["date"] = pd.to_datetime(work["date"], errors="coerce")
        work["_year"] = work["date"].dt.year.astype("Int64")
        work["_month"] = work["date"].dt.month_name()
        work["_month_num"] = work["date"].dt.month
        work["_day"] = work["date"].dt.day_name()
        work["_hour"] = work["hour"] if "hour" in work.columns else work["event_time"].dt.hour
        work["_date_only"] = work["date"].dt.date

    states = sorted(work["location"].dropna().unique().tolist()) if "location" in work.columns else []
    viol_types = sorted(work["violation_type"].dropna().unique().tolist()) if "violation_type" in work.columns else []
    years_available = sorted(work["_year"].dropna().unique().tolist())

    # ===================================================================
    # 1) Monthly Violations by Type
    # ===================================================================
    st.markdown("### 1) Monthly Violations by Type")
    min_date = work["date"].min().date()
    max_date = work["date"].max().date()
    c1a, c1b = st.columns(2)
    with c1a:
        sel_year1 = st.selectbox("Year", ["All"] + years_available, key="t1_year")
    with c1b:
        sel_state1 = st.selectbox("State", ["All"] + states, key="t1_state")

    s1 = work.copy()
    if sel_year1 != "All":
        s1 = s1[s1["_year"] == int(sel_year1)]
    if sel_state1 != "All":
        s1 = s1[s1["location"] == sel_state1]

    if not s1.empty:
        grp1 = s1.groupby(["_month", "violation_type"]).size().reset_index(name="Count")
        grp1["_month"] = pd.Categorical(grp1["_month"], categories=MONTH_ORDER, ordered=True)
        grp1 = grp1.sort_values("_month")
        fig1 = px.line(
            grp1, x="_month", y="Count", color="violation_type",
            title="Monthly Violations by Type", markers=True,
            labels={"_month": "Month", "violation_type": "Violation Type"},
        )
        st.plotly_chart(_light_layout(fig1), use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

    # ===================================================================
    # 2) Traffic Light Status by Month & Vehicle Type
    # ===================================================================
    st.markdown("---")
    st.markdown("### 2) Monthly Traffic Light Status by Vehicle Type")
    vehicle_types = sorted(work["vehicle_type"].dropna().unique().tolist()) if "vehicle_type" in work.columns else []
    c2a, c2b, c2c = st.columns(3)
    with c2a:
        sel_year2 = st.selectbox("Year", ["All"] + years_available, key="t2_year")
    with c2b:
        sel_state2 = st.selectbox("State", ["All"] + states, key="t2_state")
    with c2c:
        sel_vehicle2 = st.selectbox("Vehicle Type", ["All"] + vehicle_types, key="t2_vehicle")

    s2 = work.copy()
    if sel_year2 != "All":
        s2 = s2[s2["_year"] == int(sel_year2)]
    if sel_state2 != "All":
        s2 = s2[s2["location"] == sel_state2]
    if sel_vehicle2 != "All":
        s2 = s2[s2["vehicle_type"] == sel_vehicle2]

    signal_col = "signal_status" if "signal_status" in s2.columns else None
    if signal_col and not s2.empty:
        grp2 = s2.groupby(["_month", signal_col]).size().reset_index(name="Count")
        grp2["_month"] = pd.Categorical(grp2["_month"], categories=MONTH_ORDER, ordered=True)
        grp2 = grp2.sort_values("_month")
        pivot2 = grp2.pivot(index=signal_col, columns="_month", values="Count").fillna(0)
        # Ensure consistent row order
        for status in ["Red", "Yellow", "Green"]:
            if status not in pivot2.index:
                pivot2.loc[status] = 0
        pivot2 = pivot2.loc[["Red", "Yellow", "Green"]]
        fig2 = px.imshow(
            pivot2,
            aspect="auto",
            color_continuous_scale=["#eff6ff", "#3b82f6", "#1e3a8a"],
            title="Months vs Traffic Light Status (by Vehicle Type)",
            labels=dict(x="Month", y="Traffic Light Status", color="Count"),
        )
        fig2.update_traces(text=pivot2.values, texttemplate="%{text:.0f}")
        st.plotly_chart(_light_layout(fig2), use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

    # ===================================================================
    # 3) Total Fine Amount vs Years
    # ===================================================================
    st.markdown("---")
    st.markdown("### 3) Total Fine Amount vs Years")
    has_fine = "Fine_Amount" in work.columns
    if has_fine and len(years_available) > 0:
        c3a, c3b = st.columns(2)
        with c3a:
            mn, mx = int(min(years_available)), int(max(years_available))
            if mn < mx:
                yr_range = st.slider("Year Range", min_value=mn, max_value=mx, value=(mn, mx), key="t3_yr")
            else:
                yr_range = (mn, mx)
                st.info(f"Only one year ({mn}) available.")
        with c3b:
            sel_state3 = st.selectbox("Location (State)", ["All"] + states, key="t3_state")

        s3 = work.copy()
        s3["Fine_Amount"] = pd.to_numeric(s3["Fine_Amount"], errors="coerce").fillna(0)
        s3 = s3[(s3["_year"] >= yr_range[0]) & (s3["_year"] <= yr_range[1])]
        if sel_state3 != "All":
            s3 = s3[s3["location"] == sel_state3]

        if not s3.empty:
            grp3 = s3.groupby("_year")["Fine_Amount"].sum().reset_index()
            fig3 = px.line(
                grp3, x="_year", y="Fine_Amount",
                title="Total Fine Amount vs Years", markers=True,
                labels={"_year": "Year", "Fine_Amount": "Total Fine Amount (₹)"},
            )
            fig3.update_xaxes(type="category")
            st.plotly_chart(_light_layout(fig3), use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
    else:
        st.warning("Data lacks 'Fine_Amount' or year information for this analysis.")

    # ===================================================================
    # 4) Custom Trend Exploration
    # ===================================================================
    st.markdown("---")
    st.markdown("### 4) Custom Trend Exploration")

    # Curated axis options that make sense for the user
    x_options = {
        "Year": "_year",
        "Month": "_month",
        "Day of Week": "_day",
        "Hour": "_hour",
        "Location (State)": "location",
        "Violation Type": "violation_type",
        "Vehicle Type": "vehicle_type",
        "Weather Condition": "Weather_Condition",
        "Road Condition": "Road_Condition",
        "Registration State": "Registration_State",
        "License Type": "License_Type",
        "Driver Gender": "Driver_Gender",
    }
    # Only keep options whose columns actually exist
    x_options = {k: v for k, v in x_options.items() if v in work.columns}

    value_options = {
        "Number of Violations (count)": "__count__",
        "Total Fine Amount": "Fine_Amount",
        "Average Fine Amount": "Fine_Amount__avg",
        "Average Recorded Speed": "speed",
        "Total Penalty Points": "Penalty_Points",
        "Average Driver Age": "Driver_Age__avg",
        "Average Alcohol Level": "Alcohol_Level__avg",
    }
    value_options = {k: v for k, v in value_options.items()
                     if v == "__count__" or v.replace("__avg", "") in work.columns}

    color_options = {
        "None": None,
        "Location (State)": "location",
        "Violation Type": "violation_type",
        "Vehicle Type": "vehicle_type",
        "Driver Gender": "Driver_Gender",
        "Registration State": "Registration_State",
        "Weather Condition": "Weather_Condition",
    }
    color_options = {k: v for k, v in color_options.items() if v is None or v in work.columns}

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        sel_state4 = st.selectbox("State Filter", ["All"] + states, key="t4_state")
    with r1c2:
        sel_viol4 = st.selectbox("Violation Type Filter", ["All"] + viol_types, key="t4_viol")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        x_label = st.selectbox("X-Axis", list(x_options.keys()), key="t4_x")
    with r2c2:
        val_label = st.selectbox("Value (Y-Axis)", list(value_options.keys()), key="t4_val")
    with r2c3:
        color_label = st.selectbox("Color / Group By", list(color_options.keys()), key="t4_color")

    chart_type = st.selectbox("Graph Type", ["Bar Chart", "Line Chart", "Pie Chart"], key="t4_chart")

    x_col = x_options[x_label]
    val_key = value_options[val_label]
    color_col = color_options[color_label]

    s4 = work.copy()
    if sel_state4 != "All":
        s4 = s4[s4["location"] == sel_state4]
    if sel_viol4 != "All":
        s4 = s4[s4["violation_type"] == sel_viol4]

    if s4.empty:
        st.info("No data available for the custom selection.")
    else:
        # Build the aggregated dataframe
        group_cols = [x_col]
        if color_col and color_col != x_col:
            group_cols.append(color_col)

        if val_key == "__count__":
            agg_df = s4.groupby(group_cols).size().reset_index(name="Count")
            y_col_name = "Count"
        elif val_key.endswith("__avg"):
            raw_col = val_key.replace("__avg", "")
            s4[raw_col] = pd.to_numeric(s4[raw_col], errors="coerce")
            agg_df = s4.groupby(group_cols)[raw_col].mean().reset_index()
            agg_df = agg_df.rename(columns={raw_col: f"Avg {raw_col}"})
            y_col_name = f"Avg {raw_col}"
        else:
            s4[val_key] = pd.to_numeric(s4[val_key], errors="coerce")
            agg_df = s4.groupby(group_cols)[val_key].sum().reset_index()
            y_col_name = val_key

        # Sort months/days properly if on x-axis
        if x_col == "_month":
            agg_df["_month"] = pd.Categorical(agg_df["_month"], categories=MONTH_ORDER, ordered=True)
            agg_df = agg_df.sort_values("_month")
        elif x_col == "_year":
            agg_df = agg_df.sort_values("_year")
        elif x_col == "_hour":
            agg_df = agg_df.sort_values("_hour")

        color_arg = color_col if color_col else None
        title_text = f"{val_label} by {x_label}" + (f" (grouped by {color_label})" if color_arg else "")

        if chart_type == "Bar Chart":
            fig4 = px.bar(agg_df, x=x_col, y=y_col_name, color=color_arg,
                          title=title_text, barmode="group",
                          labels={x_col: x_label, y_col_name: val_label})
        elif chart_type == "Line Chart":
            fig4 = px.line(agg_df, x=x_col, y=y_col_name, color=color_arg,
                           title=title_text, markers=True,
                           labels={x_col: x_label, y_col_name: val_label})
        else:  # Pie Chart
            names_col = color_col if color_col else x_col
            fig4 = px.pie(agg_df, names=names_col, values=y_col_name,
                          title=title_text)

        st.plotly_chart(_light_layout(fig4), use_container_width=True)
