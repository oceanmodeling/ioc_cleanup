from __future__ import annotations

import holoviews as hv
import pandas as pd
import panel as pn
import pytest
from holoviews import DynamicMap
from holoviews import Overlay

import ioc_cleanup as C
import ioc_cleanup._plots as P
import ioc_cleanup._tools as T

pn.extension()
hv.extension("bokeh")


IOC_SAMPLE = pytest.mark.parametrize(
    "station",
    [
        pytest.param("abur", id="abur"),
        pytest.param("bres", id="bres"),
    ],
)
DEMEAN = True
YEAR = 2020
YEARS = [2020, 2021]
EPS = 1e-6
SCALE = -1.0
# Lower bound on the number of station/sensor configs in the Zenodo archive.
# The record currently ships 442; this only guards against a truncated download.
MIN_TRANSFORMATIONS = 400
IOC = C.get_meta()


@pytest.fixture(scope="session")
def data_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


## Testing download
@IOC_SAMPLE
def test_download_station_data(station, data_dir):
    for year in YEARS:
        C.download_year_station(station, year, data_folder=data_dir)


## Testing cleaning
@IOC_SAMPLE
def test_load_clean_ts_for_year_demean(station, data_dir):
    series, _ = C.load_clean_ts_for_year(
        station=station,
        sensor="rad",
        year=YEAR,
        folder=data_dir,
        demean=True,
    )

    assert isinstance(series, pd.Series)
    assert not series.empty

    meta = C.get_meta()
    meta_row = meta[meta.ioc_code == station]
    stats = C.calc_station_statistics(meta_row, "rad", series)

    assert isinstance(stats, dict)


## Testing the dashboard functions
def test_ui_widgets_exist():
    assert isinstance(P.UI.year, pn.widgets.IntInput)
    assert isinstance(P.UI.surge, pn.widgets.Checkbox)
    assert isinstance(P.UI.demean, pn.widgets.Checkbox)
    assert isinstance(P.UI.station_sensor, pn.widgets.Select)
    assert isinstance(P.UI.apply, pn.widgets.Button)


def test_plot_geographic_coverage_smoke():
    plot = P.plot_geographic_coverage(IOC, ["abur", "abed", "bres"])
    assert isinstance(plot, DynamicMap | Overlay)


def _series():
    return pd.Series(
        [1.0, 2.0, 3.0],
        index=pd.date_range("2020-01-01", periods=3, freq="h"),
    )


def test_print_all_points():
    box = pn.widgets.TextAreaInput()
    P.print_all_points(_series(), [0, 2], box)
    assert "2020-01-01T00:00:00" in box.value


def test_print_range():
    box = pn.widgets.TextAreaInput()
    P.print_range(_series(), [0, 2], box)
    assert box.value.startswith('["2020-01-01T00:00:00"')


def test_print_segment():
    box = pn.widgets.TextAreaInput()
    P.print_segment(_series(), [0, 2], box)
    assert '"offset"' in box.value
    assert '"scale"' in box.value


def _raw_frame():
    return pd.DataFrame(
        {"rad": [1.0, 2.0, 3.0], "prs": [1.0, 2.0, 3.0]},
        index=pd.date_range("2020-01-01", periods=3, freq="h"),
    )


def _transformation(**kwargs):
    return C.Transformation(
        ioc_code="test",
        sensor="rad",
        start=pd.Timestamp("2020-01-01"),
        end=pd.Timestamp("2020-01-02"),
        **kwargs,
    )


def test_transform_scale_offset_defaults_to_noop():
    df = C.transform(_raw_frame(), _transformation())
    pd.testing.assert_series_equal(df["rad"], _raw_frame()["rad"])


def test_transform_applies_scale_and_offset_to_sensor_only():
    df = C.transform(_raw_frame(), _transformation(scale=-1.0, offset=0.5))
    expected = _raw_frame()["rad"] * -1.0 + 0.5
    pd.testing.assert_series_equal(df["rad"], expected)
    # other sensors are untouched
    pd.testing.assert_series_equal(df["prs"], _raw_frame()["prs"])


def test_transform_scale_does_not_resurrect_dropped_values():
    trans = _transformation(scale=-1.0, dropped_timestamps=[pd.Timestamp("2020-01-01T01:00:00")])
    df = C.transform(_raw_frame(), trans)
    assert df["rad"].isna().sum() == 1
    assert df["rad"].iloc[0] == SCALE


def test_inverted_stations_are_flagged_with_negative_scale():
    for station, sensor in (("alak2", "pwl"), ("mona2", "pwl")):
        trans = C.load_transformation(station, sensor)
        assert trans.scale == SCALE


def test_get_notes():
    notes = P.get_notes("adak", "wls")
    assert notes == "After 2022-11 it is good. Before that too many spikes"


def test_transformation_ioc_code_matches_filename():
    paths = C._tools.get_transformation_paths()
    for path in sorted(paths):
        station, sensor = path.stem.rsplit("_", 1)
        t = C.load_transformation(station, sensor)
        assert station == t.ioc_code
        assert sensor == t.sensor


def test_registry_points_at_zenodo_doi():
    assert C._constants.REGISTRY.base_url == f"doi:{C._constants.ZENODO_DOI}/"
    assert C._constants.TRANSFORMATIONS_ARCHIVE in C._constants.REGISTRY.registry


@pytest.mark.zenodo
def test_resolve_transformation_dir_from_zenodo(monkeypatch, tmp_path):
    # Pretend there is no local checkout so the pooch download path is used.
    # The checksum in the registry is verified by pooch itself, so a corrupted
    # or moved archive makes this fail.
    monkeypatch.setattr(C._tools, "JSON_DIR", tmp_path / "missing")
    resolved = C._tools.resolve_transformation_dir()
    assert resolved.is_dir()
    jsons = sorted(resolved.glob("*.json"))
    assert len(jsons) > MIN_TRANSFORMATIONS
    station, sensor = jsons[0].stem.rsplit("_", 1)
    t = C.load_transformation(station, sensor, src_dir=resolved)
    assert t.ioc_code == station


@IOC_SAMPLE
def test_load_surge_tide_switch(station, data_dir):
    clean, _ = P.load_surge_tide(station, "rad", 2020, surge=False, demean=True, folder=data_dir)
    surge, _ = P.load_surge_tide(station, "rad", 2020, surge=True, demean=True, folder=data_dir)
    opts = T.OPTS
    lat = IOC[IOC.ioc_code == station].lat.values[0]
    opts["lat"] = lat
    surge2 = T.surge(clean, opts, T.RESAMPLE)
    pd.testing.assert_series_equal(surge, surge2, rtol=1e-3)
