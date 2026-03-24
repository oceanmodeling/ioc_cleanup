# Python API

This page documents the **public Python API** of `ioc_cleanup`.
Only stable, user-facing functions are listed here.

---

## Transformations & Cleaning

Functions related to loading, applying, and managing cleaning transformations.

::: ioc_cleanup.load_transformation
::: ioc_cleanup.load_transformation_from_path
::: ioc_cleanup.resolve_transformation_dir
::: ioc_cleanup.get_transformation_paths

::: ioc_cleanup.transform
::: ioc_cleanup.clean

---

## Surge & Signal Processing

Utilities for tidal analysis, demeaning, and surge extraction.

::: ioc_cleanup.surge

---

## Station Metadata

Access to IOC station metadata and geographic information.

::: ioc_cleanup.get_meta

---

## Data Download

Helpers for downloading and storing IOC raw data.

::: ioc_cleanup.download_raw
::: ioc_cleanup.download_year_station

---

## Data Loading

Utilities for loading archived IOC data from disk.

::: ioc_cleanup.load_station

---

## Models

Core data models used by the cleaning workflow.

::: ioc_cleanup.Transformation
