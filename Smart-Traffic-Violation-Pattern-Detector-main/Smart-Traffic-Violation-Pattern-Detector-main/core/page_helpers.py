from __future__ import annotations

import pandas as pd


def build_context(filtered_df: pd.DataFrame, risk_df: pd.DataFrame) -> dict[str, object]:
    payment_series = (
        filtered_df["Fine_Paid"].astype(str).str.strip().str.lower()
        if "Fine_Paid" in filtered_df.columns
        else pd.Series(dtype=str)
    )
    pending_count = int(payment_series.eq("no").sum()) if not payment_series.empty else 0
    high_risk_count = int(risk_df["risk_level"].eq("High").sum()) if not risk_df.empty else 0
    return {
        "total": int(len(filtered_df)),
        "risk": high_risk_count,
        "pending": pending_count,
        "speed": round(float(filtered_df["speed"].mean()), 1) if not filtered_df.empty else 0.0,
    }


def summarize_counts(df: pd.DataFrame, column: str, top_n: int | None = None) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "count"])

    summary = (
        df[column]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace({"": "Unknown"})
        .value_counts()
        .rename_axis(column)
        .reset_index(name="count")
    )
    if top_n is not None:
        summary = summary.head(top_n)
    return summary
