from __future__ import annotations

APP_TITLE = "Traffic Violation Pattern Detector"
APP_ICON = "\U0001F6A6"

PAGE_HOME = "\U0001F3E0 Home"
PAGE_DASHBOARD = "\U0001F4CA Dashboard"
PAGE_ADVANCED = "\U0001F4C8 Analytics"
PAGE_PREDICTIONS = "\U0001F52E Prediction"
PAGE_REPORTS = "\U0001F4C4 Reports & Downloads"
PAGE_UPLOAD = "\U0001F4E4 Upload File"
PAGE_VISUALIZATION = "\U0001F5A5\uFE0F Data Visualization"
PAGE_TRENDS = "\U0001F4C9 Trend Analysis"

NAV_ITEMS = [
    PAGE_HOME,
    PAGE_DASHBOARD,
    PAGE_ADVANCED,
    PAGE_VISUALIZATION,
    PAGE_TRENDS,
    PAGE_PREDICTIONS,
    PAGE_REPORTS,
    PAGE_UPLOAD,
]

METRIC_STYLES = {
    "total": {"bg": "linear-gradient(135deg, #ef4444 0%, #be123c 100%)", "icon": "\U0001F6A8"},
    "risk": {"bg": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "icon": "\U0001F4CD"},
    "pending": {"bg": "linear-gradient(135deg, #10b981 0%, #047857 100%)", "icon": "\u23F3"},
    "speed": {"bg": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)", "icon": "\u26A1"},
}
