import matplotlib.pyplot as plt
import numpy as np


def carte(table, colonne, titre, legende, ax=None, cmap="Reds"):
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 7))
    table.plot(
        column=colonne,
        cmap=cmap,
        legend=True,
        legend_kwds={"label": legende, "shrink": 0.6},
        missing_kwds={"color": "lightgrey", "hatch": "///"},  # départements sans donnée
        edgecolor="white",
        linewidth=0.3,
        ax=ax,
    )
    ax.set_title(titre)
    ax.set_axis_off()
    return ax


def cartes_cote_a_cote(table, specs):
    fig, axes = plt.subplots(1, len(specs), figsize=(7 * len(specs), 7), squeeze=False)
    for ax, spec in zip(axes[0], specs):
        carte(table, ax=ax, **spec)
    fig.tight_layout()
    return fig


def nuage(df, x, y, titre, xlabel, ylabel):
    d = df[[x, y]].dropna()
    r = d[x].corr(d[y])

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(d[x], d[y], alpha=0.7)

    a, b = np.polyfit(d[x], d[y], 1)
    xs = np.array([d[x].min(), d[x].max()])
    ax.plot(xs, a * xs + b, color="grey", linestyle="--")

    ax.set_title(f"{titre}\n(r = {r:.2f}, n = {len(d)})")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    return ax

def evolution(df, x, y, groupe, titre, xlabel, ylabel, a_souligner=()):
    # les groupes qu'on ne souligne pas restent en gris, en fond
    fig, ax = plt.subplots(figsize=(9, 5))
    for nom, d in df.sort_values(x).groupby(groupe):
        if nom in a_souligner:
            ax.plot(d[x], d[y], marker="o", linewidth=2, label=nom)
        else:
            ax.plot(d[x], d[y], color="lightgrey", linewidth=1)
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    if a_souligner:
        ax.legend()
    return ax

def nuage_ic(df, x, y, x_bas, x_haut, etiquette, titre, xlabel, ylabel):
    # barres horizontales = intervalle de confiance à 95 % de x
    d = df.dropna(subset=[x, y])
    r = d[x].corr(d[y])

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.errorbar(d[x], d[y], xerr=[d[x] - d[x_bas], d[x_haut] - d[x]], fmt="o", capsize=3)
    for _, ligne in d.iterrows():
        ax.annotate(ligne[etiquette], (ligne[x], ligne[y]), fontsize=8, xytext=(5, 4), textcoords="offset points")

    ax.set_title(f"{titre}\n(r = {r:.2f}, n = {len(d)})")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    return ax

def barres(valeurs, titre, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(8, 5))
    rects = ax.bar(valeurs.index.astype(str), valeurs.values)
    ax.bar_label(rects, fmt="%.2f")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax
