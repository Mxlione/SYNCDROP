# Description des Pages — Application de Transfert de Fichiers PC ↔ Mobile
### (À fournir à Google Stitch pour la génération du design UI/UX)

---

## Contexte du produit

Application permettant de transférer des fichiers entre un PC et un smartphone via un tunnel local (Wi-Fi/Hotspot/Wi-Fi Direct), sans connexion Internet. Deux applications : une version **Desktop (PC)** et une version **Mobile**. Style souhaité : moderne, épuré, rassurant (confidentialité/sécurité), avec un accent sur la rapidité et la simplicité de connexion.

**Palette suggérée :** tons neutres (blanc/gris clair) avec une couleur d'accent unique (ex. bleu ou violet) pour les actions principales et les états de connexion/transfert.

---

## PARTIE A — Application Desktop (PC)

### Page 1 — Écran d'accueil / Recherche d'appareils
**Objectif :** permettre à l'utilisateur de voir les appareils disponibles sur le réseau local et de démarrer une connexion.

**Éléments à afficher :**
- En-tête avec le logo/nom de l'application.
- Grand bouton central "Connecter un appareil".
- Une liste/carte des appareils détectés automatiquement sur le réseau (icône téléphone + nom de l'appareil + statut "disponible").
- Indicateur de statut réseau (ex. "Connecté au réseau local : Nom_du_Wi-Fi").
- Icône d'accès aux paramètres en haut à droite.
- État vide : message "Aucun appareil détecté" avec une illustration simple + bouton "Générer un QR code pour connecter manuellement".

---

### Page 2 — Écran d'appairage (QR Code)
**Objectif :** afficher un QR code que l'utilisateur scanne depuis son téléphone pour établir la connexion.

**Éléments à afficher :**
- Titre "Scannez ce code depuis votre téléphone".
- QR code centré, grand format.
- Code PIN alphanumérique affiché en dessous du QR code (alternative au scan).
- Bouton "Annuler".
- Petit texte explicatif : "Assurez-vous que les deux appareils sont sur le même réseau".
- Animation ou indicateur de type "en attente de connexion...".

---

### Page 3 — Écran principal de transfert
**Objectif :** interface principale où l'utilisateur envoie/reçoit des fichiers une fois connecté.

**Éléments à afficher :**
- Bandeau supérieur indiquant l'appareil connecté (nom + icône + statut "Connecté").
- Grande zone centrale de glisser-déposer ("Déposez vos fichiers ici ou cliquez pour parcourir").
- Bouton "Parcourir mes fichiers".
- Liste des transferts en cours avec, pour chaque fichier : nom, taille, barre de progression, vitesse de transfert, bouton annuler.
- Section "Fichiers reçus récemment" (miniatures ou icônes selon le type de fichier).
- Bouton de déconnexion discret.

---

### Page 4 — Historique des transferts
**Objectif :** lister tous les fichiers envoyés/reçus précédemment.

**Éléments à afficher :**
- Barre de recherche/filtrage (par nom, date, type de fichier).
- Tableau ou liste avec colonnes : nom du fichier, direction (envoyé/reçu), appareil, date, taille, statut.
- Icône "Ouvrir le dossier" et "Supprimer de l'historique" pour chaque ligne.
- Filtres rapides en haut (Tous / Envoyés / Reçus / Aujourd'hui).

---

### Page 5 — Paramètres
**Objectif :** configurer l'application.

**Éléments à afficher :**
- Sections : Général, Réseau, Sécurité, Stockage, À propos.
- Général : dossier de destination par défaut des fichiers reçus, démarrage automatique.
- Réseau : mode de connexion préféré (Wi-Fi local / Hotspot / Wi-Fi Direct), nom de l'appareil affiché aux autres.
- Sécurité : activer le chiffrement des transferts, gestion des appareils de confiance, expiration des sessions.
- À propos : version de l'application, lien support.

---

## PARTIE B — Application Mobile

### Page 1 — Écran de démarrage (Splash)
**Objectif :** écran de lancement de l'application.

**Éléments à afficher :**
- Logo centré.
- Nom de l'application.
- Indicateur de chargement discret.

---

### Page 2 — Écran d'accueil / Connexion
**Objectif :** point d'entrée principal pour se connecter à un PC.

**Éléments à afficher :**
- Deux gros boutons d'action : "Scanner un QR code" et "Voir les appareils à proximité".
- Liste des appareils détectés automatiquement (nom + icône PC + statut).
- Icône paramètres en haut à droite.
- Indicateur de statut réseau en haut (nom du réseau Wi-Fi actuel).

---

### Page 3 — Écran de scan QR Code
**Objectif :** scanner le QR code affiché sur le PC pour se connecter.

**Éléments à afficher :**
- Vue caméra plein écran avec cadre de visée centré.
- Texte d'instruction en haut : "Alignez le QR code dans le cadre".
- Bouton alternatif en bas : "Entrer le code manuellement".
- Bouton retour en haut à gauche.

---

### Page 4 — Écran de sélection de fichiers à envoyer
**Objectif :** permettre à l'utilisateur de choisir les fichiers/dossiers à envoyer au PC.

**Éléments à afficher :**
- Onglets ou filtres en haut : Photos, Vidéos, Documents, Applications, Tous les fichiers.
- Grille de miniatures (pour photos/vidéos) ou liste (pour documents), avec cases à cocher pour sélection multiple.
- Barre inférieure fixe affichant : nombre de fichiers sélectionnés + taille totale + bouton "Envoyer".

---

### Page 5 — Écran de transfert en cours
**Objectif :** afficher la progression du transfert (envoi ou réception).

**Éléments à afficher :**
- Icône ou miniature du fichier en cours de transfert.
- Barre de progression circulaire ou linéaire avec pourcentage.
- Vitesse de transfert et temps restant estimé.
- File d'attente des fichiers suivants (liste compacte en dessous).
- Bouton "Annuler" et bouton "Mettre en arrière-plan".

---

### Page 6 — Écran de confirmation / réception
**Objectif :** informer l'utilisateur qu'un fichier a été reçu.

**Éléments à afficher :**
- Notification en haut de l'écran (bannière) : "Fichier reçu : nom_du_fichier".
- Aperçu du fichier reçu (miniature si image/vidéo, icône si document).
- Boutons d'action rapide : "Ouvrir", "Partager", "Supprimer".

---

### Page 7 — Historique des transferts
**Objectif :** consulter les fichiers envoyés/reçus précédemment.

**Éléments à afficher :**
- Barre de recherche en haut.
- Liste chronologique groupée par date (Aujourd'hui, Hier, plus ancien).
- Chaque élément : miniature/icône, nom du fichier, direction (flèche entrante/sortante), taille, heure.
- Filtres rapides : Tous / Envoyés / Reçus.

---

### Page 8 — Paramètres
**Objectif :** configuration de l'application mobile.

**Éléments à afficher :**
- Nom de l'appareil (modifiable).
- Dossier de destination des fichiers reçus.
- Activer/désactiver le chiffrement.
- Gestion des appareils de confiance (liste des PC déjà appairés, option de suppression).
- Section "À propos" (version, aide, contact support).

---

## Notes générales pour Google Stitch

- Prévoir une version **claire (light mode)** et éventuellement une version **sombre (dark mode)**.
- Les écrans de connexion/transfert doivent transmettre une sensation de **sécurité et de fluidité** (icônes de cadenas, animations de progression douces).
- Cohérence visuelle entre l'application PC et l'application mobile (même palette, même typographie, mêmes icônes).
- Prioriser une **navigation simple à 3-4 destinations principales** sur mobile (ex. Accueil, Transfert, Historique, Paramètres) via une barre de navigation basse.
