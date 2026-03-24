# Transformation JSON schema

Each cleaned station is described by a single JSON file that records every
operation applied to the raw signal: the valid data window, dropped ranges and
timestamps, breakpoints, and tsunami events. Because the cleaning is fully
driven by these configs, the whole dataset is reproducible from the raw IOC
data plus the transformations.

## Getting the transformations

- **Automatic** - `C.load_transformation(station, sensor)` resolves the configs
  for you: it uses the local `transformations/` directory if present, otherwise
  it downloads and caches `transformations.tar.gz` from Zenodo. See
  [Data Access](../access_data.md).
- **Zenodo** - the complete dataset includes `transformations.tar.gz` on the
  [Zenodo record](https://doi.org/10.5281/zenodo.22181274), if you prefer to
  fetch and extract them by hand.
- **GitHub** - the transformations and metadata are also mirrored on the
  [GitHub releases](https://github.com/oceanmodeling/ioc_cleanup/releases),
  and live in the `transformations/` directory of the repository.

## Build your own

You are not limited to the shipped configs. To clean a station yourself, write
a JSON file following the schema below and load it with
`C.load_transformation_from_path(...)`. This lets you adjust the valid window,
drop additional bad ranges, or flag events for stations and periods not yet
covered.

```python
import searvey
import ioc_cleanup as C

station = "abed"
df_raw = searvey.fetch_ioc_station(station, "2020-01-01", "2026-01-01")

trans = C.load_transformation_from_path(
    "my_configs/abed_bub.json"
)

df_clean = C.transform(df_raw, trans)
```

### Example

```json
{
  "ioc_code": "abed",
  "sensor": "bub",
  "notes": "",
  "skip": false,
  "wip": false,
  "start": "2020-01-01T00:00:00",
  "end": "2026-01-01T00:00:00",
  "high": null,
  "low": null,
  "dropped_date_ranges": [
    ["2022-03-27 03:00:00", "2022-03-27 03:45:00"],
    ["2023-03-26 03:00:00", "2023-03-26 03:45:00"]
  ],
  "dropped_timestamps": [
    "2022-09-30T14:45:00",
    "2022-09-30T15:30:00",
    "2022-10-02T06:45:00",
    "2022-10-02T07:00:00",
    "2023-06-21T00:15:00",
    "2024-04-24T11:00:00",
    "2024-09-07 12:00:00"
  ],
  "breakpoints": [],
  "tsunami": []
}
```
### Field descriptions
| Field                 | Description                 |
| --------------------- | --------------------------- |
| `ioc_code`            | IOC station code            |
| `sensor`              | Sensor identifier           |
| `start`, `end`        | Valid data window           |
| `dropped_date_ranges` | Continuous ranges to remove |
| `dropped_timestamps`  | Individual timestamps       |
| `breakpoints`         | Sensor regime changes       |
| `tsunami`             | Eventual tsunami(s) date ranges|
| `skip`                | Ignore station              |
| `wip`                 | Work in progress            |
