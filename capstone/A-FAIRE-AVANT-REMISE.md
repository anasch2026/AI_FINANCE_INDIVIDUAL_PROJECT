# À faire avant la remise (début de la session 13)

Ce qui est prêt dans ce dépôt : manuscrit conforme aux consignes (corps du texte d'environ
2 300 mots, résumé chiffré de 211 mots, cinq sections imposées, risques de mise en œuvre), Word
reconstruit, présentation de 2 minutes en 4 diapositives (227 mots, environ 1 min 40), support de
secours de 15 diapositives (à reconstruire), 24 questions de soutenance, README de reproduction.

Ce qui suit ne peut être fait que depuis ton Mac. Le point 1 pèse le plus dans la note
(critère 4, 20 points).

## 1. Rendre les expériences reproductibles (indispensable pour viser 9/10)

La grille exige un dépôt qui « runs from start to finish and reproduces every result ».
Aujourd'hui, ce dépôt ne contient ni le framework (`alpha-lab/lab/`), ni ses tests, ni
`alpha-lab/requirements.txt`, ni les données. Il faut :

1. Obtenir l'accord de Sami Andaloussi pour publier le framework, puis ajouter dans ce dépôt
   `alpha-lab/lab/` (dont `ml.py`), `alpha-lab/tests/`, `alpha-lab/requirements.txt`,
   `alpha-lab/templates/`, le registre et `capstone/diagnostics/diagnostics.py` dans sa version
   exécutable. Sans cela, seul le critère « documents reconstruits depuis les sorties sauvegardées »
   est satisfait.
2. Données : les prix Yahoo ne sont probablement pas redistribuables. Fournir un script qui
   retélécharge les sept ETF et vérifie les empreintes de `alpha-lab/data/manifest.json`, en
   précisant qu'un nouveau téléchargement peut différer du snapshot gelé.
3. Vérifier avec Sami comment un tiers peut réexécuter une carte dans un clone neuf (le lab refuse
   de relancer une carte déjà enregistrée), puis documenter la commande exacte dans `README.md`.
4. Tester le tout dans un clone propre, sur une autre machine si possible, et noter la durée.

## 2. Reconstruire les exports qui demandent matplotlib

Depuis la racine, avec le `.venv` activé :

```bash
python -B capstone/build_capstone.py
```

```bash
python -B capstone/build_presentation.py
```

Le premier régénère aussi `results.csv`, les figures et le Word, avec les mêmes chiffres.
Le second produit `presentation-backup.pptx`, qui contient encore l'ancienne version tant qu'il
n'est pas reconstruit.

## 3. Optionnel : drawdown et turnover

La grille cite le drawdown et le turnover, que les rapports ne publient pas. Les calculer serait
une analyse descriptive nouvelle, après résultats : à faire seulement si tu l'assumes, en le
déclarant comme tel dans le manuscrit. Sinon, la limite est déjà écrite en section 4.

## 4. Contrôles personnels

- Ouvrir `manuscript.docx` dans Word et `presentation.pptx` dans PowerPoint : mise en page,
  police Aptos, titres sur une ligne.
- Chronométrer `defence-script.md` à voix haute : moins de 2 minutes.
- Savoir expliquer seul les questions 20 à 24 de `defence-qa.md` (coûts, DSR, placebos,
  drawdown, déploiement), ainsi que les 17 décisions d'Elastic Net.
- Vérifier les cinq références sur tes propres copies.
- Déposer les deux devoirs Blackboard (manuscrit avec le lien GitHub, présentation) avant le début
  de la session 13.
