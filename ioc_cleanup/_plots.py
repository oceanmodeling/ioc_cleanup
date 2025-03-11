from __future__ import annotations

import functools
import operator
import typing as T

import holoviews as hv
import holoviews.streams
import pandas as pd
import panel as pn


def plot_geographic_coverage(
    meta: pd.DataFrame,
    ioc_codes: list[str],
    title: str = "Geographic distribution of stations",
) -> hv.DynamicMap:
    stations_bad = meta[~meta.ioc_code.isin(ioc_codes)]
    stations_good = meta[meta.ioc_code.isin(ioc_codes)]
    plot_bad = stations_bad.hvplot.points(
        x="lon",
        y="lat",
        geo=True,
        tiles=True,
        color="red",
        hover=False,
        use_index=False,
        label="low",
    )
    plot_good = stations_good.hvplot.points(
        x="lon",
        y="lat",
        geo=True,
        tiles=True,
        color="green",
        hover_cols=["location", "country", "ioc_code", "sensor"],
        label="high",
    )
    return (plot_bad * plot_good).opts(title=title)


# Create a function to print selected points
def print_all_points(df: pd.DataFrame, indices: pd.Index[int], text_box: pn.widgets.TextAreaInput) -> T.Any:
    if indices:
        timestamps = [f'    "{df.index[id_].strftime("%Y-%m-%dT%H:%M:%S")}"' for id_ in indices]
        value = ",\n".join(timestamps)
    else:
        value = "No selection!"
    text_box.value = value


def print_range(df: pd.DataFrame, indices: pd.Index[int], text_box: pn.widgets.TextAreaInput) -> T.Any:
    if indices:
        first_ts = df.index[indices[0]]
        last_ts = df.index[indices[-1]]
        value = f'["{first_ts}", "{last_ts}"],'
    else:
        value = "No selection!"
    text_box.value = value


def select_points(df: pd.DataFrame) -> T.Any:
    curve = df.hvplot.line(tools=["hover", "crosshair", "undo"], grid=True, rasterize=True, colorbar=False)
    points = df.hvplot.scatter(tools=["box_select"]).opts(
        color="gray",
        active_tools=["box_zoom"],
        nonselection_color="gray",
        selection_color="red",
        selection_alpha=1.0,
        nonselection_alpha=0.3,
        size=2,
    )
    selection = holoviews.streams.Selection1D(source=points)

    points_all = pn.widgets.TextAreaInput(value="", height=200, placeholder="Selected indices will appear here")  # type: ignore[no-untyped-call]
    points_range = pn.widgets.TextAreaInput(value="", height=200, placeholder="Selected indices will appear here")  # type: ignore[no-untyped-call]

    selection.add_subscriber(lambda index: print_range(df=df, indices=index, text_box=points_range))
    selection.add_subscriber(lambda index: print_all_points(df=df, indices=index, text_box=points_all))

    plot = curve * points
    layout = pn.Column(
        plot.opts(width=1600, height=500),
        pn.Row(
            pn.Column("## Selected Indices:", points_all),
            pn.Column("## Selected Ranges:", points_range),
        ),
    )
    out = pn.panel(layout).servable()
    return out


def compare_dataframes(*dataframes: T.Sequence[pd.DataFrame], title: str = "") -> hv.Layout:
    assert len(dataframes) > 1, "You must pass at least two dataframes!"
    title = title or ""
    options = {
        "tools": ["crosshair", "hover", "undo"],
        "active_tools": ["box_zoom"],
        "width": 1200,
        "height": 500,
        "show_grid": True,
    }
    renamed: list[pd.DataFrame] = []
    for i, df in enumerate(dataframes):
        assert isinstance(df, pd.DataFrame)
        renamed.append(df.rename(columns=({f"{df.columns[0]}": f"{df.attrs['ioc_code']}_{df.attrs['sensor']}_{i}"})))
    plots = functools.reduce(
        operator.add,
        (df.hvplot.line().opts(**options) for df in renamed),
    )
    layout = T.cast(hv.Layout, hv.Layout(plots).cols(1).opts(title=title))
    return layout
