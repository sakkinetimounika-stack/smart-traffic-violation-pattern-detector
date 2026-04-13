from __future__ import annotations

import pandas as pd
import streamlit as st

from core.analysis import train_fine_payment_model
from core.data_loader import load_dataset


@st.cache_data(show_spinner=False)
def load_data_from_path(path: str):
    return load_dataset(path)

@st.cache_data(show_spinner=False)
def load_data_from_upload(file_bytes: bytes):
    from io import BytesIO

    return load_dataset(BytesIO(file_bytes))

@st.cache_resource(
    show_spinner=False,
    hash_funcs={pd.DataFrame: lambda df: int(pd.util.hash_pandas_object(df, index=True).sum())},
)
def get_payment_model(df):
    return train_fine_payment_model(df)
