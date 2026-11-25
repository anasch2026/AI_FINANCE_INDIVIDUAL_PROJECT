# Reprise du capstone dans Claude Code en ligne

## Ce dossier est une copie de travail documentaire

Le projet original se trouve sur le Mac d'Anas Chantah. Cette archive permet de
reprendre dans le dépôt GitHub AI_FINANCE_INDIVIDUAL_PROJECT connecté à Claude
Code en ligne. Le chemin /Users/anaschantah/alpha-factory n'existe pas dans le
conteneur cloud : ne cherche pas à y accéder.

Dans cette session cloud, la racine autorisée est la racine du dépôt courant,
celle où cette archive a été extraite. Tous les travaux et fichiers temporaires
restent dans ce dépôt. Les chemins Mac des anciens documents sont historiques.

Cette copie contient les livrables, leurs sources, les métriques sauvegardées et
les cartes/rapports utiles. Elle ne contient ni les données de marché brutes, ni
.venv, ni .git, ni le registre complet. Ce n'est pas un environnement de backtest
à réinstaller. Ces absences sont voulues et ne sont pas des erreurs à réparer.
Les références aux commits décrivent l'historique original resté sur le Mac ;
ne prétends pas que ces objets Git existent dans ce nouveau dépôt et ne tente
pas de reconstruire cet historique.

## Mission actuelle

Communique en français simplement. Le rapport et les diapositives sont en anglais.
Le capstone AI for Finance d'Anas Chantah (Master in Finance, IE Business School,
professeur Josep Gisbert) est expérimentalement terminé. L'objectif est maintenant
la relecture, la cohérence, la mise en forme et la préparation de la soutenance.

Ne lance aucune stratégie, aucun backtest, aucun notebook, aucun entraînement,
aucune nouvelle évaluation de prévisions et aucun calcul de rendement.
Ne crée aucune carte, ne change aucun paramètre, seuil ou résultat.
Ne modifie aucun fichier de alpha-lab : les cartes et rapports sont des archives.
Ne télécharge rien et n'installe rien. N'accède à aucun service externe ou secret.
Ne réécris pas l'historique Git et ne configure aucun remote.
Travaille autonomement, sans question de confirmation pour la lecture initiale.
N'effectue aucune publication, fusion ou remise du projet à la place d'Anas.

## À lire avant de travailler

1. CLAUDE.md et ce document.
2. capstone/SUMMARY-FR.md et capstone/README.md.
3. capstone/manuscript.md et capstone/results-notes.md.
4. capstone/diagnostics/diagnostics.md.
5. capstone/presentation-outline.md et capstone/defence-qa.md.
6. capstone/STOPPED.md, en respectant sa chronologie.
7. capstone/results.csv et les CSV diagnostiques uniquement comme sources.
8. handoff/AGENTS-MAC-HISTORICAL.md, alpha-lab/RUNBOOK.md et
   alpha-lab/ML-CAPSTONE.md pour le contexte historique.

Les anciennes listes de tâches de ces derniers fichiers sont périmées : ne
lance pas les runs, comparaisons, installations ou diagnostics qu'elles citent.
Les instructions de cette reprise cloud définissent la tâche actuelle.

## Conclusions et distinctions à conserver

Aucune stratégie étudiée ne passe les sept gates. TM-017-01 échoue d'abord au
3 ; TM-017-06 au 1 ; TM-017-07 et 08 au 2 ; MR-001-01 et 02 au 2 ; TM-017-10 au 3.
Les cartes 03 à 05 sont retirées sans run. TM-017-09 est sautée au précontrôle,
sans résultat financier ; seule sa réparation distincte TM-017-10 a été exécutée.
Une réussite du holdout n'annule pas un échec antérieur.

TM-017-10 manque le gate 3 (89.80% de placebos battus contre 90.00%) et échoue
aussi au gate 4 (DSR 0.27 contre 0.90). Ne la présente pas comme quasi validée.
La comparaison avec la référence est descriptive : le commit original 9a00fbb
manque, les périodes effectives diffèrent et les seuils historiques aussi.
Ne tente ni réparation ni comparaison appariée maison.

