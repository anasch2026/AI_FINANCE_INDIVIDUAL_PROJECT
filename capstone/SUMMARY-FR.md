# Version finale — remise AI for Finance

Les consignes officielles sont désormais lues et incluses. Cette version reprend le commit Claude 7983aa7fd8162d16029ad607fd2e680479649bd2, puis corrige les interprétations et complète le dossier local sans changer les résultats ni relancer une expérience.

**Fichiers à remettre :** manuscript.docx et presentation.pptx (quatre diapositives). Le support presentation-backup.pptx, quinze diapositives, sert uniquement aux questions.

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

Alphas contre la détention passive à parts égales. Périodes effectives différentes : comparaison descriptive, sans test apparié, car le commit historique 9a00fbb manque. Les sept cartes exécutées passent le gate 7 sans annuler leurs échecs précédents ; -0.00 désigne une valeur légèrement négative avant arrondi. Sources : résultats publiés, [results.csv](results.csv) et [results-notes.md](results-notes.md).

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

*Le R² de rendement est sans objet pour les probabilités logistiques ; accuracy, AUC et log-loss évaluent ce classificateur. La règle proxy utilise le signal annuel divisé par douze. Source : [diagnostics.md](diagnostics/diagnostics.md) et ses CSV.

**Vérifications réalisées.**

- Résumé : 211 mots, maximum officiel 250.
- Corps : 2240 mots ; 2344 en incluant les références. Les deux comptages respectent la limite de 2 000 à 3 000.
- Quatre tableaux et six figures ; tous les tableaux numériques sont comparés aux sources archivées.
- Présentation : quatre diapositives, 226 mots prononcés, soit environ 1.61 minute au débit supposé de 140 mots/minute. Une répétition chronométrée personnelle reste nécessaire.
- 718 fichiers d'entrée contrôlés par empreinte ; 779 contrôles réussis.
- Reconstruction documentaire également réussie dans un dossier isolé, sans installation, avec le même environnement. Les CSV numériques et les six figures du manuscrit correspondent octet pour octet.

**Reproductibilité : portée exacte.** Le framework complet, les tests, les dépendances, le registre et les snapshots originaux sont fournis. La commande python -B reproduce.py reconstruit les documents depuis les sorties archivées. Aucune réestimation des modèles ou nouvelle exécution financière n'est revendiquée. La comparaison appariée reste indisponible et aucun test maison ne la remplace.

**Conclusion.** Les stratégies ML initiales ne passent pas la validation. TM-017-10 a de meilleurs constats économiques et de robustesse sur sa fenêtre, mais échoue aux exigences de significativité et d'essais multiples. Les résultats sont négatifs pour les implémentations testées, avec les limites d'échantillon et d'exposition antérieure au holdout clairement conservées.

**Avant dépôt.** Vérifier le rendu natif des deux fichiers principaux, répéter le texte oral et maîtriser les vingt-quatre questions. Mettre la copie finale complète à disposition du correcteur avec des droits d'accès adaptés, puis déposer les livrables avant le début officiel de la session 13. La copie locale n'a pas été publiée automatiquement sur GitHub.
