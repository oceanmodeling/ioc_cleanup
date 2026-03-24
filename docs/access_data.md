# Data Access

## Automatic download (transformations only)

The JSON cleaning configs are fetched on demand, so most users do not need to
download anything by hand. `ioc_cleanup` resolves them in this order:

1. the local `transformations/` directory, if you are working inside a clone of
   the repository;
2. otherwise `transformations.tar.gz` is downloaded from Zenodo, checksum
   verified, and unpacked into a local cache.

```python
import ioc_cleanup as C

# Downloads on first use, then reads from the cache.
trans = C.load_transformation("abed", "bub")

# Where the JSON files are stored:
C.resolve_transformation_dir()
# PosixPath('~/.cache/ioc_cleanup/transformations.tar.gz.untar/transformations')

# All available station/sensor configs:
C.get_transformation_paths()
```

The download happens once. The cache lives under `pooch.os_cache("ioc_cleanup")`
(`~/.cache/ioc_cleanup` on Linux, `~/Library/Caches/ioc_cleanup` on macOS) and
can be relocated by setting the `IOC_CLEANUP_CACHE_DIR` environment variable,
which is useful on HPC or shared filesystems. Deleting the cache directory
simply triggers a re-download.

The expected MD5 is pinned in `ioc_cleanup._constants.REGISTRY`, so a truncated
or tampered archive raises an error instead of silently producing bad configs.

The time series themselves (`clean`, `surge`, `raw`) are far too large to fetch
this way and must be downloaded from Zenodo as described below.

## Directly from Zenodo

The full dataset is archived on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22181274.svg)](https://zenodo.org/records/22181274?preview_file=README.md)

### Contents

| Archive | Description | Size |
|---------|-------------|------|
| `raw.tar.gz` | Raw IOC parquet files (per station, per year) | ~23 GB |
| `clean.tar.gz` | Cleaned time series (1 parquet per station) | ~5 GB |
| `surge.tar.gz` | Detided time series (1 parquet per station) | ~14 GB |
| `transformations.tar.gz` | JSON cleaning configurations | ~60 MB |
| `meta.csv` | Station metadata | ~400 KB |

After downloading, extract with:

```bash
tar -xzf clean.tar.gz
tar -xzf surge.tar.gz
tar -xzf transformations.tar.gz
tar -xzf raw.tar.gz
```

Extracting `transformations.tar.gz` into your working directory is optional: it
gives you a local `transformations/` folder, which takes precedence over the
cached download and is what you want if you intend to edit the configs.

## GitHub mirror

Releases are also available on [GitHub](https://github.com/oceanmodeling/ioc_cleanup/releases).

The transformations (JSON configs) and metadata are mirrored there.

For the full dataset (raw + clean + surge), use Zenodo.

## How to cite

If you use this dataset, please cite:

```
Saillour, T. and Mavrogiorgos, P.: Reproducible, transparent and traceable cleaning of IOC Tide Gauge Data,
EGU General Assembly 2026, Vienna, Austria, 3–8 May 2026, EGU26-7777,
https://doi.org/10.5194/egusphere-egu26-7777, 2026.
```

Dataset DOI: [10.5281/zenodo.22181274](https://doi.org/10.5281/zenodo.22181274)
