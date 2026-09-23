# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature du dépôt

Ce dépôt applique un cycle de développement piloté par des documents, en phases successives : **Intent → Design (spec) → Build**. Le produit `mars-rover` est en phase Build : son code Python est dans `src/mars_rover/`, ses tests dans `tests/`.

Tout le contenu (documents, skills, messages de commit, titres de PR) est rédigé en français.

## Commandes

Le `python3` du système est en 3.9. Le projet exige Python 3.12 et s'installe avec `uv` dans `.venv` :

- installer : `uv venv --python 3.12 && uv pip install -e '.[dev]'`
- lancer tous les tests : `.venv/bin/pytest -q`
- lancer un seul test : `.venv/bin/pytest tests/test_api.py::test_malformed_json_is_rejected`
- lancer l'API en local : `.venv/bin/uvicorn mars_rover.api:app --reload`

## Organisation

- `intent/<slug>/intent.md` : l'intention d'un produit (problème, résultat proposé, utilisateurs, contraintes, questions ouvertes).
- `intent/<slug>/spec.md` : la spécification de cette intention, dans le même dossier.
- `intent/<slug>/plan.md` : le plan de réalisation de la phase Build.
- `.claude/skills/intent/SKILL.md` : skill qui formalise une intention.
- `.claude/skills/spec/SKILL.md` : skill invoquée uniquement par `/spec <chemin de l'intent.md>` (`disable-model-invocation`).
- `.claude/skills/clean-code/SKILL.md` : skill de lisibilité du code, utilisée pour la planification, l'implémentation et la relecture.
- `src/mars_rover/` : le cœur de simulation (`direction`, `grid`, `commands`, `simulation`) ne dépend pas de FastAPI. `api.py` traduit le JSON et transforme toute erreur (`InvalidRequest` ou validation Pydantic) en réponse 400 `{"error": …}`.
- `tests/` : un fichier de tests par module.

Produit en cours : `mars-rover` (simulateur exposé via l'API `POST /simulations`). Sa spec contient les exigences `EX-xx`, les réserves `R-xx` et les questions `Q-xx`.

## Gouvernance et flux Git

- Le **Product Owner** accepte chaque phase en mergeant sa pull request vers `main`. Claude ne merge jamais une PR, ne déclare jamais un document accepté et ne tranche aucune décision produit à la place du PO.
- Chaque phase est réalisée sur sa propre branche `claude/<phase>-<slug>` (par exemple `claude/intent-mars-rover`, `claude/spec-mars-rover`), créée depuis `main`.
- Une spec ne se rédige qu'à partir d'une intention dont l'acceptation est vérifiable, c'est-à-dire mergée dans `main` via une PR.
- Pas de commit, de push ni de PR sans la confirmation explicite de l'utilisateur. Chaque commit ne concerne que le document de la phase en cours.
- Messages de commit courts, en français, à l'indicatif : « Ajoute l'intention … », « Ajoute la spec … », « Ajoute la skill … ».
- Les points non tranchés restent visibles dans `Questions ouvertes` ou `Réserves`. Chaque décision humaine est consignée avec son auteur connu, sa date et sa justification. N'invente ni auteur ni accord.
- La rubrique « Contexte de génération » de `spec.md` conserve le prompt exact et le commit Git de chaque skill utilisée. Vérifie ces commits (`git log -1 --format=%H -- <chemin du SKILL.md>`) plutôt que de les supposer.

## Outillage

Le CLI `gh` n'est pas installé sur ce poste. Après un push, donne à l'utilisateur le lien de création de PR renvoyé par `git push`.

## Erreurs récurrentes

Lorsqu’une même erreur se répète deux fois, propose une instruction courte et précise pour l’éviter. Appuie-toi sur les erreurs observées et fais valider cette instruction avant de l’ajouter à CLAUDE.md.

Si une instruction devient obsolète, propose sa correction ou son retrait et attends la validation avant de modifier le fichier.
