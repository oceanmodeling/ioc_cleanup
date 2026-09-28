from __future__ import annotations

import logging
import pathlib

import ioc_cleanup as C

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YEARS = [2020, 2021, 2022, 2023, 2024, 2025]
OVERWRITE = False

DATA_FOLDER = pathlib.Path("./data")
IOC = C.get_meta()


def main():
    for code in IOC.ioc_code:
        text = f"\n{code}"
        for year in YEARS:
            try:
                path = DATA_FOLDER / f"{year}/{code}.parquet"
                if not path.exists() or OVERWRITE:
                    C.download_year_station(code, year, data_folder=DATA_FOLDER)
                    text += f" {year}"
            except Exception:
                text += " x"
        logger.info(text)


if __name__ == "__main__":
    main()
