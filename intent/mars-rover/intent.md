# Intent : Simulateur Mars Rover
Auteur : non renseigné.

## Problème
L'équipe qui construit Mars Rover ne dispose pas d'un outil permettant de simuler le déplacement du rover : à partir d'un point de départ, d'une carte et d'une liste de commandes, il n'est pas possible aujourd'hui de connaître la position et l'orientation finales du rover sans le déployer réellement.

## Résultat proposé
Un simulateur qui :
- reçoit un point de départ (x, y), une orientation initiale (N, S, E ou W), une carte plaçant les obstacles, et une liste de commandes ;
- interprète les commandes : avancer, ou tourner de 90° à droite ou à gauche ;
- reste immobile lorsqu'un obstacle bloque son avancée ;
- affiche la position et la direction finales du rover.

La carte peut utiliser deux jeux de symboles possibles pour représenter les cases (dans chaque jeu, le premier symbole indique une case libre, le second un obstacle).

## Utilisateurs et systèmes concernés
Les utilisateurs de l'application qui pilote l'outil, sollicitant le simulateur via une API.

## Contraintes
Non précisées (voir Questions ouvertes).

## Questions ouvertes
- Contraintes à respecter (délai, langage/techno imposé, compatibilité avec un système existant, performance, autre) : à définir.
