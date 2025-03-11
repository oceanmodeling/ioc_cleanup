from __future__ import annotations

import typing as T

import geopandas as gpd
import pandas as pd
import searvey.ioc


def get_meta() -> gpd.GeoDataFrame:
    meta_web = searvey.get_ioc_stations()
    meta_api = (
        pd.read_json("http://www.ioc-sealevelmonitoring.org/service.php?query=stationlist&showall=all")
        .drop_duplicates()
        .rename(columns={"Code": "ioc_code"})
    )

    merged = pd.merge(
        meta_web.drop(columns=["lon", "lat", "geometry"]),
        meta_api[["ioc_code", "Lon", "Lat"]].rename(columns={"Lon": "lon", "Lat": "lat"}).drop_duplicates(),
        on=["ioc_code"],
    )
    merged = T.cast(
        gpd.GeoDataFrame,
        merged.assign(geometry=gpd.points_from_xy(merged.lon, merged.lat, crs="EPSG:4326")),
    )
    return merged


def download_raw(ioc_codes: list[str], start: pd.Timestamp, end: pd.Timestamp) -> dict[str, pd.DataFrame]:
    no_codes = len(ioc_codes)
    start_dates = pd.DatetimeIndex([start] * no_codes)
    end_dates = pd.DatetimeIndex([end] * no_codes)
    dataframes: dict[str, pd.DataFrame] = searvey._ioc_api._fetch_ioc(
        station_ids=ioc_codes,
        start_dates=start_dates,
        end_dates=end_dates,
        http_client=None,
        rate_limit=None,
        multiprocessing_executor=None,
        multithreading_executor=None,
        progress_bar=False,
    )
    return dataframes
