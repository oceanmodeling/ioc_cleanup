from __future__ import annotations

import pathlib
from importlib.metadata import version

import pandas as pd
import pooch

ZENODO_DOI = "10.5281/zenodo.22181274"

REGISTRY = pooch.create(
    path=pooch.os_cache("ioc_cleanup"),
    base_url=f"doi:{ZENODO_DOI}/",
    # Allows users to relocate the cache, e.g. on shared/HPC filesystems.
    env="IOC_CLEANUP_CACHE_DIR",
    registry={
        "transformations.tar.gz": "md5:4d8665afbba1adb6f724c85e990acf03",
    },
)

TRANSFORMATIONS_ARCHIVE = "transformations.tar.gz"

DATA_DIR = pathlib.Path("data")
SPLIT_DIR = pathlib.Path("split")
TRANSFORMATIONS_DIR = pathlib.Path("transformations")

START = pd.Timestamp("2020-01-01T00:00:00")
END = pd.Timestamp("2026-01-01T00:00:00")

METADATA = {  # from https://github.com/orgs/oceanmodeling/discussions/26
    "cleaning_method": "https://github.com/oceanmodeling/ioc_cleanup",
    "cleaning_method_version": version("ioc_cleanup"),
    "standard_name": "sea_surface_height_above_reference_ellipsoid",
    "long_name": "Sea surface height",
    "water_level_type": "total_water_level",
    "tidal_component": "included",
    "description": "IOC sea-level data downloaded from https://www.ioc-sealevelmonitoring.org/",
    "units": "m",
    "source": "ioc",
    "featureType": "timeSeries",
    "cf_role": "timeseries_id",
}
