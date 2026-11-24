# Couche ML — capstone AI for Finance (TM-017-03 à -05)

## Ce qui est ajouté
- `lab/ml.py` : prévisions walk-forward (fenêtre glissante de 60 mois, refit mensuel, 8 features de prix, Elastic Net / Random Forest / Gradient Boosting), converties en positions au format du lab.
- `strategies/TM-017-03-elastic-net-trend`, `-04-random-forest-trend`, `-05-boosted-trend` : card, reasoning, build plan, strategy.py.
- `tests/test_ml.py` : pas de look-ahead, mémoire respectée, signal planté retrouvé, bruit non (7 tests, passés).
- `requirements.txt` : scikit-learn 1.9.1, joblib 1.6.0, threadpoolctl 3.8.0 épinglés.

Mêmes 7 fonds, mêmes dates de décision, même allocation que TM-017-01 : seule la décision de détenir change, donc `lab.compare` donne la comparaison ML vs règle.

## Ordre des commits (verrou du lab)
1. Pour chaque card : `git add strategies/<id>/card.yaml strategies/<id>/reasoning.md` puis `git commit -m "card: <id>"` (le dossier ne doit contenir que ces deux fichiers au moment du `--check` : mettre build-plan.md et strategy.py de côté pendant cette étape).
2. Puis un commit avec `lab/ml.py`, `requirements.txt`, `tests/test_ml.py`, les `build-plan.md` et `strategy.py`.

## Lancer
```
uv pip install -r alpha-lab/requirements.txt
cd alpha-lab
../.venv/bin/python -m lab.data check
../.venv/bin/python -m pytest
../.venv/bin/python -m lab.report --check strategies/TM-017-03-elastic-net-trend   # puis la commande de run du RUNBOOK
../.venv/bin/python -m lab.compare strategies/TM-017-03-elastic-net-trend strategies/TM-017-01-time-series-momentum
```
Ajouter scikit-learn change le hash de `requirements.txt` et de `lab/` : les rapports existants peuvent être signalés comme à relancer.
