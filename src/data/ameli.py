"""Patients traités pour un cancer du poumon, par département et classe d'âge (data.ameli.fr)."""

from pathlib import Path

import pandas as pd
import requests

URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets/effectifs/exports/csv"
FICHIER = Path("data/raw/ameli_cancer_poumon.csv")


def telecharger_cancer_poumon(fichier=FICHIER, forcer=False):
    if not fichier.exists() or forcer:
        params = {
            "where": 'top="CAN_BPU_ACT" and sexe=9',  # cancer bronchopulmonaire actif, tous sexes
            "select": "annee,region,dept,cla_age_5,ntop,npop",
            "delimiter": ";",
        }
        r = requests.get(URL, params=params, timeout=120)
        r.raise_for_status()
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(r.content)

    # on garde les codes en texte sinon "01" devient 1
    return pd.read_csv(
        fichier,
        sep=";",
        encoding="utf-8-sig",
        dtype={"region": str, "dept": str, "cla_age_5": str},
    )
