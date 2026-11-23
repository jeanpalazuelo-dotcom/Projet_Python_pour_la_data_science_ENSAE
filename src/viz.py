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
