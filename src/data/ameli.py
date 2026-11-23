"""Récupération des effectifs de patients atteints d'un cancer du poumon (Assurance Maladie).

Source : « Cartographie des pathologies et des dépenses », jeu de données `effectifs`
publié en open data sur data.ameli.fr (API Opendatasoft, sans clé).
"""

from pathlib import Path

import pandas as pd
import requests

URL_EXPORT = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets/effectifs/exports/csv"

# Code de la pathologie « Cancer bronchopulmonaire actif » dans la nomenclature Ameli
CODE_CANCER_POUMON = "CAN_BPU_ACT"

FICHIER_CACHE = Path("data/raw/ameli_cancer_poumon.csv")


def telecharger_cancer_poumon(fichier: Path = FICHIER_CACHE, forcer: bool = False) -> pd.DataFrame:
    """Télécharge les effectifs de patients par département, année et classe d'âge.

    Le fichier est mis en cache : s'il existe déjà, on le relit sans rappeler l'API
    (sauf si `forcer=True`).

    Colonnes renvoyées :
        annee      année (2015 à 2024)
        region     code région INSEE
        dept       code département ("999" = ensemble de la région)
        cla_age_5  classe d'âge de 5 ans ("tsage" = tous âges)
        ntop       nombre de patients (vide quand l'effectif est trop petit, secret statistique)
        npop       population couverte par l'Assurance Maladie
    """
    if fichier.exists() and not forcer:
        return lire_cache(fichier)

    parametres = {
        "where": f'top="{CODE_CANCER_POUMON}" and sexe=9',  # sexe=9 : hommes et femmes
        "select": "annee,region,dept,cla_age_5,ntop,npop",
        "delimiter": ";",
    }
    reponse = requests.get(URL_EXPORT, params=parametres, timeout=120)
    reponse.raise_for_status()

    fichier.parent.mkdir(parents=True, exist_ok=True)
    fichier.write_bytes(reponse.content)
    return lire_cache(fichier)


def lire_cache(fichier: Path) -> pd.DataFrame:
    """Lit le CSV en gardant les codes géographiques comme du texte ("01" et non 1)."""
    return pd.read_csv(
        fichier,
        sep=";",
        encoding="utf-8-sig",  # le fichier commence par un BOM
        dtype={"region": str, "dept": str, "cla_age_5": str},
    )
