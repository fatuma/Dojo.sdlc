---
name: spec
description: Rédige ou révise la spécification d’une intention acceptée. Décrit les exigences et la conception, signale les réserves et conserve le contexte de génération. S’invoque avec /spec suivi du chemin de l’intent.md.
disable-model-invocation: true
---

# Spec

Rédige la spécification de l’intention désignée par $ARGUMENTS.
Enregistre spec.md dans le même dossier que cette intention.
Le Product Owner relit la proposition et décide de son acceptation.

## Avant de rédiger

- Lis l’intention et vérifie que sa version acceptée est disponible dans la branche main. Sa présence seule ne prouve pas son acceptation. Consulte la décision dans la pull request ; si tu ne peux pas la vérifier, demande au Product Owner de la confirmer.
- Si la session est sur main, crée une branche pour la phase Design depuis la dernière version de main sur GitHub et place-toi dessus avant toute écriture dans intent/. Choisis un nom disponible et respecte les contraintes de nommage de l’environnement. Si la création ou le changement de branche échoue, arrête-toi sans écrire la spécification et explique le problème.
- Si la session est déjà sur une branche de travail, conserve-la pour poursuivre la rédaction ou la révision. Vérifie qu’elle contient la version acceptée de l’intention. Si ce n’est pas le cas, signale-le et attends sa mise à jour avant d’écrire la spécification.
- Si spec.md existe déjà, lis-le et conserve les décisions humaines qui y sont enregistrées. Une demande de révision doit préciser les décisions à réexaminer.

## Rédiger les exigences et la conception

- Reprends le besoin, le périmètre et les contraintes de l’intention acceptée. N’ajoute aucune contrainte produit ou règle d’organisation.
- Donne à chaque exigence un identifiant stable. Indique le comportement attendu et son origine dans l’intention.
- Associe à chaque exigence un scénario avec une situation de départ, une action et un résultat observable. Si le résultat dépend d’une décision encore ouverte, indique ce qui manque au lieu d’inventer la réponse.
- Décris la conception proposée et justifie ses choix au regard du besoin. Distingue les choix déjà acceptés des propositions à valider.
- N’écris ni code ni plan de réalisation. Le découpage des travaux et leur ordre appartiennent à la phase Build.

## Signaler les réserves et suivre les questions

- Signale les ambiguïtés, les informations manquantes et les éventuelles contradictions qui empêchent de préciser la solution. Ne fabrique pas de réserve pour remplir une rubrique.
- Pour chaque réserve, indique son origine, les exigences concernées, ses conséquences et la décision attendue du Product Owner.
- Reprends chaque question ouverte de l’intention. Indique si elle reste ouverte ou si une réponse humaine a été fournie. Une question bloquante doit rester visible avant le passage à la phase Build.
- Après une décision humaine, consigne sa formulation, son auteur lorsqu’il est connu, sa date et sa justification. Mets à jour les exigences, les scénarios et les choix concernés. N’invente ni auteur ni accord.

## Conserver le contexte de génération

- Recopie le prompt exact qui a demandé la spécification dans la rubrique « Contexte de génération ». Pour une invocation /spec, conserve la commande et son argument.
- Liste les chemins des skills réellement utilisées, y compris cette skill. Relève pour chacune l’identifiant du commit Git qui permet de retrouver le contenu utilisé.
- Vérifie que le contenu utilisé correspond à cette version. Si une skill contient des changements non commités ou si sa version ne peut pas être établie, signale-le au lieu d’attribuer une fausse version.
- Lors d’une révision, conserve le contexte initial et ajoute la demande de révision ainsi que les versions des skills utilisées pour cette révision.

## Conduire les décisions

Présente le nom de la branche, le chemin de spec.md, les réserves et les questions qui demandent une décision. Reprends-les ensuite une par une.
Pour chacune, explique ce qui doit être tranché et les conséquences de chaque choix, attends la réponse du Product Owner, puis mets à jour les exigences, les scénarios et les choix concernés. Ne décide jamais à sa place et n’enchaîne pas sur la suivante avant sa réponse.
Une question qu’il ne peut pas trancher reste ouverte. Consigne-la avec son effet sur le passage à la phase Build.

## Enregistrer et proposer

Quand il ne reste plus de point à trancher, arrête-toi et demande si la spécification peut être proposée. N’enregistre rien avant cette réponse.
Une fois acceptée, commit spec.md, push la branche et ouvre la pull request vers main pour la soumettre au Product Owner. Résume les décisions prises et les questions restées ouvertes. Ne déclare pas la spécification acceptée et ne merge pas la pull request.

## Format de spec.md

```md
# Spec : [titre]

Intention de référence : [chemin vers intent.md]

## Périmètre

[Besoin couvert et exclusions présents dans l’intention.]

## Exigences

### EX-01 — [comportement attendu]

Origine dans l’intention : [passage concerné]
Comportement attendu : [exigence vérifiable]

Scénario
- Situation de départ : [conditions connues]
- Action : [action effectuée]
- Résultat attendu : [résultat observable ou décision manquante]

## Conception proposée

[Choix de conception, justification et statut proposé ou accepté.]

## Réserves

[Pour chaque réserve réelle, origine, exigences concernées, conséquences, décision attendue et statut. Après décision, conserver l’auteur connu, la date, la justification et les éléments modifiés. Indiquer « Aucune réserve identifiée » si l’examen n’en révèle aucune.]

## Questions ouvertes

[Suivi de chaque question de l’intention, réponse humaine éventuelle et effet sur le passage à la phase Build.]

## Contexte de génération

### Demande initiale

[Prompt exact ou commande /spec avec son argument.]

### Skills utilisées

| Chemin | Commit Git de la version utilisée |
| --- | --- |
| [chemin du SKILL.md utilisé] | [identifiant vérifié du commit] |

### Révisions

[Lors de chaque révision, ajouter la demande exacte et les versions des skills utilisées.]
```
