"""Plotting helper wrappers."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def line_timeseries(df: pd.DataFrame, x: str, y: str, color: str | None = None):
    return px.line(df, x=x, y=y, color=color)


def bar_distribution(df: pd.DataFrame, x: str, y: str | None = None):
    return px.bar(df, x=x, y=y)
