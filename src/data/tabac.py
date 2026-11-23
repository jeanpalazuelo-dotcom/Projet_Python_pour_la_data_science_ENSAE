"""Récupération de la prévalence du tabagisme quotidien par région (Santé publique France).

Source : Baromètre de Santé publique France, jeu de données
`tabac-consommation-quotidienne_reg` publié sur le portail Odissé (API Opendatasoft, sans clé).
Prévalence chez les adultes, éditions 2000, 2005, 2010, 2014, 2017 et 2021.
"""

from pathlib import Path

import pandas as pd
import requests

URL_EXPORT = (
    "https://odisse.santepubliquefrance.fr/api/explore/v2.1/catalog/datasets/"
    "tabac-consommation-quotidienne_reg/exports/csv"
)

FICHIER_CACHE = Path("data/raw/spf_tabac_region.csv")

# Noms de colonnes plus lisibles que ceux de la source
RENOMMAGE = {
    "reg": "region",
    "reglib": "nom_region",
    "tab_quo_v": "tabac_quotidien",
    "tab_quo_icb": "tabac_ic_bas",
    "tab_quo_ich": "tabac_ic_haut",
}


def telecharger_tabac(fichier: Path = FICHIER_CACHE, forcer: bool = False) -> pd.DataFrame:
    """Télécharge la prévalence du tabagisme quotidien (en %) par région, année et sexe.

    Le fichier est mis en cache dans data/raw/ ; s'il existe déjà, on le relit
    sans rappeler l'API (sauf si `forcer=True`).

    Colonnes renvoyées :
        annee            année de l'enquête
        region           code région INSEE
        nom_region       nom de la région
        sexe             "Hommes", "Femmes" ou "Hommes et Femmes"
        tabac_quotidien  part de fumeurs quotidiens (%)
        tabac_ic_bas, tabac_ic_haut  intervalle de confiance à 95 %
    """
    if not fichier.exists() or forcer:
        reponse = requests.get(URL_EXPORT, params={"delimiter": ";"}, timeout=60)
        reponse.raise_for_status()
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_bytes(reponse.content)

    df = pd.read_csv(fichier, sep=";", encoding="utf-8-sig", dtype={"reg": str})
    return df.rename(columns=RENOMMAGE).drop(columns="tab_quo_typo")
