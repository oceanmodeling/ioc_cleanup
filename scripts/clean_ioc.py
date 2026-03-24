from __future__ import annotations

import logging
import pathlib

import ioc_cleanup as C

logger = logging.getLogger(__name__)

OVERWRITE = True

clean_folder = pathlib.Path("./clean")
clean_folder.mkdir(exist_ok=True)

clean_candidates = C._tools.get_transformation_paths()


def process_station(code: pathlib.Path) -> None:
    station, sensor = code.stem.split("_")
    logger.info(f" > cleaning station {station}, sensor {sensor}")
    outpath = clean_folder / f"{station}_{sensor}.parquet"

    if outpath.exists() and not OVERWRITE:
        return

    t = C.load_transformation(station, sensor)
    if t.skip:
        logger.warning(f"skip flag active for station {station}")
        return

    ts = C.load_station(station)
    if ts.empty:
        logger.warning(f"no valid data for station {station}")
        return

    ts_clean = C.clean(ts, station, sensor)
    ts_clean.attrs["sensor"] = sensor
    ts_clean.to_frame(name=sensor).to_parquet(outpath)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    for code in clean_candidates:
        process_station(code)


if __name__ == "__main__":
    main()
