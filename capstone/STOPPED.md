# Exécution arrêtée — verrou historique de TM-017-03

Date : 11 novembre 2026.

## Erreur exacte

Commande, depuis `alpha-lab/`, avec l'environnement `.venv` activé :

```sh
nohup python -m lab.report strategies/TM-017-03-elastic-net-trend > /tmp/run-TM-017-03.log 2>&1 &
```

Sortie exacte du journal `/tmp/run-TM-017-03.log` ; code de sortie du processus : 1.

```text
refused: alpha-lab/strategies/TM-017-03-elastic-net-trend/card.yaml: the commit that locked the card holds other files; the card is committed alone
```

## Cause et règle d'arrêt

Le commit de verrouillage `add09ac8ad52738b4cecae1fb93554acc6c36764`, intitulé `card: TM-017-03-elastic-net-trend` et signé par Anas Chantah, contient ces deux fichiers :

- `alpha-lab/strategies/TM-017-03-elastic-net-trend/card.yaml`
- `alpha-lab/strategies/TM-017-03-elastic-net-trend/reasoning.md`

La fonction `locked()` de `alpha-lab/lab/report.py` exige que ce commit contienne uniquement `card.yaml`. Le briefing décrit un verrou contenant la carte et son raisonnement ; le contrôle historique du runner est donc plus strict que cette description. `--check` accepte la carte, mais ne réalise pas ce contrôle historique, qui intervient au lancement réel.

Un nouveau commit ne peut pas retirer `reasoning.md` d'un ancien commit. Corriger le verrou existant demanderait de réécrire l'historique, de modifier le runner, ou de remplacer la carte. Ces actions sont interdites ou hors du périmètre autorisé. Aucun contournement n'a été tenté. Conformément à l'instruction d'arrêt, aucun autre run ni travail de rédaction des résultats n'a été lancé.

## Vérifications achevées avant le refus

- `python -m pytest tests/test_ml.py -q` : les 7 tests sont passés. Deux avertissements concernent une corrélation indéfinie sur une série constante.
- `--check` : accepté pour les trois cartes, dans l'ordre 03, 04, 05.
- `--try` : terminé avec un code de sortie nul pour les trois cartes. Aucune rupture de chronologie ou de mémoire ; quatre fenêtres voisines vérifiées par carte ; aucune fenêtre voisine identique à la base.
- Les décisions indépendantes indiquées par `--try` sont respectivement 17, 102 et 122. Le seuil du gate 1 est 30 ; Elastic Net présente donc un problème de nombre de décisions, sans qu'un verdict de batterie ait été produit.
- Elastic Net a affiché des avertissements de convergence pendant `--try`. Aucun paramètre ni code n'a été modifié pour les supprimer.

Ces vérifications ne produisent pas de rendements et ne remplacent pas un run.

## État des trois cartes après l'arrêt

Une lecture de `registry.opened()` et de `registry/trials.jsonl` après le refus a confirmé, pour chacune des cartes 03, 04 et 05 : `opened: None` et `registry_lines: 0`. Aucun holdout n'a été ouvert et aucune ligne de registre n'a été ajoutée. Il n'y a donc aucune modification du registre à engager séparément.

Le premier lancement détaché avait disparu sans sortie, avant tout enregistrement par le lab. L'absence de processus, de marqueur d'ouverture et de ligne au registre a été vérifiée avant de corriger uniquement la persistance de la session shell. Le lancement conservé dans une session ouverte a ensuite produit le refus reproduit ci-dessus. Aucun run enregistré n'a été relancé.

Les stratégies et les fichiers préexistants du lab sont inchangés. Aucun dépôt distant n'a été ajouté ; aucun push ni réécriture de commit n'a été effectué. Aucun `verdict.md` du lab n'a été écrit.

## Livrables suspendus

Les comparaisons `lab.compare`, les brouillons de verdict, `results.csv`, les graphiques, le manuscrit Markdown et Word, le plan de présentation et les questions de soutenance ne sont pas produits : ils dépendent de runs qui n'ont pas eu lieu. Aucun chiffre financier n'est inventé ou déduit des seuls tests de positions.

## Complément du 11 novembre 2026 — runs 06–08 achevés, comparaisons indisponibles

