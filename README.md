# Tabac et cancer du poumon en France

Projet de groupe du cours *Python pour la data science* (ENSAE 2A, 2026-2027).

## Question

À âge égal, les départements les plus touchés par le cancer du poumon sont-ils ceux des régions où l'on fumait le plus ?
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

| Données | Source | Niveau | Années |
|---|---|---|---|
| Patients traités pour un cancer du poumon, par classe d'âge | Assurance Maladie, data.ameli.fr (API) | Département et région | 2015-2024 |
| Tabagisme quotidien des adultes | Santé publique France, Baromètre santé (API Odissé) | Région | 2000-2021 |
| Contours des départements | france-geojson (IGN) | Département | — |

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

