from __future__ import annotations

import pathlib

import pandas as pd

DATA_DIR = pathlib.Path("data")
SPLIT_DIR = pathlib.Path("split")
TRANSFORMATIONS_DIR = pathlib.Path("transformations")

START = pd.Timestamp("2020-01-01T00:00:00")
END = pd.Timestamp("2026-01-01T00:00:00")
