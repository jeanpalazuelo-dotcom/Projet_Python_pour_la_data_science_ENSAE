"""Récupération des contours des départements de France métropolitaine.

Source : dépôt GitHub « france-geojson » (Grégoire David), construit à partir des
données de l'IGN. Version simplifiée, plus légère et suffisante pour des cartes.
"""

from pathlib import Path

import geopandas as gpd
import requests

URL_GEOJSON = (
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/"
    "departements-version-simplifiee.geojson"
)

FICHIER_CACHE = Path("data/raw/departements.geojson")


def telecharger_departements(fichier: Path = FICHIER_CACHE, forcer: bool = False) -> gpd.GeoDataFrame:
    """Renvoie un GeoDataFrame avec une ligne par département métropolitain.

    Colonnes : dept (code département, ex. "59", "2A"), nom_dept, geometry.
    """
    if not fichier.exists() or forcer:
        reponse = requests.get(URL_GEOJSON, timeout=60)
        reponse.raise_for_status()
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(reponse.content)

    carte = gpd.read_file(fichier)
    return carte.rename(columns={"code": "dept", "nom": "nom_dept"})
