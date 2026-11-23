# Tabac, pollution et cancer du poumon en France

Projet de groupe du cours *Python pour la data science* (ENSAE 2A, 2026-2027).

## Question

Comment expliquer les écarts de mortalité par cancer du poumon entre départements français : tabac, pollution de l'air ou conditions sociales ?

## Installation

```bash
git clone https://github.com/jeanpalazuelo-dotcom/Projet_Python_pour_la_data_science_ENSAE.git
cd Projet_Python_pour_la_data_science_ENSAE
pip install -r requirements.txt
nbstripout --install
cp .env.example .env   # puis y mettre sa clé INSEE
```

Ouvrir ensuite `rapport.ipynb` et lancer toutes les cellules.

## Données

| Données | Source |
|---|---|
| Mortalité par cancer du poumon | CépiDc-Inserm, Géodes (Santé publique France) |
| Ventes de tabac par département | OFDT |
| Pollution de l'air (PM2.5, NO₂) | Géod'air |
| Revenu, pauvreté, catégories sociales | INSEE |
| Contours des départements | IGN / Etalab |

Les données sont téléchargées automatiquement par les fonctions de `src/data/` et mises en cache dans `data/raw/`.

## Organisation du dépôt

```
├── rapport.ipynb          rapport final
├── src/
│   └── data/              une fonction de récupération par source
├── data/
│   ├── raw/               données téléchargées (non versionnées)
│   └── processed/         table finale
└── notebooks/exploration/ brouillons
```

## Auteurs

- Palazuelo Jean
- Ilyan Radjabaly

