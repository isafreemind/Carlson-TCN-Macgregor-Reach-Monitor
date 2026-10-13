# Carlson–TCN–Macgregor Reach Monitor

Compare reach. Verify the data.

Tableau comparant les publications originales de **@TuckerCarlson**, **@TCNetwork** et **@DougAMacgregor**. Le lecteur règle le nombre de jours par colonne, compare les périodes et vérifie les calculs publication par publication.

## GitHub Pages

1. Envoyer le projet sur la branche `master` ou `main` du dépôt.
2. Dans **Settings → Pages → Build and deployment → Source**, sélectionner **GitHub Actions**.
3. Le workflow **Deploy GitHub Pages** construit et publie la page à chaque push. Il peut aussi être lancé depuis l’onglet **Actions**.

Adresse attendue après le déploiement : https://isafreemind.github.io/Carlson-TCN-Macgregor-Reach-Monitor/

Seul `_site/` est publié. La page embarque les données nécessaires aux calculs et aux exports ; elle fonctionne sans bibliothèque externe ni serveur applicatif.

## Aperçu local

Python 3.11 ou ultérieur, sans dépendances supplémentaires :

```sh
python build_site.py
python -m http.server 8000 --directory _site
```

Ouvrir http://localhost:8000/. Le fichier `index.html` peut également être ouvert directement. La construction vérifie les identifiants uniques, la période, les comptes et le format des compteurs du jeu de données.

## Vérifier les chiffres

1. Cliquer sur **Vérifier** à côté d’une période et d’un compte.
2. Examiner les publications retenues, leurs compteurs relevés et le calcul détaillé.
3. Ouvrir les publications sur X et télécharger les données en CSV ou JSON pour refaire le calcul.

Les compteurs actuels peuvent avoir augmenté depuis le relevé. Les exports conservent les valeurs utilisées dans le graphique. Vérifier un calcul ne garantit pas l’exhaustivité du jeu de données ni une validation indépendante des compteurs historiques.

## Méthode

- Publications originales et citations incluses ; réponses, réponses à soi-même et reposts exclus.
- Regroupement par date de publication en UTC.
- Vues cumulées observées au moment du relevé, et non vues gagnées durant chaque intervalle.
- Compteurs absents exclus des sommes et moyennes, jamais remplacés par zéro.
- Variation : `(valeur actuelle / valeur précédente − 1) × 100`, calculée avant arrondi. Une valeur précédente nulle ou absente empêche ce calcul.
- Dernière période plus courte signalée. Les publications récentes ont eu moins de temps pour accumuler des vues. Une variation ne démontre pas une causalité.

## Organisation

| Fichier | Rôle |
| --- | --- |
| `dashboard.template.html` | Interface et calculs |
| `build_site.py` | Construction du site statique |
| `data/stats.json` | Publications et compteurs utilisés |
| `.github/workflows/pages.yml` | Déploiement GitHub Pages |

Les pages générées, exports, caches et fichiers privés sont exclus de Git.
