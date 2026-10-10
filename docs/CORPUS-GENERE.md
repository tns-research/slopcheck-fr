# Corpus généré d'octobre 2026 (`bench/genere-2026-10/`)

224 textes écrits le 9 octobre 2026 par quatre modèles, sans aucune consigne de style : Claude Haiku, Sonnet et Opus (alias de Claude Code 2.1.295) et GPT-5.6 (Codex CLI 0.159.1). Chaque fichier s'appelle `modele-genre[-vN].md`.

Ils servent à mesurer ce que slopcheck relève sur la production courante des modèles. Les cinq règles ajoutées en 0.2.0 (`emoji-tete`, `hashtags`, `rituel-reseau`, `contraste-appose`, `mot-gonfle`) et l'élargissement de `puces-gras-serie` ont été réglés sur ces textes : la mesure y est donc optimiste. `bench/ia-controle/` reste le corpus que personne n'a lu pour écrire des règles.

Les textes sont bruts, à une retouche près : dans `opus-lettre-motiv.md`, le modèle avait recopié une adresse email réelle tirée de son contexte, remplacée par `prenom.nom@exemple.fr`.

Quatorze genres, quatre demandes par genre (variante `-v2` à `-v4` = sujet voisin). Les demandes :

| Genre | Demande |
|---|---|
| `readme` | Écris le README en français d'un petit outil open source en ligne de commande qui convertit des factures PDF en CSV. Réponds uniquement avec le markdown du README. |
| `pr` | Écris la description en français d'une pull request qui ajoute un cache Redis devant l'API de recherche d'une app Django. Réponds uniquement avec le texte de la description. |
| `release` | Rédige en français les notes de version 2.0 d'une application mobile de gestion de budget. Réponds uniquement avec le texte. |
| `linkedin-dev` | Écris un post LinkedIn en français pour annoncer que je viens de publier en open source ma bibliothèque Python de validation de données. Réponds uniquement avec le post. |
| `lettre-motiv` | Écris une lettre de motivation en français pour un poste de développeuse front-end junior dans une agence web à Lyon. Réponds uniquement avec la lettre. |
| `blog-tech` | Écris un article de blog en français d'environ 500 mots sur les avantages de TypeScript pour une petite équipe. Réponds uniquement avec l'article en markdown. |
| `email-client` | Écris un email en français à un client pour lui annoncer un retard de deux semaines sur la livraison de son site e-commerce. Réponds uniquement avec l'email. |
| `avis` | Écris un avis Google en français sur un restaurant italien où j'ai bien mangé hier soir. Réponds uniquement avec l'avis. |
| `dissertation` | Rédige en français une courte dissertation (400 mots) sur la question : les réseaux sociaux favorisent-ils la démocratie ? Réponds uniquement avec le texte. |
| `fiche-airbnb` | Écris en français la description d'un appartement deux pièces à louer sur Airbnb à Nantes, près de la gare. Réponds uniquement avec la description. |
| `newsletter` | Écris en français la newsletter mensuelle d'une association de quartier qui organise un vide-grenier et un atelier de réparation de vélos. Réponds uniquement avec le texte. |
| `discours` | Écris en français un discours de deux minutes pour le pot de départ à la retraite d'un collègue comptable après 30 ans dans l'entreprise. Réponds uniquement avec le discours. |
| `doc-api` | Écris en français la page de documentation « Démarrage rapide » d'une API REST de paiement. Réponds uniquement avec le markdown. |
| `post-x` | Écris un thread X (Twitter) en français de 5 tweets sur ce que j'ai appris en lançant mon SaaS en solo. Réponds uniquement avec le thread. |
| `readme-v2` | Écris le README en français d'une application web open source de liste de courses partagée entre colocataires. Réponds uniquement avec le markdown du README. |
| `readme-v3` | Écris le README en français d'un script open source qui sauvegarde automatiquement les photos d'un téléphone Android sur un disque dur externe. Réponds uniquement avec le markdown du README. |
| `readme-v4` | Écris le README en français d'un plugin WordPress open source qui affiche les horaires d'ouverture d'une boutique sur sa page d'accueil. Réponds uniquement avec le markdown du README. |
| `pr-v2` | Écris la description en français d'une pull request qui corrige un bug d'affichage des dates sur le tableau de bord d'une application React. Réponds uniquement avec le texte de la description. |
| `pr-v3` | Écris la description en français d'une pull request qui ajoute l'authentification à deux facteurs sur le site d'une mutuelle de santé. Réponds uniquement avec le texte de la description. |
| `pr-v4` | Écris la description en français d'une pull request qui refactorise le module d'envoi d'emails d'une application Ruby on Rails. Réponds uniquement avec le texte de la description. |
| `release-v2` | Rédige en français les notes de version 3.4 d'un logiciel de caisse pour boulangeries. Réponds uniquement avec le texte. |
| `release-v3` | Rédige en français les notes de version 1.2 d'une application de méditation guidée pour iPhone. Réponds uniquement avec le texte. |
| `release-v4` | Rédige en français les notes de version 5.0 d'un outil de planification de tournées pour livreurs indépendants. Réponds uniquement avec le texte. |
| `linkedin-dev-v2` | Écris un post LinkedIn en français pour annoncer que je viens de terminer ma formation de développeur web après six mois de reconversion. Réponds uniquement avec le post. |
| `linkedin-dev-v3` | Écris un post LinkedIn en français pour annoncer que mon équipe recrute deux développeurs back-end à Bordeaux. Réponds uniquement avec le post. |
| `linkedin-dev-v4` | Écris un post LinkedIn en français pour raconter ce que j'ai retenu de ma première conférence tech à Paris. Réponds uniquement avec le post. |
| `lettre-motiv-v2` | Écris une lettre de motivation en français pour un poste d'infirmière dans un service de pédiatrie à Toulouse. Réponds uniquement avec la lettre. |
| `lettre-motiv-v3` | Écris une lettre de motivation en français pour un contrat d'apprentissage en boulangerie-pâtisserie à Lille. Réponds uniquement avec la lettre. |
| `lettre-motiv-v4` | Écris une lettre de motivation en français pour un poste de chargé de communication dans une mairie de petite commune. Réponds uniquement avec la lettre. |
| `blog-tech-v2` | Écris un article de blog en français d'environ 500 mots sur les bonnes pratiques pour sauvegarder ses données personnelles à la maison. Réponds uniquement avec l'article en markdown. |
| `blog-tech-v3` | Écris un article de blog en français d'environ 500 mots pour expliquer à des débutants comment fonctionne le cloud. Réponds uniquement avec l'article en markdown. |
| `blog-tech-v4` | Écris un article de blog en français d'environ 500 mots sur l'intérêt du télétravail pour une PME de dix personnes. Réponds uniquement avec l'article en markdown. |
| `email-client-v2` | Écris un email en français à une cliente pour lui confirmer la date de son déménagement et lui rappeler les démarches à faire avant. Réponds uniquement avec l'email. |
| `email-client-v3` | Écris un email en français à un client pour lui proposer un rendez-vous afin de réviser son contrat d'assurance habitation. Réponds uniquement avec l'email. |
| `email-client-v4` | Écris un email en français à un client pour s'excuser d'une erreur de facturation et lui annoncer le remboursement. Réponds uniquement avec l'email. |
| `avis-v2` | Écris un avis Google en français sur un garage automobile qui a réparé ma voiture rapidement et à un prix correct. Réponds uniquement avec l'avis. |
| `avis-v3` | Écris un avis Google en français sur un coiffeur dont je suis déçu à cause d'une longue attente et d'une coupe ratée. Réponds uniquement avec l'avis. |
| `avis-v4` | Écris un avis Google en français sur un hôtel au bord de la mer où j'ai passé un week-end en famille. Réponds uniquement avec l'avis. |
| `dissertation-v2` | Rédige en français une courte dissertation (400 mots) sur la question : le travail est-il une condition du bonheur ? Réponds uniquement avec le texte. |
| `dissertation-v3` | Rédige en français une courte dissertation (400 mots) sur la question : peut-on tout pardonner ? Réponds uniquement avec le texte. |
| `dissertation-v4` | Rédige en français une courte dissertation (400 mots) sur la question : le progrès technique rend-il l'homme plus libre ? Réponds uniquement avec le texte. |
| `fiche-airbnb-v2` | Écris en français la description d'un chalet de montagne pour huit personnes à louer sur Airbnb à Chamonix, près des pistes. Réponds uniquement avec la description. |
| `fiche-airbnb-v3` | Écris en français la description d'un studio à louer sur Airbnb à Strasbourg, à deux pas du marché de Noël. Réponds uniquement avec la description. |
| `fiche-airbnb-v4` | Écris en français la description d'une maison de pêcheur avec jardin à louer sur Airbnb à La Rochelle. Réponds uniquement avec la description. |
| `newsletter-v2` | Écris en français la newsletter mensuelle d'un club de randonnée qui prépare une sortie en Vercors et une soirée raclette. Réponds uniquement avec le texte. |
| `newsletter-v3` | Écris en français la newsletter mensuelle d'une médiathèque municipale qui annonce une rencontre avec un auteur et un atelier de lecture pour enfants. Réponds uniquement avec le texte. |
| `newsletter-v4` | Écris en français la newsletter mensuelle d'une petite boutique de plantes qui lance ses nouveautés de printemps et un atelier de rempotage. Réponds uniquement avec le texte. |
| `discours-v2` | Écris en français un discours de deux minutes pour le mariage de ma meilleure amie, en tant que témoin. Réponds uniquement avec le discours. |
| `discours-v3` | Écris en français un discours de deux minutes pour la remise des diplômes d'un lycée professionnel, prononcé par le proviseur. Réponds uniquement avec le discours. |
| `discours-v4` | Écris en français un discours de deux minutes pour les 80 ans de mon grand-père, prononcé par son petit-fils. Réponds uniquement avec le discours. |
| `doc-api-v2` | Écris en français la page de documentation « Démarrage rapide » d'une API de météo destinée aux développeurs d'applications mobiles. Réponds uniquement avec le markdown. |
| `doc-api-v3` | Écris en français la page de documentation « Démarrage rapide » d'une bibliothèque JavaScript de graphiques interactifs. Réponds uniquement avec le markdown. |
| `doc-api-v4` | Écris en français la page de documentation « Démarrage rapide » d'une API de réservation de salles de réunion. Réponds uniquement avec le markdown. |
| `post-x-v2` | Écris un thread X (Twitter) en français de 5 tweets sur ce que j'ai appris en courant mon premier marathon. Réponds uniquement avec le thread. |
| `post-x-v3` | Écris un thread X (Twitter) en français de 5 tweets sur les erreurs à éviter quand on ouvre sa première boutique en ligne. Réponds uniquement avec le thread. |
| `post-x-v4` | Écris un thread X (Twitter) en français de 5 tweets sur mes conseils pour apprendre l'anglais en autodidacte. Réponds uniquement avec le thread. |
