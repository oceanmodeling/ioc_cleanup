from __future__ import annotations

import datetime

import pydantic


class Transformation(pydantic.BaseModel):
    ioc_code: str
    sensor: str
    notes: str = ""
    skip: bool = False
    wip: bool = False
    start: datetime.datetime
    end: datetime.datetime
    high: float | None = None
    low: float | None = None
    dropped_date_ranges: list[tuple[datetime.datetime, datetime.datetime]] = []
    dropped_timestamps: list[datetime.datetime] = []
    breakpoints: list[datetime.datetime] = []
    tsunami: list[tuple[datetime.datetime, datetime.datetime]] = []
    scale: float = 1.0
    offset: float = 0.0