Ce complément conserve intégralement le premier refus ci-dessus. Les cartes de remplacement TM-017-06, TM-017-07 et TM-017-08 ont ensuite été exécutées une seule fois, dans cet ordre, après réussite des 7 tests ML et des contrôles `--check` et `--try`. Les trois processus se sont terminés normalement, avec un code de sortie nul. Après chaque run, le registre a été engagé seul, puis le notebook et STATUS.md dans un autre commit, sous le nom d'Anas Chantah. Aucun échec de gate n'a été traité comme une erreur à corriger.

Les trois commandes officielles de comparaison ont été tentées, depuis `alpha-lab/` :

```sh
python -m lab.compare strategies/TM-017-06-elastic-net-trend strategies/TM-017-01-time-series-momentum
python -m lab.compare strategies/TM-017-07-random-forest-trend strategies/TM-017-01-time-series-momentum
python -m lab.compare strategies/TM-017-08-boosted-trend strategies/TM-017-01-time-series-momentum
```

Chacune s'est terminée avec un code de sortie 1 et la même erreur exacte :

```text
refused: TM-017-01-time-series-momentum: the commit of its run cannot be read (git diff --name-only 9a00fbb81b360dbaf6df5e2a66aa575eb1954aee -- strategy.py: fatal: bad object 9a00fbb81b360dbaf6df5e2a66aa575eb1954aee)
```

Les sorties sont conservées dans `.git/codex-logs/compare-TM-017-06-elastic-net-trend.log`, `.git/codex-logs/compare-TM-017-07-random-forest-trend.log` et `.git/codex-logs/compare-TM-017-08-boosted-trend.log`.

Le registre de la stratégie de référence nomme un commit que le dépôt local ne contient pas. La commande locale `git cat-file -t 9a00fbb81b360dbaf6df5e2a66aa575eb1954aee` confirme l'absence de l'objet ; `git rev-parse --is-shallow-repository` renvoie `false`. L'historique local du fichier de stratégie de référence commence au commit d'importation `da87875`. La comparaison refuse donc de vérifier que la stratégie actuelle est celle du run historique, avant tout calcul de différence.

Récupérer un historique depuis un autre dossier ou depuis Internet est interdit par la règle absolue de cette session. Modifier le registre historique, le lab, la stratégie de référence, ou recréer un historique pour contourner ce contrôle ne serait pas une correction autorisée. Aucun de ces actes n'a été tenté. Les différences officielles contre TM-017-01 restent indisponibles ; aucun calcul maison ne les remplace. Ce refus concerne les comparaisons, pas les trois runs ML, dont les résultats restent enregistrés et exploitables.

Anas a demandé une pause pendant cette étape. Les deux comparaisons déjà lancées ont été laissées se terminer ; ce complément termine la consignation de l'étape en cours. Aucun autre run, aucune nouvelle étape et aucune finalisation des livrables ne seront lancés avant son message « continue ».

## Complément — phase 2 et final autorisés le 11 novembre 2026

La nouvelle demande explicite d'Anas autorise la rédaction autonome des livrables dans `capstone/`, sans reprendre les runs ni tenter de réparer les comparaisons. La pause mentionnée ci-dessus appartient à l'historique. Les résultats des notebooks de 01, 06, 07 et 08 sont désormais utilisés pour une comparaison descriptive uniquement. La comparaison appariée reste indisponible ; aucun calcul maison ne la remplace.

Les périodes déclarées sont communes, mais les notebooks publient des périodes effectives différentes : la règle commence le 1er février 2006, les modèles le 2 février 2011, et tous terminent le 30 décembre 2022. Les versions des seuils diffèrent également : version 1 pour la règle, version 4 pour les modèles. Ces limites sont indiquées dans les livrables.

<!-- Sources : alpha-lab/strategies/TM-017-01-time-series-momentum/report.ipynb ; alpha-lab/strategies/TM-017-06-elastic-net-trend/report.ipynb ; alpha-lab/strategies/TM-017-07-random-forest-trend/report.ipynb ; alpha-lab/strategies/TM-017-08-boosted-trend/report.ipynb ; cellules 4 et 24. -->

La vérification bibliographique en ligne et l'accès à des consignes ou outils stockés hors du dépôt sont omis : ils exigeraient un accès extérieur à `~/alpha-factory`, interdit par la règle absolue. Les références retenues sont des publications connues ; Anas doit vérifier leurs notices sur ses propres copies avant soumission. Aucun nouveau document Blackboard n'a été consulté. Aucune application externe n'est utilisée pour ouvrir ou convertir le Word ; l'export et la vérification de sa structure sont réalisés avec les bibliothèques déjà présentes dans `.venv`. Les polices et les caches des graphiques restent dans le dépôt.

