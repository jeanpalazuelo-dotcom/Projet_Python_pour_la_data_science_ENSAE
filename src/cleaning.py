import pandas as pd


def est_metropole(dept):
    # "999" = total de la région, "97x" = DROM
    return ~dept.str.startswith("97") & (dept != "999")


def taux_cancer(ameli, annees, niveau="departement"):
    """Taux brut et taux standardisé sur l'âge (pour 100 000 hab.), moyennés sur les années choisies.
    niveau = "departement" ou "region" (Ameli donne le total de chaque région avec dept = "999").

    Standardisation directe avec la structure d'âge de la métropole comme référence.
    Les cases sous secret statistique sont mises à 0 (ce sont surtout des jeunes, quasi aucun cas).
    """
    if niveau == "region":
        garder, cles = ameli["dept"] == "999", ["region"]
    else:
        garder, cles = est_metropole(ameli["dept"]), ["dept", "region"]

    df = ameli[garder & ameli["annee"].isin(annees)].copy()
    df["ntop"] = df["ntop"].fillna(0)

    par_age = df[df["cla_age_5"] != "tsage"].copy()
    par_age["taux"] = par_age["ntop"] / par_age["npop"]

    # même référence pour les deux niveaux, sinon les taux ne seraient pas comparables
    metro = ameli[est_metropole(ameli["dept"]) & ameli["annee"].isin(annees)]
    ref = metro[metro["cla_age_5"] != "tsage"].groupby("cla_age_5")["npop"].sum()
    ref = ref / ref.sum()
    par_age["contrib"] = par_age["taux"] * par_age["cla_age_5"].map(ref)
    std = par_age.groupby(cles + ["annee"])["contrib"].sum().rename("taux_std")

    tot = df[df["cla_age_5"] == "tsage"].set_index(cles + ["annee"])
    brut = (tot["ntop"] / tot["npop"]).rename("taux_brut")

    taux = pd.concat([brut, std], axis=1).reset_index()
    taux = taux.groupby(cles)[["taux_brut", "taux_std"]].mean() * 100_000
    return taux.reset_index()


def tabac_par_region(tabac, annee, sexe="Hommes et Femmes"):
    cols = ["region", "nom_region", "tabac_quotidien", "tabac_ic_bas", "tabac_ic_haut"]
    df = tabac[(tabac["annee"] == annee) & (tabac["sexe"] == sexe)][cols]
    return df.rename(columns={c: f"{c}_{annee}" for c in cols if c.startswith("tabac")})


def construire_table(cancer, tabac, carte):
    # le tabac n'existe qu'au niveau régional : chaque département prend la valeur de sa région
    table = cancer.merge(tabac, on="region", how="left", validate="many_to_one")
    return carte.merge(table, on="dept", how="left", validate="one_to_one")
