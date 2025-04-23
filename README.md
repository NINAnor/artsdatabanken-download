# artsobservasjoner-download

This program downloads observations from `artskart.artsdatabanken.no/publicapi`.
Observations are exposed on GBIF too, but artsdatabanken.no API provide the latest version.

API documentation is available at [artskart.artsdatabanken.no/PublicApi/Help](https://artskart.artsdatabanken.no/PublicApi/Help).

## Configuration

1. Open `artsobservasjoner.py`
2. Change `areas`
3. Add or remove fields in `fields`
4. Write species in `species.txt` (one per line)

## Run

```
uv run artsobservasjoner.py
```

Open `output.csv`.
