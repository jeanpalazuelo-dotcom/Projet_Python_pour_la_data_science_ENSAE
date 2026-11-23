"""Tabagisme quotidien par région, Baromètre santé (Santé publique France, portail Odissé)."""

from pathlib import Path

import pandas as pd
import requests

URL = (
    "https://odisse.santepubliquefrance.fr/api/explore/v2.1/catalog/datasets/"
    "tabac-consommation-quotidienne_reg/exports/csv"
)
FICHIER = Path("data/raw/spf_tabac_region.csv")


def telecharger_tabac(fichier=FICHIER, forcer=False):
    if not fichier.exists() or forcer:
        r = requests.get(URL, params={"delimiter": ";"}, timeout=60)
        r.raise_for_status()
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(r.content)

    df = pd.read_csv(fichier, sep=";", encoding="utf-8-sig", dtype={"reg": str})
    df = df.rename(columns={
        "reg": "region",
        "reglib": "nom_region",
        "tab_quo_v": "tabac_quotidien",
        "tab_quo_icb": "tabac_ic_bas",
        "tab_quo_ich": "tabac_ic_haut",
    })
    return df.drop(columns="tab_quo_typo")
