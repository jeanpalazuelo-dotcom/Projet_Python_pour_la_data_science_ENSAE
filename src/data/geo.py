"""Contours des départements (france-geojson, version simplifiée)."""

from pathlib import Path

import geopandas as gpd
import requests

URL = (
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/"
    "departements-version-simplifiee.geojson"
)
FICHIER = Path("data/raw/departements.geojson")


def telecharger_departements(fichier=FICHIER, forcer=False):
    if not fichier.exists() or forcer:
        r = requests.get(URL, timeout=60)
        r.raise_for_status()
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(r.content)

    carte = gpd.read_file(fichier)
    return carte.rename(columns={"code": "dept", "nom": "nom_dept"})
