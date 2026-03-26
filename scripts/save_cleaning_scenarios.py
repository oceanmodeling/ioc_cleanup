from __future__ import annotations

from pathlib import Path

import hvplot.pandas  # noqa: F401
import pandas as pd
import panel as pn

import ioc_cleanup as C
from ioc_cleanup._plots import plot_line
from ioc_cleanup._plots import plot_points

IOC = C.get_meta()
RSMP = 2


def save_interactive_plot(
    station: str,
    sensor: str,
    folder: Path,
    start: pd.Timestamp,
    end: pd.Timestamp,
    html_out: str,
    *,
    clean: bool = False,
    surge: bool = False,
) -> None:
    item = IOC[IOC.ioc_code == station].iloc[0]
    if clean:
        ts = C._plots.load_surge_tide(station, sensor, start.year, surge=surge, demean=True)
    else:
        ts = C._searvey.load_station(station, folder, 2020, 2026).sort_index()
        ts = ts[sensor]
        if surge:
            ts = ts.loc[f"{start.year}" : f"{start.year+1}"]
            args = C._tools.OPTS
            args["lat"] = item.lat
            ts = C._tools.surge(ts, args, rsmp=RSMP)

    subset = ts.loc[start:end]
    plot_ = (plot_line(subset) * plot_points(subset)).opts(
        height=700,
        title=f"{item.ioc_code} - {item.location} ({item.country})",
    )

    pane_ = pn.Row(
        pn.pane.HoloViews(
            plot_.opts(responsive=True),
            sizing_mode="stretch_width",
            height=700,
        ),
        width_policy="max",
    )
    pane_.save(html_out)


RUNS = [
    {
        "station": "ouis",
        "sensor": "rad",
        "start": "2024-10-15",
        "end": "2024-10-29",
        "out": "docs/spikes.html",
    },
    {
        "station": "maya",
        "sensor": "pwl",
        "start": "2023-09-01",
        "end": "2023-09-05",
        "out": "docs/example.html",
    },
    {
        "station": "maya",
        "sensor": "pwl",
        "start": "2023-09-01",
        "end": "2023-09-05",
        "out": "docs/example_clean.html",
        "clean": True,
    },
    {
        "station": "marsh",
        "sensor": "rad",
        "start": "2020-08-07",
        "end": "2020-08-21",
        "out": "docs/unknown.html",
    },
    {
        "station": "LA23",
        "sensor": "rad",
        "start": "2021-11-03",
        "end": "2021-11-14",
        "out": "docs/seiche.html",
    },
    {
        "station": "cres",
        "sensor": "pwl",
        "start": "2025-07-29",
        "end": "2025-08-03",
        "out": "docs/tsunami.html",
    },
    {
        "station": "cres",
        "sensor": "pwl",
        "start": "2025-07-29",
        "end": "2025-08-03",
        "out": "docs/tsunami_detided.html",
        "surge": True,
    },
    {
        "station": "chst",
        "sensor": "prs",
        "start": "2023-07-29",
        "end": "2023-09-01",
        "out": "docs/noise.html",
        "clean": True,
        "surge": True,
    },
    {
        "station": "work",
        "sensor": "bub",
        "start": "2021-03-27",
        "end": "2021-03-29",
        "out": "docs/step_simple.html",
        "surge": True,
    },
    {
        "station": "mala",
        "sensor": "ra2",
        "start": "2023-06-27",
        "end": "2023-07-16",
        "out": "docs/step_long.html",
    },
    {
        "station": "LI11",
        "sensor": "rad",
        "start": "2025-01-28",
        "end": "2025-02-03",
        "out": "docs/flat.html",
    },
]

DATA_DIR = Path("./data")

for cfg in RUNS:
    save_interactive_plot(
        folder=DATA_DIR,
        start=pd.Timestamp(cfg.pop("start")),
        end=pd.Timestamp(cfg.pop("end")),
        html_out=cfg.pop("out"),
        **cfg,
    )
