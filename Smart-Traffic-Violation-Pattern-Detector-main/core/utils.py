from __future__ import annotations

from io import BytesIO

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def build_pdf_report(summary_df: pd.DataFrame, filtered_df: pd.DataFrame) -> bytes:
    buffer = BytesIO()

    with PdfPages(buffer) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")
        ax.set_title("Traffic Violation Pattern Detector Report", fontsize=16, fontweight="bold", pad=20)

        report_lines = []
        for _, row in summary_df.iterrows():
            report_lines.append(f"{row['metric']}: {row['value']}")

        report_lines.extend(
            [
                "",
                f"Filtered records: {len(filtered_df)}",
                f"Locations covered: {filtered_df['location'].nunique() if not filtered_df.empty else 0}",
                f"Violation types covered: {filtered_df['violation_type'].nunique() if not filtered_df.empty else 0}",
            ]
        )

        ax.text(
            0.05,
            0.95,
            "\n".join(report_lines),
            va="top",
            ha="left",
            fontsize=11,
            family="monospace",
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

    buffer.seek(0)
    return buffer.read()
