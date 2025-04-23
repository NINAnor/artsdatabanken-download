#!/usr/bin/env python3

import csv
import logging
import pathlib

import requests
import tqdm

## Parameters

SPECIES_PATH = pathlib.Path("species.txt")
OUTPUT_PATH = pathlib.Path("output.csv")

# areas = ""
areas = "5001"  # Trondheim

# from_date = None  # no filter
from_date = "01.01.2000"  # from 2000

polygon = None  # do not further filter by WKT polygon
# polygon = "POLYGON ((254967.13 7034042.43,254967.13 7040148.92,258669.4678 7040138.5445,258721.3453 7034073.5565,254967.13 7034042.43))"  # noqa: E501


API = "https://artskart.artsdatabanken.no/publicapi/"
TIMEOUT = 60


fields = [
    "Id",
    "ScientificName",
    "TaxonId",
    "Sex",
    "Status",
    "Count",
    "Behavior",
    "Locality",
    "Habitat",
    "Latitude",
    "Longitude",
    "Precision",
    "East",
    "North",
    "Projection",
    "Institution",
    "Collector",
    "CollectedDate",
]

terms = []
# empty species.txt file would disable the species filter:
#   all species are downloaded
with SPECIES_PATH.open() as species:
    for line in species.readlines():
        line = line.strip()
        if not line:
            continue
        terms.append(line)


def get_taxon_from_scientificname(term):
    taxons = requests.get(
        f"{API}/api/taxon/short", params={"term": term}, timeout=TIMEOUT
    ).json()
    for result in taxons:
        if result["ScientificName"] == term:
            return str(result["IntId"])


def get_observations_from_taxon(taxons):
    params = {
        "Taxons": taxons,
        "Areas": areas,
        "FromDate": from_date,
        "pageSize": 1000,
        "filter.wktPolygon": polygon,
    }
    results = requests.get(
        f"{API}/api/observations/list", params=params, timeout=TIMEOUT
    ).json()
    yield from results["Observations"]
    total = results["TotalPages"]
    for index in tqdm.tqdm(range(1, total), desc="Pages", leave=False):
        params["pageIndex"] = index
        results = requests.get(
            f"{API}/api/observations/list", params=params, timeout=TIMEOUT
        ).json()
        yield from results["Observations"]


def main():
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, dialect="excel")
        writer.writerow(fields)
        ids = []
        for term in terms:
            scientificname = get_taxon_from_scientificname(term)
            if scientificname:
                ids.append(scientificname)
            else:
                logging.warning(f"Term {term} not found")
        taxons = ",".join(ids)
        observations = get_observations_from_taxon(taxons)
        for observation in observations:
            writer.writerow(str(observation[field]) for field in fields)


if __name__ == "__main__":
    main()
