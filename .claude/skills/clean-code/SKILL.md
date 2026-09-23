---
name: clean-code
description: >-
  Applique les principes Clean Code lors de la planification, de
  l’implémentation et de la relecture du code. À utiliser aussi pour
  proposer des critères de lisibilité à partir d’une spécification ou
  identifier les erreurs de nommage, de responsabilité et de complexité
  à éviter avant la réalisation.
---

# Appliquer Clean Code de Robert C. Martin

## Quand utiliser cette skill

Utilise cette skill lorsque la lisibilité, la compréhension locale et la maintenabilité du code sont les préoccupations principales, notamment pendant l’implémentation et la relecture courantes.

## Biais à corriger

Un code qui fonctionne n’est pas automatiquement un code propre.

## Règles de décision

- Intègre la propreté du code à la livraison. Préserve le comportement et améliore le code touché dans le périmètre demandé. Un délai serré ou une réécriture promise ne justifie pas d’ajouter du désordre.
- Facilite la compréhension locale. Le lecteur doit pouvoir suivre le cheminement sans reconstituer un état caché, naviguer entre des portions éloignées ou décoder des conventions de nommage obscures.
- Utilise des noms précis et un seul terme par concept. Renomme ce qui masque l’intention, porte plusieurs sens ou nécessite des commentaires compensatoires.
- Garde les fonctions petites, ciblées et à un seul niveau d’abstraction. Présente l’intention avant les détails, dans une lecture de haut en bas.
- Limite les paramètres et donne-leur un sens clair. Évite les indicateurs booléens, les paramètres de sortie et les listes d’arguments hétéroclites. Modélise le concept qu’ils représentent.
- Sépare les commandes des requêtes et supprime les effets de bord cachés. Une fonction qui répond à une question ne doit pas modifier l’état à l’insu du lecteur.
- Garde le parcours nominal lisible. Isole la gestion des erreurs, des états invalides et du nettoyage des ressources. Préfère une absence explicite ou des résultats typés aux valeurs sentinelles de type null lorsque le langage le permet.
- Expose les comportements plutôt que la représentation interne. Évite les chaînes d’accès en cascade, les modules utilitaires fourre-tout et les classes ou modules aux responsabilités mélangées.
- Garde les détails de construction, de framework, de persistance, de transaction, de sécurité et de fournisseurs externes en dehors du comportement métier.
- Conçois des API publiques réduites, explicites et difficiles à mal utiliser. Rends visibles la logique aux frontières, l’ordre requis des opérations et les points de changement probables.
- Réserve les commentaires aux raisons des choix, aux contraintes, aux avertissements et aux contrats externes. Ne commente pas le déroulement du code au lieu de l’améliorer.
- Traite les tests comme du code de production. Ils doivent être lisibles, déterministes et alignés sur le comportement ou le contrat protégé. Effectue une validation proportionnée avant de déclarer la modification terminée.
- Laisse la conception émerger des tests, de la suppression des duplications, de l’expressivité et d’une structure minimale. N’ajoute pas d’abstractions ou d’infrastructure inutiles.
- Dans le code touché, corrige le défaut qui augmente le plus le coût des changements. Ne dépasse pas silencieusement le plus petit nettoyage nécessaire pour rendre la modification demandée sûre.

## Déclencheurs

- Lorsqu’une fonction mélange préparation, validation, calcul et effets de bord, sépare ces phases.
- Lorsqu’un commentaire explique le flux de contrôle, simplifie les noms ou la structure avant de le conserver.
- Lorsqu’une fonction modifie l’état tout en renvoyant une réponse, ou cache un changement de mode derrière un indicateur, sépare les responsabilités.
- Lorsque des duplications, des branchements répétés ou des groupes de valeurs primitives apparaissent, nomme le concept avec un objet de paramètres, du polymorphisme, un cas particulier ou une autre petite abstraction.
- Lorsqu’une frontière laisse entrer les particularités d’un framework, d’un fournisseur ou de la persistance, ajoute ou renforce un adaptateur local.
- Lorsque l’asynchronisme ou la concurrence intervient, isole la politique d’exécution des threads, minimise l’état mutable partagé, définis l’arrêt et teste les comportements sensibles au timing.
- Lorsque tu corriges un bug ou modifies un comportement, ajoute ou mets à jour le test qui protège le contrat attendu.
- Lorsque le nettoyage s’étend à des zones sans rapport avec la demande, reviens au plus petit refactoring qui garde la modification sûre et lisible.

## Vérification finale

- Le lecteur peut-il comprendre la modification localement ?
- Les noms et les API portent-ils le sens sans commentaire narratif ?
- Les mutations sont-elles explicites et le parcours nominal reste-t-il clair ?
- Les détails de framework, de persistance, de fournisseurs et de construction restent-ils derrière leurs frontières ?
- Ai-je supprimé au moins un défaut de conception dans la zone touchée ?
- Les tests protègent-ils le comportement ou le contrat modifié ?
- Ai-je réellement exécuté les tests ou vérifications pertinents pour cette modification ?
