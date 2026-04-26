from __future__ import annotations

import ioc_cleanup as C

YEARS = [2020, 2021, 2022, 2023, 2024, 2025]
STATION = "abed"


def main():
    for year in YEARS:
        C.download_year_station(STATION, year, data_folder="./data")


if __name__ == "__main__":
    main()