Les brouillons ne constituent ni des `verdict.md` du lab ni une nouvelle validation financière. Aucun fichier du lab, aucune carte et aucune ligne du registre ne sont modifiés pendant cette phase.

## Complément — diagnostic, unique nouvelle carte et finalisation

La demande suivante d'Anas autorise explicitement un diagnostic in-sample, au plus deux nouvelles cartes, leurs runs et les livrables finaux. Une seule nouvelle carte a été dessinée : MR-001-01-monthly-liquidity-reversal. Aucun code ni carte déjà exécuté n'a été modifié ou relancé. Les seules modifications de fichiers préexistants du lab sont celles expressément prévues par ce nouveau périmètre : statut de MR-001, index et STATUS.md régénérés, et ajout officiel au registre.

Le diagnostic utilise le chargeur local avec un adaptateur de lecture limité à 2022-12-31 avant l'assemblage du marché ; il exécute les sources ML inchangées et ne calcule aucun rendement de stratégie. Les fichiers et graphiques sont dans capstone/diagnostics/. Le commit 2762800 conserve les résultats antérieurs au dessin de la nouvelle carte.

La nouvelle carte a été verrouillée seule au commit 11e268a, avant son code au commit 1d7b19b. --check et --try ont réussi : 205 décisions, aucune rupture de chronologie ou de mémoire, quatre voisins testés et aucun identique à la base. Le run officiel unique s'est terminé avec un code de sortie nul et un premier échec au gate 2. Son journal et son PID sont dans .git/codex-logs/run-MR-001-01-monthly-liquidity-reversal.*, sans utilisation de ps. Le registre a été engagé seul dans a31cfd5, puis le rapport et STATUS.md dans aa76374. Aucun second essai ni nouvelle carte n'a suivi le résultat. Le statut final de la théorie est tested-inconclusive.

Les anciens résultats holdout de 06–08 étaient déjà connus avant le diagnostic et le nouveau dessin. Le raisonnement et les livrables le déclarent. Aucun nouveau calcul sur 2023–2025 n'est fait hors du run du lab ; l'exploitation ultérieure des résultats holdout se limite aux chiffres déjà publiés par les notebooks. Cette discipline ne rend pas le même calendrier globalement inconnu : la nouvelle expérience reste un suivi exploratoire.

La comparaison appariée demeure indisponible et n'est pas remplacée. Aucune recherche bibliographique en ligne, consultation de Blackboard, installation ou ouverture d'un fichier hors de ~/alpha-factory n'est effectuée. Le rendu visuel du Word et du PowerPoint dans une application externe est omis, car il nécessiterait un accès extérieur au dossier autorisé. Leur structure, leurs tables, images et notes sont vérifiées localement avec les bibliothèques déjà installées ; la mise en page finale reste à relire avant soumission.

## Deux règles supplémentaires imposées par Anas — résultat et saut obligatoire

Anas a fixé intégralement MR-001-02 et TM-017-09 dans la même instruction, avant leurs vérifications et tout run de ces cartes. MR-001-02 est le suivi numéro 2, TM-017-09 le numéro 3. Les holdouts antérieurs de 06–08 et MR-001-01 étaient déjà connus ; ce fait figure dans les raisonnements. Aucune ancienne carte ni stratégie n'est modifiée ou relancée.

MR-001-02 : verrou seul 85b0ff2, code ultérieur 41dbd85. --check et --try passent : 92 décisions, aucune rupture de chronologie ou de mémoire, quatre voisins distincts. Son unique run officiel termine normalement et échoue d'abord au gate 2. Le registre est engagé seul dans 818bb2c, puis le rapport et STATUS.md dans 00408dc. Son journal et son PID restent dans .git/codex-logs/run-MR-001-02-stress-conditioned-reversal.*. Aucun second run n'est lancé.

TM-017-09 : verrou seul 547df95, code ultérieur 6d5ac29. --check passe ; --try est refusé avec code de sortie 1, avant tout run réel. Erreur exacte, conservée dans .git/codex-logs/try-TM-017-09-volatility-weighted-trend.log :

```text
refused: undefined inverse-volatility denominator on 2006-03-01: tradable fund(s) without a defined full 63-session volatility: DBC; the fixed rule supplies no exclusion, imputation or fallback
```

