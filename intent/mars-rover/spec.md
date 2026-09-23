# Spec : Simulateur Mars Rover

Intention de référence : [intent/mars-rover/intent.md](intent.md) (acceptée par merge de la PR #1 dans main, le 2026-09-23)

## Périmètre

Besoin couvert : permettre à l'équipe qui construit Mars Rover de connaître la position et l'orientation finales du rover sans le déployer réellement. Le simulateur :
- reçoit un point de départ (x, y), une orientation initiale (N, S, E ou W), une carte plaçant les obstacles et une liste de commandes ;
- interprète les commandes avancer, tourner de 90° à droite et tourner de 90° à gauche ;
- reste immobile lorsqu'un obstacle bloque son avancée ;
- affiche la position et la direction finales du rover.

La carte peut utiliser deux jeux de symboles. Dans chaque jeu, le premier symbole désigne une case libre et le second un obstacle.

Utilisateurs : les utilisateurs de l'application qui pilote l'outil. Cette application sollicite le simulateur via une API.

Exclusions : l'intention n'en formule aucune explicitement. Elle ne prévoit pas d'autres commandes que avancer, tourner à droite et tourner à gauche. Elle ne demande pas non plus de restituer le trajet intermédiaire.

Contraintes : non précisées dans l'intention (voir Questions ouvertes).

## Exigences

### EX-01 — Recevoir une demande de simulation via une API

Origine dans l'intention : « reçoit un point de départ (x, y), une orientation initiale (N, S, E ou W), une carte plaçant les obstacles, et une liste de commandes » ; « sollicitant le simulateur via une API ».
Comportement attendu : le simulateur expose une API. Une demande de simulation fournit un point de départ (x, y), une orientation initiale parmi N, S, E et W, une carte et une liste de commandes.

Scénario
- Situation de départ : l'application pilote dispose d'un point de départ, d'une orientation, d'une carte et d'une liste de commandes.
- Action : elle envoie une demande de simulation à l'API.
- Résultat attendu : le simulateur accepte la demande et produit un résultat (EX-07).

Scénario complémentaire (entrée invalide)
- Situation de départ : la demande contient une entrée invalide (orientation inconnue, symbole de carte inconnu, commande inconnue, carte vide ou irrégulière, point de départ hors carte ou sur obstacle, ou trajet qui sortirait de la carte).
- Action : elle envoie cette demande à l'API.
- Résultat attendu : le simulateur rejette la demande avant toute exécution de commande, avec une réponse HTTP 400 et un corps `{"error": "<message>"}` (R-06).

Contrat (R-03, choix délégué par le Product Owner) : `POST /simulations` avec un corps JSON `{"x": <entier>, "y": <entier>, "direction": "N"|"S"|"E"|"W", "map": [<rangée>, …], "commands": "<lettres F, R, L>"}`.

### EX-02 — Interpréter une carte écrite avec l'un des deux jeux de symboles

Origine dans l'intention : « La carte peut utiliser deux jeux de symboles possibles pour représenter les cases (dans chaque jeu, le premier symbole indique une case libre, le second un obstacle). »
Comportement attendu : le simulateur accepte une carte écrite avec l'un ou l'autre jeu de symboles, ou avec un mélange des deux (décision R-02). Dans chaque jeu, il interprète le premier symbole comme une case libre et le second comme un obstacle. Le résultat de la simulation ne dépend pas des symboles utilisés.

Scénario
- Situation de départ : deux cartes décrivent la même disposition d'obstacles, chacune avec un jeu de symboles différent.
- Action : la même demande (départ, orientation, commandes) est simulée sur chacune des deux cartes.
- Résultat attendu : les deux simulations donnent la même position et la même direction finales.

Jeux de symboles (R-02, décision du Product Owner) :

| Jeu | Case libre | Obstacle |
| --- | --- | --- |
| A | 🟩 | 🌳 |
| B | 🟫 | 🪨 |

Scénario complémentaire (mélange)
- Situation de départ : une carte utilise 🟩 et 🪨 dans une même rangée, et décrit la même disposition d'obstacles qu'une carte écrite uniquement avec le jeu A.
- Action : la même demande est simulée sur les deux cartes.
- Résultat attendu : les deux simulations donnent la même position et la même direction finales.

### EX-09 — Accepter uniquement une carte rectangulaire

Origine dans l'intention : « une carte plaçant les obstacles ». Précisé par la décision R-02 du Product Owner (2026-09-23).
Comportement attendu : la carte est composée de rangées de cases, et toutes les rangées ont le même nombre de cases. Une carte dont les rangées n'ont pas toutes la même longueur n'est pas simulée.

Scénario
- Situation de départ : une carte a une première rangée de 4 cases et une deuxième rangée de 3 cases.
- Action : une demande de simulation est envoyée avec cette carte.
- Résultat attendu : aucune position finale n'est calculée. La demande est rejetée avec une réponse HTTP 400 et un corps `{"error": "<message>"}` (R-06).

### EX-03 — Avancer d'une case dans la direction courante

Origine dans l'intention : « interprète les commandes : avancer ».
Comportement attendu : la commande avancer déplace le rover d'une case dans la direction de son orientation courante. L'orientation reste inchangée.

Scénario
- Situation de départ : le rover est sur une case libre, orienté N. La case voisine au nord est libre et se trouve dans la carte.
- Action : la commande avancer est exécutée.
- Résultat attendu : le rover occupe la case voisine au nord et reste orienté N. Avancer orienté N décrémente y de 1 (R-05).

Scénario complémentaire (sortie de la carte)
- Situation de départ : le rover est sur une case libre en bordure de la carte, orienté de sorte que la case suivante serait hors de la carte.
- Action : la commande avancer est exécutée.
- Résultat attendu : la demande est rejetée avant toute exécution de commande, avec une réponse HTTP 400 et un corps `{"error": "<message>"}` (R-01, R-06). Aucune position n'est renvoyée.

### EX-04 — Tourner de 90° à droite

Origine dans l'intention : « tourner de 90° à droite ».
Comportement attendu : la commande tourner à droite fait pivoter le rover de 90° dans le sens horaire (N → E → S → W → N) sans changer sa position.

Scénario
- Situation de départ : le rover est en (x, y), orienté N.
- Action : la commande tourner à droite est exécutée quatre fois, avec un relevé après chaque exécution.
- Résultat attendu : le rover prend successivement les orientations E, S, W puis N et reste en (x, y).

### EX-05 — Tourner de 90° à gauche

Origine dans l'intention : « tourner de 90° […] à gauche ».
Comportement attendu : la commande tourner à gauche fait pivoter le rover de 90° dans le sens antihoraire (N → W → S → E → N) sans changer sa position.

Scénario
- Situation de départ : le rover est en (x, y), orienté N.
- Action : la commande tourner à gauche est exécutée quatre fois, avec un relevé après chaque exécution.
- Résultat attendu : le rover prend successivement les orientations W, S, E puis N et reste en (x, y).

### EX-06 — Rester immobile face à un obstacle

Origine dans l'intention : « reste immobile lorsqu'un obstacle bloque son avancée ».
Comportement attendu : lorsque la case dans la direction courante contient un obstacle, la commande avancer ne déplace pas le rover. Sa position et son orientation restent inchangées. La simulation s'arrête alors et les commandes suivantes ne sont pas exécutées (décision R-04).

Scénario
- Situation de départ : le rover est en (x, y), orienté E. La case voisine à l'est contient un obstacle.
- Action : la liste de commandes `"FLF"` (avancer, tourner à gauche, avancer) est exécutée.
- Résultat attendu : le rover reste en (x, y), orienté E. Les commandes « tourner à gauche, avancer » ne sont pas exécutées. La réponse vaut `{"x": x, "y": y, "direction": "E", "blocked": true}`.

### EX-07 — Restituer la position et la direction finales

Origine dans l'intention : « affiche la position et la direction finales du rover ».
Comportement attendu : à l'issue de la simulation, le simulateur renvoie à l'appelant la position finale (x, y) et la direction finale (N, S, E ou W) du rover. La réponse indique aussi si la simulation s'est arrêtée sur un obstacle (champ `blocked`, décision R-04).

Scénario
- Situation de départ : une demande valide est envoyée (départ (x, y), orientation N, carte sans obstacle sur le trajet, liste de commandes vide).
- Action : la simulation est exécutée.
- Résultat attendu : la réponse JSON contient la position et la direction de départ, sous la forme `{"x": x, "y": y, "direction": "N", "blocked": false}` (R-03, R-04).

### EX-08 — Exécuter les commandes dans l'ordre de la liste

Origine dans l'intention : « une liste de commandes » ; « interprète les commandes ».
Comportement attendu : le simulateur exécute les commandes une à une, dans l'ordre de la liste. Chaque commande part de l'état laissé par la précédente.

Scénario
- Situation de départ : le rover est orienté N sur une case libre. Les cases voisines sont libres et se trouvent dans la carte.
- Action : la liste `"RF"` (tourner à droite, avancer) est exécutée, puis, sur une nouvelle simulation partant du même état, la liste `"FR"` (avancer, tourner à droite).
- Résultat attendu : dans le premier cas, le rover finit une case à l'est, orienté E. Dans le second, il finit une case au nord, orienté E.

## Conception proposée

Tous les choix ci-dessous sont **proposés** et restent à valider par le Product Owner. Aucun n'a encore été accepté.

1. **Séparation entre le cœur de simulation et l'API.** Un cœur de simulation calcule l'état final à partir de l'état initial, de la carte et des commandes. Une couche API, distincte, reçoit les demandes et renvoie les résultats. Justification : les règles de déplacement (EX-03 à EX-06, EX-08) peuvent être vérifiées sans passer par l'API. Leur logique ne dépend pas non plus du format d'échange. La couche API suit le contrat HTTP/JSON retenu dans R-03 (`POST /simulations`, commandes `F`/`R`/`L`, carte en liste de rangées).
2. **Normalisation de la carte à l'entrée.** La carte reçue est convertie une seule fois en une grille de cases libres ou occupées, quel que soit le jeu de symboles utilisé. Le cœur de simulation ne manipule jamais les symboles. Symboles reconnus : 🟩 et 🟫 (libre), 🌳 et 🪨 (obstacle), mélangeables dans une même carte. La normalisation vérifie aussi que toutes les rangées ont la même longueur (EX-09). Voir R-02. Justification : EX-02 exige que le résultat ne dépende pas du jeu de symboles. Traiter ce point à un seul endroit garantit cette indépendance.
3. **État du rover réduit à la position et à l'orientation.** L'état du rover se compose de (x, y) et de l'orientation. Chaque commande transforme un état en un nouvel état. Justification : c'est l'information que l'intention demande de restituer (EX-07). Ce modèle rend aussi l'enchaînement ordonné des commandes explicite (EX-08).
4. **Rotation par cycle d'orientations.** Les orientations suivent le cycle N, E, S, W. Tourner à droite passe à l'orientation suivante du cycle, tourner à gauche à la précédente. Justification : cela couvre EX-04 et EX-05 sans cas particulier.
5. **Contrôle d'obstacle avant chaque déplacement.** Avant de déplacer le rover, la commande avancer calcule la case cible et consulte la grille normalisée. Si la case est occupée, l'état reste inchangé, l'exécution s'arrête et le résultat est marqué `blocked` (décision R-04). Justification : cela répond à EX-06 et donne à l'appelant l'information que la position seule ne fournit pas.
   Ce même calcul de case cible détecte aussi une sortie de la carte : si la case cible est hors de la grille, la simulation en cours (voir point 6) note cette sortie comme invalide plutôt que de continuer (décision R-01).
6. **Validation complète avant toute réponse.** Les entrées sont contrôlées avant de renvoyer un résultat : orientation connue, symboles de carte reconnus, carte rectangulaire (EX-09), commandes reconnues, point de départ exploitable, et absence de sortie de la carte sur l'ensemble du trajet. Ce dernier point est vérifié en exécutant la simulation normalement dès la réception de la demande : si une sortie de carte est rencontrée (avant un éventuel blocage par obstacle, qui lui reste un résultat valide), la demande entière est rejetée et aucune position n'est renvoyée. Toute entrée invalide, quelle que soit sa nature, produit la même forme de réponse d'échec : HTTP 400 avec un corps `{"error": "<message>"}` (décision R-06). Justification : cela évite d'exposer à l'appelant un état intermédiaire atteint sur un trajet finalement invalide, et donne un contrat d'erreur unique et prévisible.

## Réserves

### R-01 — Comportement au bord de la carte

- Origine : l'intention décrit une carte et le blocage par un obstacle. Elle ne dit rien du cas où le rover avance au-delà du bord.
- Exigences concernées : EX-03, EX-06, EX-08, EX-09, R-06.
- Conséquences : sans décision, le résultat d'un avancer depuis une case en bordure n'était pas défini. Les options possibles étaient : passer de l'autre côté de la carte (monde torique), rester immobile comme face à un obstacle, ou rejeter la demande.
- Décision humaine : « Rejet de la demande », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Justification : aucune donnée par le Product Owner.
- Choix retenu : lorsqu'une commande avancer mènerait le rover hors de la carte, la demande est rejetée. Le rover n'est ni téléporté de l'autre côté de la carte, ni simplement bloqué comme face à un obstacle. D'après R-06, ce rejet est détecté avant toute exécution de commande et renvoyé avec une réponse HTTP 400 et un corps `{"error": "<message>"}`.
- Éléments modifiés : EX-03 (scénario complémentaire ajouté), R-06 (cas ajouté aux conséquences).
- Statut : tranchée.

### R-02 — Symboles concrets des deux jeux

- Origine : « La carte peut utiliser deux jeux de symboles possibles ». Les symboles eux-mêmes ne sont pas donnés.
- Exigences concernées : EX-02, EX-01.
- Conséquences : impossible de lire une carte sans connaître les symboles. Il faut aussi savoir si une même carte peut mélanger les deux jeux, et comment la carte est structurée (lignes, séparateurs).
- Décision attendue : définir les deux jeux (symbole libre et symbole obstacle pour chacun), dire si le mélange est autorisé et fixer la structure de la carte.
- Décision humaine (symboles) : « tu px mettre ce que tu vx comme symbole ». Le Product Owner a délégué ce choix le 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Justification : aucune donnée par le Product Owner.
- Choix fait par Claude dans le cadre de cette délégation, puis remplacé par la décision humaine ci-dessous : jeu A = `.` (libre) et `#` (obstacle) ; jeu B = `_` (libre) et `X` (obstacle).
- Décision humaine (symboles concrets définitifs) : « Symboles de carte : 🟩/🌳 ou 🟫/🪨. », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Justification : aucune donnée par le Product Owner. Cette décision remplace le choix fait par Claude ci-dessus.
- Jeux retenus : jeu A = 🟩 (libre) et 🌳 (obstacle) ; jeu B = 🟫 (libre) et 🪨 (obstacle).
- Décision humaine (mélange et structure) : « oui , rangées », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Réponse à deux questions : une même carte peut mélanger les deux jeux ; la carte est rectangulaire, toutes ses rangées ont la même longueur. Justification : aucune donnée par le Product Owner.
- Éléments modifiés : EX-02 (comportement attendu, tableau et scénarios), EX-09 (ajoutée), conception proposée (point 2), R-03 (exemple de carte), R-06 (cas de la carte irrégulière).
- Reste renvoyé à R-03 : la forme de l'envoi de la carte (chaîne de texte avec une ligne par rangée, ou liste de lignes).
- Statut : tranchée.

### R-03 — Format d'échange de l'API et encodage des commandes

- Origine : « sollicitant le simulateur via une API » ; « affiche la position et la direction finales ». Ni le format de la demande, ni celui de la réponse, ni l'encodage des commandes ne sont précisés.
- Exigences concernées : EX-01, EX-07, EX-08.
- Conséquences : l'application pilote ne peut pas s'intégrer sans contrat d'API. Il faut décider du style de l'API, de la représentation de la demande, de la représentation de la réponse et des symboles des commandes. « Affiche » doit aussi être interprété : renvoyer le résultat dans la réponse de l'API, ou prévoir un affichage supplémentaire.
- Décision attendue : définir le contrat d'API (entrées, sortie, encodage des commandes) et confirmer que « afficher » signifie « renvoyer dans la réponse de l'API ».
- Décision humaine : « je te laisse choisir », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Le Product Owner a délégué les quatre points de R-03. Justification : aucune donnée par le Product Owner.
- Choix retenus dans le cadre de cette délégation (faits par Claude, soumis à la relecture du Product Owner dans la pull request) :
  1. API HTTP avec des échanges en JSON : une demande de simulation est un appel `POST /simulations`. Justification : c'est le format le plus courant pour une application cliente, et il ne suppose aucun langage chez l'appelant.
  2. Commandes encodées en une chaîne de lettres : `F` pour avancer, `R` pour tourner à droite, `L` pour tourner à gauche. Justification : c'est compact et cela correspond aux trois commandes de l'intention.
  3. Carte transmise comme une liste de rangées, chaque rangée étant une chaîne de symboles. Justification : chaque rangée est un élément distinct, ce qui simplifie la vérification d'EX-09, sans ambiguïté sur les fins de ligne.
  4. « Afficher » veut dire renvoyer la position et la direction finales dans la réponse de l'API. Aucun autre affichage n'est prévu.
- Forme de la demande : `{"x": 0, "y": 0, "direction": "N", "map": ["🟩🟩🌳🟩", "🟫🌳🟫🟫"], "commands": "FRFL"}`.
- Forme de la réponse en cas de succès : `{"x": 1, "y": 2, "direction": "E", "blocked": false}`. Le champ `blocked` a été ajouté par la décision R-04.
- Forme de la réponse en cas d'entrée invalide : réponse HTTP 400 avec un corps `{"error": "<message>"}` (décision R-06).
- Éléments modifiés : EX-01, EX-07, EX-08 (scénarios), conception proposée (point 1), R-06 (forme de la réponse d'échec).
- Statut : tranchée.

### R-04 — Suite de l'exécution après un blocage par un obstacle

- Origine : « reste immobile lorsqu'un obstacle bloque son avancée ».
- Exigences concernées : EX-06, EX-08.
- Conséquences : deux lectures sont possibles. Soit le rover s'arrête et ignore toutes les commandes restantes. Soit seul l'avancer bloqué est sans effet et les commandes suivantes s'exécutent. Les positions finales diffèrent (voir le scénario d'EX-06). Il faut aussi décider si la réponse signale qu'un obstacle a été rencontré. L'intention ne demande que la position et la direction finales.
- Décision attendue : choisir la lecture retenue et décider si la rencontre d'un obstacle est signalée dans la réponse.
- Décision humaine : « je te laisse choisir », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Le Product Owner a délégué les deux points de R-04. Justification : aucune donnée par le Product Owner.
- Choix retenus dans le cadre de cette délégation (faits par Claude, soumis à la relecture du Product Owner dans la pull request) :
  1. Arrêt au premier blocage : lorsqu'un `F` est bloqué par un obstacle, le rover reste sur sa case avec son orientation, et les commandes suivantes ne sont pas exécutées. Justification : c'est la lecture la plus littérale de « reste immobile ». Elle évite aussi qu'un rover réel continue une séquence calculée pour un trajet qu'il n'a pas pu suivre.
  2. Signalement du blocage : la réponse contient un champ booléen `blocked`, qui vaut `true` si la simulation s'est arrêtée sur un obstacle et `false` sinon. Justification : avec l'arrêt, la position finale seule ne permet pas de savoir si toutes les commandes ont été exécutées. Réserve : ce champ va au-delà de ce que demande l'intention (position et direction). Le Product Owner peut le retirer à la relecture.
- Éléments modifiés : EX-06 (comportement attendu et scénario), EX-07 (comportement attendu et scénario), R-03 (forme de la réponse), conception proposée (point 5).
- Statut : tranchée.

### R-05 — Système de coordonnées

- Origine : « un point de départ (x, y) », « une carte plaçant les obstacles ». Rien ne relie les coordonnées à la carte.
- Exigences concernées : EX-03, EX-06, EX-07, EX-08.
- Conséquences : sans convention, un même trajet peut aboutir à des coordonnées différentes. Il faut fixer l'origine (0 ou 1, coin de la carte concerné), le sens de x et de y, et la correspondance entre N et le sens de variation de y (par exemple, la première ligne de la carte est-elle au nord ?).
- Décision attendue : définir le système de coordonnées et son lien avec la carte.
- Décision humaine : « Origine en haut à gauche, N = y décroissant », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Justification : aucune donnée par le Product Owner.
- Choix retenu : l'origine (x=0, y=0) est la case de la première rangée et de la première colonne de la carte transmise. x augmente d'une case vers l'est en avançant dans une rangée. y augmente d'une case vers le sud en descendant d'une rangée à la suivante. En conséquence, avancer orienté N décrémente y de 1, avancer orienté S incrémente y de 1, avancer orienté E incrémente x de 1, avancer orienté W décrémente x de 1.
- Éléments modifiés : EX-03 (résultat attendu).
- Statut : tranchée.

### R-06 — Traitement des entrées invalides

- Origine : l'intention décrit les entrées attendues. Elle ne dit pas comment réagir à une entrée incorrecte.
- Exigences concernées : EX-01, EX-02, EX-08, EX-09, R-01.
- Conséquences : plusieurs cas sont possibles : point de départ hors de la carte ou sur un obstacle, orientation inconnue, symbole de carte inconnu, commande inconnue, carte vide, carte irrégulière (refusée d'après la décision R-02), avancer qui mènerait hors de la carte (rejet décidé par R-01). Selon la décision, la demande est rejetée avec une erreur, ou la simulation ignore l'élément fautif. L'application pilote doit savoir ce qu'elle recevra.
- Décision attendue : décider du traitement de chaque cas (rejet de la demande ou autre comportement) et de la forme de la réponse.
- Décision humaine : « Rejet uniforme, validé avant simulation », 2026-09-23. Auteur : Product Owner (identité non précisée dans la session). Justification : aucune donnée par le Product Owner.
- Choix retenu : tous ces cas sont détectés avant toute exécution de commande. La demande est alors rejetée avec la réponse HTTP 400 et un corps JSON `{"error": "<message>"}`. Aucune position n'est jamais calculée ni renvoyée pour une demande invalide. En particulier, une sortie de carte en cours de trajet (R-01) est détectée en simulant le trajet à blanc avant de répondre, et non en s'arrêtant au milieu d'une exécution réelle.
- Éléments modifiés : EX-01 (ajout d'un cas d'échec), EX-03 (scénario complémentaire), EX-09 (résultat attendu), R-01 (forme du rejet), R-02 (forme du rejet pour une carte irrégulière), R-03 (réponse en cas d'échec).
- Statut : tranchée.

## Questions ouvertes

### Q-01 — Contraintes à respecter

- Question de l'intention : « Contraintes à respecter (délai, langage/techno imposé, compatibilité avec un système existant, performance, autre) : à définir. »
- Réponse humaine : aucune à ce stade.
- Statut : ouverte.
- Effet sur le passage à la phase Build : à confirmer par le Product Owner. En l'absence de contrainte, la phase Build devra choisir elle-même le langage, la technologie de l'API et l'hébergement. Si une contrainte existe (technologie imposée, compatibilité avec l'application pilote), elle doit être connue avant le démarrage de la phase Build.

## Contexte de génération

### Demande initiale

```
/spec intent/mars-rover/intent.md
```

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| .claude/skills/spec/SKILL.md | 0776fbedc022cd1fe2332e3836d4c0de9ea2548a |

Aucun changement non commité n'a été constaté sur cette skill au moment de la génération.

### Révisions

Aucune révision à ce stade.
