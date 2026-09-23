# Plan de réalisation : Simulateur Mars Rover

Intention de référence : [intent.md](intent.md)
Spécification de référence : [spec.md](spec.md) (acceptée par merge de la PR #2 dans main)

Ce plan n'est pas accepté. Aucune pull request n'est prévue pour la phase Build (voir « Branche et commits »), la phase n'a donc pas d'acceptation vérifiable au sens de CLAUDE.md.

## Décisions de réalisation

Chaque décision ci-dessous a été prise par Fatima-Zahrae Abbadi le 2026-09-23, dans la session de préparation du plan, sans justification donnée. Ces décisions ne valent pas décision du Product Owner (identité non précisée dans la session).

### D-01 — Techno

- Choix : Python 3.12, FastAPI, pytest et le client de test FastAPI (httpx).
- Lien avec la spec : Q-01 (contraintes, langage, techno) reste ouverte côté spec tant que le Product Owner ne l'a pas tranchée.
- Conséquences : il faut remplacer la réponse d'erreur par défaut de FastAPI (422 `{"detail": …}`) par la réponse 400 `{"error": "<message>"}` de R-06, et imposer des entiers stricts pour `x` et `y` (ni `"3"` ni `true`). Si le Product Owner impose une autre techno, la couche API et les tests HTTP seront à réécrire ; le cœur de simulation est petit.
- Autres options envisagées : TypeScript, Node, Fastify et Vitest ; Java, Spring Boot et JUnit ; Python sans framework ou avec Flask.

### D-02 — Branche et commits

- Branche : le travail se fait sur `phase-build`, poussée vers `origin/phase-build`. Aucune pull request n'est ouverte.
- Écart à la convention : CLAUDE.md prévoit une branche `claude/build-mars-rover` et une acceptation par merge d'une PR.
- Commits :
  - étape 1 : un commit qui ne contient que ce fichier ;
  - étapes 2 à 8 : un commit par étape, poussé vers `origin/phase-build` juste après ;
  - chaque commit ne contient que les fichiers de son étape, et ses tests passent ;
  - chaque commit et chaque push attend une confirmation explicite.

### D-03 — Champs inconnus dans la demande

- Choix : tout champ absent du contrat R-03 (`x`, `y`, `direction`, `map`, `commands`) est rejeté avec une réponse 400 `{"error": "<message>"}`.
- Lien avec la spec : point non tranché par la spec, compatible avec R-06. À relire par le Product Owner.
- Autre option envisagée : ignorer les champs inconnus.

### D-04 — Symboles de carte et sélecteur de variante Unicode

- Choix : seuls les quatre caractères exacts de R-02 sont reconnus (🟩 U+1F7E9, 🌳 U+1F333, 🟫 U+1F7EB, 🪨 U+1FAA8), et chaque case correspond à un seul caractère. Tout autre caractère, y compris le sélecteur U+FE0F, est rejeté avec une réponse 400. Le message indique la rangée, la colonne et le code du caractère, par exemple `symbole inconnu U+FE0F en rangée 0, colonne 1`.
- Lien avec la spec : point non tranché par la spec. À relire par le Product Owner.
- Autres options envisagées : retirer les U+FE0F avant la lecture ; découper la carte par graphème.

### D-05 — Mise à jour de CLAUDE.md

- Choix : à l'étape 8, une fois les commandes vérifiées, un texte de mise à jour est soumis à validation avant toute modification. Il remplace la rubrique « Nature du dépôt », ajoute une rubrique « Commandes » et complète « Organisation ». Il ne cite pas la branche.
- Commit : séparé du code, avec le message « Met à jour les instructions du projet ».

## Architecture

Le cœur de simulation ne dépend ni de FastAPI ni des symboles de carte (conception de la spec, points 1 et 2). `simulate` n'a pas d'effet de bord : la réponse n'est construite qu'après son exécution complète. Ce calcul tient lieu de « trajet à blanc » exigé par R-06, sans passe de validation séparée qui dupliquerait les règles de déplacement.

| Fichier | Rôle | Exigences |
| --- | --- | --- |
| `pyproject.toml`, `.gitignore` | dépendances, configuration de pytest | — |
| `src/mars_rover/direction.py` | `Direction` (cycle N → E → S → W), `turn_right`, `turn_left`, déplacement (dx, dy) | EX-04, EX-05, R-05 |
| `src/mars_rover/grid.py` | `Grid` (`contains`, `is_obstacle`) ; `parse_map(rows)` : traduction des symboles, carte non vide et rectangulaire | EX-02, EX-09, D-04 |
| `src/mars_rover/commands.py` | `Command` (F, R, L) ; `parse_commands(text)` | EX-01, EX-08 |
| `src/mars_rover/simulation.py` | `RoverState` (x, y, direction) ; `simulate(grid, départ, commandes)` qui renvoie `SimulationResult(state, blocked)`, avec rejet d'un départ hors carte ou sur obstacle et d'une sortie de carte | EX-03, EX-06, EX-07, EX-08, R-01, R-04 |
| `src/mars_rover/errors.py` | `InvalidRequest(message)` : erreur métier unique | R-06 |
| `src/mars_rover/api.py` | `POST /simulations` : traduction du JSON en objets du domaine, appel de `simulate`, transformation de `InvalidRequest` et des erreurs de validation en réponse 400 | EX-01, EX-07, R-03, R-06, D-03 |
| `tests/test_*.py` | un fichier de tests par module | voir « Tests prévus » |

## Ordre du travail

1. Enregistrer ce plan et commiter uniquement ce fichier (« Ajoute le plan de réalisation Simulateur Mars Rover »).
2. Mettre en place le projet : `pyproject.toml`, `.gitignore`, un test minimal qui vérifie que pytest tourne.
3. `direction.py` et ses tests, en écrivant le test d'abord.
4. `grid.py` et ses tests.
5. `commands.py` et ses tests.
6. `simulation.py` et ses tests.
7. `errors.py`, `api.py` et les tests HTTP de bout en bout.
8. Relecture clean-code, exécution complète des tests, proposition de mise à jour de CLAUDE.md (D-05).

## Tests prévus

- **direction**
  - quatre `R` depuis N donnent E, S, W puis N (EX-04) ;
  - quatre `L` depuis N donnent W, S, E puis N (EX-05) ;
  - déplacements N = (0, -1), S = (0, +1), E = (+1, 0), W = (-1, 0) (R-05).
- **grid**
  - le jeu A, le jeu B et une carte mélangée décrivant la même disposition donnent la même grille (EX-02) ;
  - une carte avec des rangées de 4 et de 3 cases est rejetée (EX-09) ;
  - une carte vide ou contenant une rangée vide est rejetée ;
  - un symbole inconnu est rejeté, par exemple `.` ;
  - une carte contenant 🌳 suivi de U+FE0F est rejetée, et le message cite `U+FE0F` ainsi que sa position (D-04).
- **commands**
  - `"FRL"` est accepté, `""` donne une liste vide ;
  - `"FX"` et `"f"` sont rejetés.
- **simulation**
  - avancer orienté N décrémente y et garde l'orientation (EX-03) ;
  - `"RF"` et `"FR"` depuis le même état donnent respectivement une case à l'est et une case au nord, orienté E (EX-08) ;
  - `"FLF"` face à un obstacle à l'est laisse le rover sur place, orienté E, avec `blocked=true` (EX-06) ;
  - une liste de commandes vide renvoie l'état de départ avec `blocked=false` (EX-07) ;
  - une sortie par chacun des quatre bords est rejetée, y compris en milieu de trajet (R-01) ;
  - un obstacle rencontré avant une sortie de carte donne un résultat valide et bloqué ;
  - un départ hors carte ou sur un obstacle est rejeté.
- **api**
  - un cas nominal renvoie 200 et `{"x", "y", "direction", "blocked"}` (EX-01, EX-07) ;
  - renvoient 400 `{"error": …}` sans aucune position : orientation inconnue, x ou y non entier (y compris `"3"` et `true`), champ manquant, champ inconnu (D-03), JSON mal formé, carte irrégulière, symbole inconnu, commande inconnue, départ hors carte ou sur obstacle, sortie de carte (R-06).

## Risques

- **Étape la plus risquée : l'étape 7 (API).** C'est là que le contrat devient observable par l'application pilote. Le comportement par défaut de FastAPI (422, conversion de types, format d'erreur) va à l'encontre de R-06. Chaque cas de rejet a donc son test HTTP.
- **Ordre entre obstacle et sortie de carte (étape 6).** Un obstacle rencontré avant une sortie donne un résultat valide et bloqué ; une sortie rencontrée avant un obstacle entraîne un rejet.
- **Contrat figé.** Une fois l'application pilote branchée, toute différence avec la spec deviendra une rupture pour elle.
- **CLAUDE.md faux pendant les étapes 2 à 7.** Sa rubrique « Nature du dépôt » affirme qu'il n'y a aucun code ; la correction n'arrive qu'à l'étape 8 (D-05).
- **Q-01 ouverte.** Un choix de techno différent du Product Owner imposerait de réécrire la couche API.

## Contexte de génération

### Demande initiale

```
Lis @intent.md et @spec.md, puis propose un plan de réalisation du simulateur. Précise les fichiers à créer ou modifier, l’ordre du travail et les tests prévus.

Prévois comme première étape d’enregistrer le plan dans plan.md à côté de ces deux fichiers et de commiter uniquement ce fichier.
```

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| .claude/skills/clean-code/SKILL.md | 06dff2f7a6131c0124b42dec62f11e8cb9deb8eb |

Aucun changement non commité n'a été constaté sur cette skill au moment de la génération.