La règle impose une somme sur TOUS les fonds tradables, même non détenus. DBC est tradable dès le 2006-02-06 selon data/manifest.json et lab/universe.py, mais ne dispose pas encore des 63 rendements nécessaires à sa volatilité au 2006-03-01. Le dénominateur exact est donc indéfini sur une décision comportant d'autres positions. Un sum() ignorant les NaN exclurait silencieusement DBC ; raccourcir la fenêtre, imputer une volatilité, définir un plancher, différer la date de départ ou tout passer en cash changerait également la règle. L'implémentation lève cette erreur au lieu de choisir un substitut.

Conformément à l'instruction explicite « If a rule below cannot be implemented exactly as written ... skip that card », TM-017-09 est sautée, sans run réel ni nouveau test financier. registry.opened() renvoie None et aucune ligne du registre ne porte son identifiant. Ses gates sont non exécutés et ses chiffres financiers restent vides. Son code et sa carte verrouillés ne sont pas modifiés ; aucune carte de remplacement n'est inventée. Il y a donc trois cartes de suivi spécifiées au total, deux exécutées et une sautée, et non trois essais financiers. Seule MR-001-02 ajoute un essai à la correction du gate 4 lors de cette demande.

Les livrables finaux distinguent ce saut d'un échec financier. Les anciens chiffres sont conservés ; les nouveaux chiffres proviennent exclusivement du notebook de MR-001-02. Aucun calcul de rendement ni inspection de données brutes 2023–2025 n'a lieu hors des commandes officielles du lab. Les statuts de MR-001 et TM-017 restent tested-inconclusive pour les formes effectivement testées. Aucun accès hors du dépôt, aucune installation, aucun réseau et aucun push.

## Réparation autorisée TM-017-10 et extension des prévisions

Anas a ensuite autorisé exactement une carte supplémentaire, TM-017-10, parent=null. Elle répare uniquement le cas indéfini de TM-017-09 : un fonds sans volatilité définie n'est ni détenu ni inclus dans la somme. Aucun résultat financier de 09 n'existe et sa carte et son code restent inchangés. Les autres règles et paramètres sont ceux imposés par Anas avant le run ; les holdouts antérieurs étaient déjà connus et déclarés.

Verrou seul : b3dc647 ; code ultérieur : 47b5dca. --check et --try passent : 203 décisions, aucune rupture de chronologie ou de mémoire, quatre voisins distincts. L'unique run se termine normalement, avec un premier échec au gate 3. Son journal, PID et code de sortie sont dans .git/codex-logs/run-TM-017-10-volatility-weighted-trend.*. Le registre est engagé seul dans fe8c43e, puis le rapport et STATUS.md dans f308b34. Le verdict capstone et le statut tested-inconclusive sont engagés ensuite. Aucun nouveau réglage, run ou carte ne suit ce résultat.

La deuxième partie est une extension de prévisions seulement : OLS, logistique L2 et petit MLP, avec les paramètres fixés par Anas, les huit mêmes variables et les mêmes estimations mensuelles sur 60 mois. Le protocole est engagé avant évaluation dans 8a7dd60. Tous les intrants sont tronqués avant assemblage à 2022-12-31. Les importances par permutation utilisent uniquement le mois suivant chaque estimation dans cet échantillon, avec dix répétitions et random_state=0 ; aucun rendement de portefeuille, position, run du lab ou essai de registre n'est ajouté par ces modèles. Les chiffres des trois anciens modèles et du proxy sont conservés ; les observations et historiques d'estimation originaux ne sont pas réécrits.

La logistique prévoit le signe. Son R² est donc calculé contre zéro sur sa cible binaire, explicitement distinct du R² de rendement des régressions ; il ne constitue pas une prévision calibrée de rendement. L'AUC, la log-loss et le taux de bons signes sont indiqués. Les importances de permutation ont pour unité l'augmentation de MSE du mois suivant en points de base au carré ; elles peuvent être négatives et ne sont pas assimilées à une importance causale. Le journal et le PID du diagnostic sont dans .git/codex-logs/extended-forecast-diagnostics.* ; son code de sortie est nul.

La demande porte ainsi à quatre les cartes de suivi spécifiées, trois exécutées et une non exécutée (09), réparée par 10. Cette phase ajoute une seule ligne au registre, pour 10. La comparaison appariée historique reste indisponible ; aucune méthode maison ne la remplace. Aucun accès hors du dépôt, réseau, installation, réécriture d'historique ou push. Le rendu des documents dans une application externe reste omis sous la règle de périmètre ; leur structure, leurs chiffres, figures et notes sont contrôlés localement.
