# Contrôle contre les consignes officielles

Sources : instructions/AI_for_Finance_Capstone_Guidelines.pdf, sections 2 à 7 ; instructions/AI_for_Finance_Capstone_Rubric.pdf, critères 1 à 5. Il s'agit d'un contrôle de preuves et de limites, pas d'une auto-attribution de note.

| Exigence | Preuve dans cette version | État |
|---|---|---|
| Type A : objectif économique et benchmark | Section 1 : allocation mensuelle, Sharpe net, alpha, coûts et décision de validation | Présent |
| Résumé de 250 mots maximum, résultats chiffrés | 215 mots ; dataset, modèles, résultats et verdict | Vérifié |
| Corps de 2 000 à 3 000 mots | 2306 hors références, 2410 avec références | Vérifié |
| Cinq sections officielles | Abstract ; Introduction and Business Problem ; Data and Methodology ; Empirical Results ; Conclusion and Implementation Risks | Vérifié |
| Traitement des données et modèle | Retards, labels achevés, fenêtre glissante, données manquantes, pooling, hyperparamètres et CV interne | Présent ; limites du scaler et de l'early stopping déclarées |
| Valeur financière et robustesse | Tables 2 et 3 : Sharpe, alpha, coûts, placebos, stabilité et DSR | Concordance avec les rapports vérifiée |
| Analyse d'erreurs | Table 4, diagnostic par année, coefficients et permutations | Sources conservées, pas de causalité revendiquée |
| Risques de mise en œuvre | Section 4 : surapprentissage, limites des données, charge de calcul et préparation réglementaire | Présent, sans prétendre avoir mesuré les coûts de calcul ou validé une conformité juridique |
| Code documenté et dépendances | README, requirements, framework/tests complets et snapshots gelés | Fourni |
| Reconstruction de tous les tableaux et figures | python -B reproduce.py ; verify_submission.py ; contrôle dans un second dossier | Exécutée et vérifiée depuis les sorties sauvegardées |
| Réestimation indépendante des expériences | Code et données fournis, mais aucune expérience relancée à cette étape | Non effectuée et non présentée comme effectuée |
| Présentation de deux minutes maximum | 4 diapositives, 240 mots ; estimation à débit explicite | Support prêt ; débit réel à chronométrer par Anas |
| Déclaration IA et travail antérieur | Annexe A, licence MIT et attribution Sami Andaloussi | Conservés |
| Responsabilité individuelle | defence-qa.md et texte oral | À maîtriser personnellement par Anas |

## Limites à conserver

Les exemples de drawdown et turnover figurent dans le critère de validation financière, mais aucun de ces deux indicateurs n'est publié dans les rapports fournis. Ils ne sont ni inventés ni assimilés au coût annuel. Les métriques disponibles et cette limite sont exposées. Les comparaisons de performance entre fenêtres différentes restent descriptives. L'absence du commit historique 9a00fbb empêche toujours la comparaison appariée officielle. Les holdouts antérieurs déjà vus et les cartes retirées/non exécutées restent déclarés.

## Rendu visuel

Le manuscrit a été exporté puis rendu par LibreOffice en dix pages, toutes inspectées. Les quatre diapositives principales et les quinze diapositives de secours ont été rendues et inspectées. Les colonnes du Word, la lisibilité des tableaux, les légendes et la présentation des probabilités logistiques ont été corrigées. Il s’agit d’un contrôle du rendu LibreOffice, pas d’une affirmation sur toutes les versions de Microsoft Office.

## Dernière relecture

Voir capstone/RELECTURE-FINALE.md. Les contrôles supplémentaires vérifient aussi la concordance de tous les paragraphes, légendes et figures du Word avec ses sources, le texte oral et le tableau financier des diapositives. Les chiffres des expériences et du diagnostic restent identiques.
