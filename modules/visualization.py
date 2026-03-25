"""Visualization module."""

from __future__ import annotations

from utils.plotting import bar_distribution, line_timeseries


class VisualizationModule:
    line_timeseries = staticmethod(line_timeseries)
    bar_distribution = staticmethod(bar_distribution)
