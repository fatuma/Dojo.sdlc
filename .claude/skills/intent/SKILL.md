---
name: intent
description: Aide à préciser un besoin et rédige intent.md après validation du brouillon. À utiliser pour formaliser ou mettre à jour l’intention d’un produit avant sa conception.
---

# Intent

Transforme une idée en intention structurée, sans décider à la place de son auteur.

## Règles

- Le document se trouve toujours dans `intent/<slug>/intent.md`. Si le slug
  n'est pas fourni, demande-le avant de commencer.
- Ne prends aucune décision produit à la place de l'auteur et n'invente aucune
  contrainte ni solution technique.
- Conserve tout point non tranché dans `Questions ouvertes`.
- Utilise les informations d'auteur fournies dans la demande ou présentes dans
  le document. Si elles manquent, indique `Auteur : non renseigné.`.
- Attends une validation explicite du brouillon avant de créer ou de modifier
  le fichier.
- Cette validation autorise la création d'une branche de travail et l'écriture
  du fichier sur cette branche. L'intention sera acceptée plus tard par le
  Product Owner lors du merge de sa pull request.
- Ne développe pas le produit. Sans confirmation de la création de la pull
  request, ne commit rien, ne push rien et n'ouvre aucune pull request.
  Après confirmation, limite ces opérations au fichier d'intention concerné.

## Préciser le besoin

Si `intent/<slug>/intent.md` existe, lis-le avant de poser tes questions et
préserve les décisions et les informations qui ne sont pas remises en cause.
Reformule le besoin, puis pose une question à la fois pour préciser le problème,
le résultat recherché, les utilisateurs et systèmes concernés et les contraintes.
Si la personne demande le brouillon ou n'a plus d'information, arrête les
questions et conserve les inconnues dans `Questions ouvertes`.
Si la demande fournit déjà le problème, le résultat recherché, le slug et
l'auteur, par exemple un diagnostic accepté, passe directement au brouillon
sans poser de questions.

## Proposer le brouillon

Présente le brouillon dans la conversation avec ce modèle.

# Intent : [titre]
Auteur : [nom] ([rôle]).
## Problème
## Résultat proposé
## Utilisateurs et systèmes concernés
## Contraintes
## Questions ouvertes

Présente un nouveau brouillon après chaque correction, jusqu'à sa validation.

## Enregistrer le contenu validé

Après validation, crée une nouvelle branche de travail depuis la branche
courante et place-toi dessus avant toute écriture dans `intent/`. Utilise un
nom disponible sous `claude/intent-<slug>` et respecte les contraintes de
nommage de l'environnement. Si la création ou le changement de branche
échoue, arrête-toi sans écrire le fichier et explique le problème.

Sur cette branche, crée ou mets à jour `intent/<slug>/intent.md`.
Affiche le nom de la branche, le chemin et le contenu complet du fichier.

Propose ensuite de créer une pull request vers `main` pour soumettre
l'intention au Product Owner. Précise que cette demande permettra de relire
le document avant de décider de son passage à la phase Design. Attends une
confirmation avant toute opération de commit, de push ou de création de
pull request. Ne merge jamais la pull request.
