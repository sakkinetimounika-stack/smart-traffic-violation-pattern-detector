from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
from typing import BinaryIO

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "location",
    "violation_type",
    "vehicle_type",
    "speed",
    "helmet_detected",
    "signal_status",
]

DATASET_COLUMN_MAP = {
    "Date": "date",
    "Location": "location",
    "Violation_Type": "violation_type",
    "Vehicle_Type": "vehicle_type",
    "Recorded_Speed": "speed",
    "Helmet_Worn": "helmet_detected",
    "Traffic_Light_Status": "signal_status",
    "Time": "time",
}


def _read_csv(source: str | Path | BytesIO | BinaryIO) -> pd.DataFrame:
    if hasattr(source, "read"):
        raw = source.read()
        if isinstance(raw, bytes):
            return pd.read_csv(BytesIO(raw))
        return pd.read_csv(StringIO(raw))
    return pd.read_csv(source)


def load_dataset(source: str | Path | BytesIO | BinaryIO) -> pd.DataFrame:
    """Load and normalize a traffic violation dataset."""
    df = _read_csv(source)
    df = df.rename(columns=DATASET_COLUMN_MAP)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(
            "Dataset is missing required columns after normalization: "
            + ", ".join(missing)
        )

    if "time" not in df.columns:
        df["time"] = "00:00"

    normalized = df.copy()
    normalized["date"] = pd.to_datetime(
        normalized["date"], errors="coerce", dayfirst=True
    )
    normalized["time"] = normalized["time"].fillna("00:00").astype(str).str.strip()
    normalized["event_time"] = pd.to_datetime(
        normalized["date"].dt.strftime("%Y-%m-%d") + " " + normalized["time"],
        errors="coerce",
    )
    normalized["location"] = (
        normalized["location"].fillna("Unknown").astype(str).str.strip()
    )
    normalized["violation_type"] = (
        normalized["violation_type"].fillna("Unknown").astype(str).str.strip()
    )
    normalized["vehicle_type"] = (
        normalized["vehicle_type"].fillna("Unknown").astype(str).str.strip()
    )
    normalized["speed"] = pd.to_numeric(normalized["speed"], errors="coerce").fillna(0)
    normalized["helmet_detected"] = (
        normalized["helmet_detected"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace({"Yes": "Detected", "No": "Not Detected", "N/A": "Unknown"})
    )
    normalized["signal_status"] = (
        normalized["signal_status"].fillna("Unknown").astype(str).str.strip()
    )
    normalized["hour"] = normalized["event_time"].dt.hour.fillna(0).astype(int)
    normalized["day_name"] = normalized["date"].dt.day_name().fillna("Unknown")
    normalized["month"] = normalized["date"].dt.to_period("M").astype(str)

    normalized = normalized.dropna(subset=["date"]).reset_index(drop=True)
    return normalized


def validate_dataset(df: pd.DataFrame) -> tuple[bool, list[str]]:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    return not missing, missing
