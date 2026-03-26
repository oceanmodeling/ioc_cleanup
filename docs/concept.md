## Why `ioc_cleanup`?

Cleaning tide gauge data is often:

- :x: manual
- :x: poorly documented
- :x: hard to reproduce
- :x: difficult to review or share

!!! success "`ioc_cleanup` concept:"
    This project proposes a **community-driven, version-controlled**     approach where all cleaning decisions are explicitly **recorded** and **auditable**.


## Concept

The core idea of `ioc_cleanup` is **declarative cleaning**.

Instead of scripts or notebooks, all cleaning decisions are:

- [x] Explicit
- [x] Version controlled
- [x] Human-readable
- [x] Reviewable

Cleaning logic lives entirely in JSON files.

## Why it matters

This methodology allows:

- [x] Flagging:
    * bad or corrupt data (timestamp / data ranges)
    * sensor breakpoints
    * singular phenomena (e.g. tsunamis, meteo-tsunamis, seiches, or unidentified events)
- [x] **Reproducible** cleaning
- [x] **Transparent** and **traceable** decisions stored in plain JSON
- [x] Peer review of cleaning decisions via GitHub
- [x] Easy extension to any other datasets (e.g. [GESLA](https://gesla787883612.wordpress.com/), [NDBC](https://www.ndbc.noaa.gov/))
- [x] Gradual growth in station coverage through community contributions


## Transformations

Each station/sensor pair is described by a JSON file located in:

```
./transformations/
```

These files define the transformation from **raw data → clean signal** by
declaring:

- valid time windows
- dropped timestamps
- dropped ranges
- breakpoints
- notes and metadata

More details in the [JSON format](./reference/json-schema.md)


## Dataset Details

### Cleaned Stations
<iframe
  src="../cleaned_map.html"
  width="100%"
  height="740"
  style="border:none;">
</iframe>

### Data availability in the 2020 - 2025 period

<iframe
  src="../data_availability_map.html"
  width="100%"
  height="590"
  style="border:none;">
</iframe>

<iframe
  src="../data_availability_hist.html"
  width="100%"
  height="320"
  style="border:none;">
</iframe>

### Ratio of data removed in the 2020 - 2025 period

<iframe
  src="../data_removed_map.html"
  width="100%"
  height="590"
  style="border:none;">
</iframe>

<iframe
  src="../data_removed_hist.html"
  width="100%"
  height="320"
  style="border:none;">
</iframe>
