"""Nettoyage des données et construction de la table finale par département."""

import geopandas as gpd
import pandas as pd

TOUS_AGES = "tsage"
TOTAL_REGION = "999"


def est_metropole(dept: pd.Series) -> pd.Series:
    """Vrai pour les départements de métropole (exclut les DROM « 97x » et les totaux « 999 »)."""
    return ~dept.str.startswith("97") & (dept != TOTAL_REGION)


def taux_cancer(ameli: pd.DataFrame, annees: list[int]) -> pd.DataFrame:
    """Calcule, pour chaque département, le taux brut et le taux standardisé sur l'âge.

    Les taux sont exprimés pour 100 000 habitants et moyennés sur les années demandées,
    ce qui lisse les variations aléatoires des petits départements.

    Standardisation directe : on applique les taux par classe d'âge de chaque département
    à la structure par âge de la France métropolitaine (population de référence).
    Les effectifs masqués par le secret statistique (ntop vide) sont comptés comme 0 :
    ils concernent presque uniquement les classes jeunes, où il n'y a quasiment pas de cas.
    """
    df = ameli[est_metropole(ameli["dept"]) & ameli["annee"].isin(annees)].copy()
    df["ntop"] = df["ntop"].fillna(0)

    par_age = df[df["cla_age_5"] != TOUS_AGES].copy()
    par_age["taux_age"] = par_age["ntop"] / par_age["npop"]

    # Structure par âge de référence : part de chaque classe d'âge dans la métropole
    reference = par_age.groupby("cla_age_5")["npop"].sum()
    reference = reference / reference.sum()
    par_age["poids_ref"] = par_age["cla_age_5"].map(reference)

    standardise = (
        par_age.assign(contribution=par_age["taux_age"] * par_age["poids_ref"])
        .groupby(["dept", "region", "annee"])["contribution"]
        .sum()
        .rename("taux_std")
    )

    tous_ages = df[df["cla_age_5"] == TOUS_AGES].set_index(["dept", "region", "annee"])
    brut = (tous_ages["ntop"] / tous_ages["npop"]).rename("taux_brut")

    taux = pd.concat([brut, standardise], axis=1).reset_index()
    resultat = taux.groupby(["dept", "region"])[["taux_brut", "taux_std"]].mean() * 100_000
    return resultat.reset_index()


def tabac_par_region(tabac: pd.DataFrame, annee: int, sexe: str = "Hommes et Femmes") -> pd.DataFrame:
    """Garde la prévalence du tabagisme quotidien d'une année et d'un sexe, une ligne par région."""
    selection = tabac[(tabac["annee"] == annee) & (tabac["sexe"] == sexe)]
    colonnes = ["region", "nom_region", "tabac_quotidien", "tabac_ic_bas", "tabac_ic_haut"]
    return selection[colonnes].rename(
        columns={c: f"{c}_{annee}" for c in colonnes if c.startswith("tabac")}
    )


def construire_table(
    cancer: pd.DataFrame, tabac: pd.DataFrame, carte: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Fusionne cancer (département), tabac (région) et contours (département).

    Chaque département reçoit la valeur de tabagisme de sa région.
    `validate` fait planter la fusion si une clé est dupliquée par erreur.
    """
    table = cancer.merge(tabac, on="region", how="left", validate="many_to_one")
    return carte.merge(table, on="dept", how="left", validate="one_to_one")
