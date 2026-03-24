# IOC Cleanup

`ioc_cleanup` provides a reproducible, transparent, and traceable workflow
for cleaning tide gauge data from [IOC](https://www.ioc-sealevelmonitoring.org/list.php) (Intergovernmental Oceanographic Commission) stations worldwide.

## IOC Cleanup database
All stations with clean data between 1st of January 2020 and the 31st of december 2025.

<iframe
  src="assets/cleaned_map.html"
  width="100%"
  height="740"
  style="border:none;">
</iframe>


## Getting Started

### Installation

```bash
git clone https://github.com/seareport/ioc_cleanup.git
pip install -r requirements.txt
```

### Minimal example
```python
import searvey
import ioc_cleanup as C

station = "abed"
df_raw = searvey.fetch_ioc_station(station, "2020-01-01", "2026-01-01")

trans = C.load_transformation(station, "bub")

df_clean = C.transform(df_raw, trans)
```

## JSON transformations

Each cleaned station is described by a single JSON file that records every
operation applied to the raw signal, so the dataset is fully reproducible from
the raw IOC data plus the transformations.

- **Automatic** - `C.load_transformation(station, sensor)` downloads and caches
  them from Zenodo on first use. See [Data Access](access_data.md).
- **Zenodo** - the complete dataset includes `transformations.tar.gz`, if you
  prefer to fetch them by hand.
- **GitHub** - also mirrored on the
  [GitHub releases](https://github.com/oceanmodeling/ioc_cleanup/releases).
- **Build your own** - follow the [JSON schema](reference/json-schema.md) and
  load it with `C.load_transformation_from_path(...)`.

## Example for `maya` station:

### From raw signal...
<iframe
  src="assets/example.html"
  width="100%"
  height="710"
  style="border:none;">
</iframe>

 ... using [JSON transformation](reference/json-schema.md) ...

### ... to clean signal
<iframe
  src="assets/example_clean.html"
  width="100%"
  height="710"
  style="border:none;">
</iframe>