Le diagnostic compare six modèles plus une règle proxy, mais OLS, logistique et
MLP n'ont aucun portefeuille ni verdict de trading. Dans tous les tableaux et
graphiques publiés, le R² logistique est n/a. Les scores historiques archivés dans
les CSV/JSON ne doivent pas être réintroduits comme R² dans les livrables.
Ne réécris pas ces fichiers numériques. Accuracy, AUC et log-loss évaluent le
classificateur. Le diagnostic est limité aux observations antérieures à 2023.

La volatilité sur 63 séances est la seule importance de permutation moyenne
positive pour les deux modèles d'arbres. Ce constat n'est pas causal. TM-017-10
utilise la volatilité pour pondérer plutôt que prédire, et sa règle a été fixée
avant le diagnostic étendu. Les holdouts antérieurs avaient déjà été vus : le
manuscrit expose cette limite et ne doit pas être rendu plus confirmatoire.

Alpha Factory est un framework préexistant cofondé avec Sami Andaloussi, utilisé
comme outil d'évaluation. La contribution de cours est la couche ML, les
diagnostics, les hypothèses, les expériences et l'analyse. La déclaration d'aide
par Claude et OpenAI Codex et l'attribution du travail antérieur doivent rester.

## Documents et génération

- Manuscrit source : capstone/manuscript.md ; export : manuscript.docx.
- Présentation : capstone/presentation.pptx, avec quinze diapositives et notes.
- Source du PowerPoint : capstone/build_presentation.py.
- Export Word et figures financières : capstone/build_capstone.py.
- Notes de soutenance : presentation-outline.md ; dix-neuf questions : defence-qa.md.
- Dernier graphique de la diapositive 9 :
  capstone/diagnostics/07-tree-permutation-importance.png.
  Titre : Only volatility helps out of sample.
  Source : permutation-summary.csv ; valeurs affichées en milliers de bp².

Les scripts de génération ne relancent pas les stratégies, mais ils ont été
préparés pour l'environnement .venv du Mac, notamment local_plotting.py.
Ne suppose pas que ce .venv existe dans le cloud. Vérifie d'abord les dépendances
et chemins en lecture seule. N'exécute pas les scripts s'ils exigent un accès
hors du dépôt ou une installation. Dans ce cas, poursuis la relecture et les
modifications textuelles autorisées ; indique clairement quels exports restent
à reconstruire localement. N'affirme jamais avoir régénéré un document sans
l'avoir fait. Ne lance surtout pas diagnostics.py ou son option --extend.

Une future demande explicite de mise en forme peut autoriser l'adaptation des
seuls scripts documentaires dans cette copie cloud, sans changement scientifique.
Après toute modification autorisée, vérifie la conservation des nombres,
provenances, tableaux, figures et notes. Ne touche pas aux rapports archivés.
Les nouveaux commits de travail doivent être attribués à Anas Chantah : vérifier
l'identité sans falsifier ou réécrire un auteur existant.

## Première tâche après extraction

Commence en lecture seule. Confirme que tu vois manuscript.md, manuscript.docx,
presentation.pptx, results.csv et les consignes de reprise. Lis les documents,
puis donne une courte synthèse en français : état du projet, incohérences
éventuelles et vérifications prioritaires avant remise. Ne reconstruis rien et
ne recommence aucune expérience. N'attends pas de question supplémentaire.

La grille détaillée Blackboard n'a pas été fournie. Ne prétends pas vérifier la
conformité à une grille absente. La mise en page finale dans les applications
Word/PowerPoint et la maîtrise personnelle de l'oral restent à vérifier par Anas.

## Traçabilité

Le fichier TRANSFER-MANIFEST.json indique les empreintes des fichiers originaux
inclus et le commit de départ du Mac. Les documents générés de reprise et le
manifeste sont des ajouts de transfert ; les livrables d'origine sont inchangés.
Cette copie cloud ne synchronise pas automatiquement le dossier du Mac.
