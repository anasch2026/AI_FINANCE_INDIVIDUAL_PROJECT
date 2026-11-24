Travail terminé : TM-017-10 a été verrouillée puis exécutée une seule fois ; le diagnostic a été étendu sans nouvelle stratégie ni calcul de portefeuille. Word et PowerPoint ont été reconstruits.

**Résultats de toutes les cartes.**

| Carte | Premier gate échoué / état | Sharpe IS | Alpha IS (%/an) | Placebos battus (%) | Sharpe holdout | Alpha holdout (%/an) |
|---|---|---:|---:|---:|---:|---:|
| TM-017-01 — Règle simple | 3 | 0.50 | 1.55 | 81.70 | 0.89 | 0.61 |
| TM-017-03 — Elastic Net retirée | Retirée, sans run | — | — | — | — | — |
| TM-017-04 — Random Forest retirée | Retirée, sans run | — | — | — | — | — |
| TM-017-05 — Boosting retirée | Retirée, sans run | — | — | — | — | — |
| TM-017-06 — Elastic Net | 1 | 0.30 | -0.61 | 0.00 | 0.91 | -0.00 |
| TM-017-07 — Random Forest | 2 | 0.08 | -2.07 | 0.90 | 0.79 | -0.15 |
| TM-017-08 — Gradient Boosting | 2 | 0.09 | -1.90 | 1.80 | 0.71 | -0.54 |
| MR-001-01 — Réversion simple | 2 | 0.24 | -1.07 | 37.10 | 0.90 | 1.06 |
| MR-001-02 — Réversion en stress | 2 | 0.08 | -1.37 | 33.70 | 0.78 | 1.04 |
| TM-017-09 — Spécification non exécutée | Sautée au précontrôle | — | — | — | — | — |
| TM-017-10 — Tendance pondérée réparée | 3 | 0.61 | 2.16 | 89.80 | 0.79 | -0.02 |

Alphas contre la détention passive à parts égales. Périodes effectives différentes : comparaison descriptive, sans test apparié, car le commit historique 9a00fbb manque. Les sept cartes exécutées passent le gate 7 sans annuler leurs échecs précédents ; -0.00 désigne une valeur légèrement négative avant arrondi. Sources : résultats publiés, [results.csv](/Users/anaschantah/alpha-factory/capstone/results.csv) et [results-notes.md](/Users/anaschantah/alpha-factory/capstone/results-notes.md).

**Diagnostic étendu : six modèles et la règle proxy.**

| Modèle | R² contre zéro (%) | IC | t de l’IC | Signes corrects (%) | AUC | Log-loss |
|---|---:|---:|---:|---:|---:|---:|
| OLS | -6.77 | -0.06 | -1.26 | 50.40 | — | — |
| Elastic Net | -2.36 | 0.08 | 1.36 | 52.21 | — | — |
| Random Forest | -6.23 | -0.04 | -1.13 | 48.29 | — | — |
| Gradient Boosting | -13.08 | -0.05 | -1.23 | 46.38 | — | — |
| Logistique* | n/a | -0.06 | -1.59 | 48.69 | 0.45 | 0.71 |
| MLP | -15.73 | -0.07 | -1.68 | 45.98 | — | — |
| Règle proxy | -8.03 | 0.06 | 1.13 | 52.41 | — | — |

*R² is not defined for a binary target; the logistic model is judged by accuracy, AUC and log-loss. La règle proxy utilise le signal annuel divisé par douze. Source : [diagnostics.md](/Users/anaschantah/alpha-factory/capstone/diagnostics/diagnostics.md) et ses CSV.

**TM-017-10, en trois lignes.**

- Elle répare uniquement le cas de volatilité indéfinie de TM-017-09, qui reste sans run ni résultat financier.
- Elle passe les gates 1, 2, 6 et 7 : Sharpe IS 0.61, alpha 2.16%/an, part maximale du profit de SPY 28.55%.
- Elle échoue d’abord au gate 3, avec 89.80% des placebos battus contre 90.00% requis ; le DSR de 0.27 échoue aussi au gate 4.

**Diagnostic étendu, en quatre lignes.**

- OLS et MLP ont des R² de rendement négatifs, comme les trois modèles initiaux ; ajouter de la flexibilité ne suffit pas ici.
- La logistique obtient 48.69% de signes corrects, une AUC de 0.45 et une log-loss de 0.71 : prédire directement le signe ne résout pas le problème.
- La volatilité sur 63 séances est la seule importance moyenne de permutation positive pour les deux arbres ; le MLP donne des signes mixtes et la dispersion entre refits est forte.
- Les comparaisons utilisent les mêmes 994 observations sur 142 mois évalués, avant 2023, sans portefeuille ni essai ajouté au registre.

**Conclusion en trois phrases.** Les trois stratégies ML initiales ne passent pas la validation et l’extension montre des prévisions peu convaincantes. TM-017-10 améliore les constats économiques et de robustesse, mais reste rejetée pour significativité puis essais multiples. Ces résultats décrivent les implémentations testées, avec des holdouts antérieurs déjà connus, sans réfuter tout usage du ML en finance.

**Fichiers changés.**

- `alpha-lab/strategies/TM-017-10-volatility-weighted-trend/` : carte, raisonnement, plan, code autonome et rapport officiel ; registre engagé seul, statuts de théorie, index et `STATUS.md` actualisés.
- `capstone/diagnostics/` : script, rapport, mesures et prévisions additionnelles, importances de permutation et graphiques ; anciens chiffres conservés.
- [manuscript.md](/Users/anaschantah/alpha-factory/capstone/manuscript.md) et [manuscript.docx](/Users/anaschantah/alpha-factory/capstone/manuscript.docx) : comparaison étendue, section 5.5, discussion et limites actualisées.
- [presentation.pptx](/Users/anaschantah/alpha-factory/capstone/presentation.pptx), `presentation-outline.md` et `defence-qa.md` : quinze diapositives avec notes, dix-neuf questions.
- `results.csv`, `results-notes.md`, `figures/`, `source-hashes.json` et les brouillons de verdict 09 et 10 : provenance et résultats actualisés.
- Scripts de génération, `README.md`, `STOPPED.md` et `SUMMARY-FR.md`.

Avant soumission, relire la mention n/a du R² logistique, les limites des permutations, la distinction 09 non exécutée / 10 exécutée et la divulgation des holdouts déjà vus. Vérifier la mise en page dans Word et PowerPoint et s’approprier les notes orales. Une seule nouvelle carte a été exécutée, aucun ancien run relancé, aucun réglage après résultat, aucun push.
