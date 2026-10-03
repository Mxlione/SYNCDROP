# Cahier des Charges
## Application de Transfert de Fichiers PC ↔ Téléphone via Tunnel Local (sans connexion Internet)

---

## 1. Contexte et Objectif du Projet

De nombreux utilisateurs ont besoin de transférer rapidement des fichiers (photos, documents, vidéos, APK, etc.) entre un ordinateur et un smartphone sans dépendre d'une connexion Internet, d'un câble USB, ou de services cloud tiers (Google Drive, WhatsApp, etc.), souvent lents, limités en taille, ou nécessitant une connexion réseau externe.

**Objectif principal :** développer une application (PC + Mobile) permettant de créer un tunnel de communication local direct entre les deux appareils, afin d'échanger des fichiers rapidement, en toute confidentialité, sans passer par Internet.

---

## 2. Objectifs Spécifiques

- Permettre le transfert de fichiers dans les deux sens (PC → téléphone et téléphone → PC).
- Fonctionner entièrement en local, sans nécessiter d'accès Internet.
- Offrir une connexion simple et rapide (appairage en quelques secondes).
- Garantir la confidentialité des données transférées (aucune donnée ne transite par un serveur externe).
- Supporter des fichiers volumineux (vidéos, archives, etc.).
- Être multiplateforme (Windows/Mac/Linux pour le PC, Android/iOS pour le mobile).

---

## 3. Périmètre Fonctionnel

### 3.1 Fonctionnalités incluses (MVP)
- Découverte automatique des appareils sur le même réseau local ou via Wi-Fi Direct.
- Appairage sécurisé (QR code ou code PIN).
- Envoi/réception de fichiers (glisser-déposer sur PC, sélection sur mobile).
- Barre de progression du transfert.
- Historique des fichiers transférés.
- Notification de fin de transfert.

### 3.2 Fonctionnalités avancées (V2)
- Transfert de dossiers entiers.
- Transfert multi-fichiers en file d'attente.
- Reprise du transfert en cas d'interruption.
- Chiffrement de bout en bout des fichiers transférés.
- Mode "presse-papier partagé" (copier sur PC, coller sur mobile et inversement).
- Support multi-appareils (plusieurs téléphones connectés simultanément).

### 3.3 Hors périmètre
- Synchronisation automatique en arrière-plan (type cloud).
- Stockage distant des fichiers.
- Streaming audio/vidéo en direct.

---

## 4. Acteurs du Système

| Acteur | Rôle |
|---|---|
| Utilisateur PC | Envoie/reçoit des fichiers depuis son ordinateur |
| Utilisateur Mobile | Envoie/reçoit des fichiers depuis son smartphone |
| Application PC (Desktop) | Interface et moteur de transfert côté ordinateur |
| Application Mobile | Interface et moteur de transfert côté smartphone |

---

## 5. Approches Techniques Possibles pour le "Tunnel sans Internet"

Puisque le mot "Internet" est exclu, le transfert doit passer par une couche réseau locale. Voici les options possibles, à choisir selon le niveau de contrainte souhaité :

| Option | Description | Avantages | Contraintes |
|---|---|---|---|
| **Wi-Fi local (LAN)** | Les deux appareils sont connectés au même réseau Wi-Fi (routeur), sans accès Internet actif requis | Simple à mettre en œuvre (HTTP/WebSocket local) | Nécessite un routeur ou point d'accès Wi-Fi commun |
| **Hotspot du téléphone/PC** | Le téléphone crée un point d'accès Wi-Fi local, le PC s'y connecte (ou inversement) | Fonctionne sans routeur externe | Coupe l'accès Internet du téléphone pendant l'opération |
| **Wi-Fi Direct** | Connexion directe pair-à-pair entre les deux appareils, sans routeur | Pas besoin de réseau existant | Support natif variable selon OS (bien supporté sur Android, plus complexe sur iOS) |
| **USB (câble)** | Connexion filaire créant une interface réseau locale (ADB, RNDIS) | Rapide et fiable, aucune interférence | Nécessite un câble et des pilotes spécifiques |
| **Bluetooth** | Connexion sans fil basse consommation | Pas de configuration réseau | Débit plus faible, moins adapté aux gros fichiers |

**Recommandation :** démarrer avec le **Wi-Fi local / Hotspot** pour le MVP (le plus simple à développer et le plus rapide en débit), puis ajouter le Wi-Fi Direct et le mode USB en V2.

---

## 6. Architecture Technique Proposée

### 6.1 Vue d'ensemble
```
[Application PC]  <---- Tunnel local (Wi-Fi/Hotspot/WiFiDirect) ---->  [Application Mobile]
     |                                                                        |
 Serveur HTTP/WebSocket local                                    Client + Serveur HTTP/WebSocket local
     |                                                                        |
 Découverte réseau (mDNS/Bonjour ou UDP Broadcast)  <----------------->  Découverte réseau
```

### 6.2 Stack technique suggérée

| Composant | Technologie suggérée |
|---|---|
| Application Desktop | Electron, Tauri (plus léger) ou application native (C#/.NET, Python+Qt) |
| Application Mobile | Flutter ou React Native (code partagé Android/iOS) |
| Protocole de transfert | HTTP local (serveur embarqué) ou WebSocket pour le suivi temps réel |
| Découverte des appareils | mDNS/Bonjour (NSD sur Android, Bonjour sur iOS/Mac) ou UDP Broadcast |
| Appairage/sécurité | Génération de QR code contenant IP + port + token de session |
| Chiffrement | TLS local auto-signé ou chiffrement symétrique (AES) par session |

### 6.3 Sécurité
- Chaque session de transfert utilise un token unique généré à l'appairage (via QR code ou code PIN à 6 chiffres).
- Aucune donnée ne doit transiter par un serveur tiers : tout reste sur le réseau local.
- Option de chiffrement des fichiers pendant le transfert (AES-256).
- Expiration automatique de la session après transfert ou inactivité.

---

## 7. Étapes de Réalisation du Projet

### Étape 1 — Cadrage et spécifications
- Valider le périmètre fonctionnel (MVP vs fonctionnalités avancées).
- Choisir la méthode de connexion prioritaire (Wi-Fi local recommandé pour commencer).
- Définir les plateformes cibles (Windows/Mac/Linux, Android/iOS).

### Étape 2 — Conception technique
- Définir l'architecture réseau (serveur/client, protocole de communication).
- Concevoir le mécanisme de découverte et d'appairage des appareils.
- Définir le format des métadonnées de transfert (nom fichier, taille, type, checksum).

### Étape 3 — Développement du cœur de transfert (Core Engine)
- Implémenter le serveur local sur PC et sur mobile.
- Implémenter la découverte réseau automatique.
- Implémenter l'envoi/réception de fichiers avec suivi de progression.
- Gérer les erreurs réseau (déconnexion, timeout).

### Étape 4 — Développement de l'interface utilisateur
- Interface PC : glisser-déposer, liste des appareils détectés, historique.
- Interface Mobile : sélection de fichiers, scan QR code, historique.
- Notifications de statut (connexion, transfert en cours, terminé, erreur).

### Étape 5 — Sécurisation
- Ajouter l'appairage sécurisé (QR code / PIN).
- Ajouter le chiffrement des transferts.
- Gérer l'expiration des sessions.

### Étape 6 — Tests
- Tests unitaires sur le moteur de transfert.
- Tests d'intégration sur différents réseaux (LAN, hotspot, Wi-Fi Direct).
- Tests de charge (gros fichiers, transferts multiples).
- Tests de compatibilité multiplateforme.

### Étape 7 — Optimisation et fonctionnalités avancées
- Reprise de transfert interrompu.
- Transfert de dossiers complets.
- Support multi-appareils simultanés.

### Étape 8 — Packaging et déploiement
- Empaquetage de l'application PC (installateur Windows/Mac/Linux).
- Publication mobile (APK direct ou Play Store / App Store).
- Documentation utilisateur.

### Étape 9 — Maintenance et évolutions
- Corrections de bugs post-lancement.
- Ajout de nouvelles méthodes de connexion (Bluetooth, USB).
- Retours utilisateurs et amélioration continue.

---

## 8. Critères d'Acceptation

- [ ] Le transfert fonctionne sans connexion Internet active sur les deux appareils.
- [ ] L'appairage entre PC et mobile prend moins de 10 secondes.
- [ ] Le transfert d'un fichier de 500 Mo se fait sans erreur ni corruption.
- [ ] L'utilisateur voit une progression en temps réel du transfert.
- [ ] Les fichiers reçus sont accessibles immédiatement après transfert.
- [ ] L'application fonctionne sur au moins Windows + Android en V1.

---

## 9. Livrables Attendus

1. Application Desktop (Windows, extensible Mac/Linux).
2. Application Mobile (Android, extensible iOS).
3. Documentation technique (architecture, protocole de communication).
4. Guide utilisateur (installation, appairage, utilisation).
5. Code source versionné (Git).

---

## 10. Planning Indicatif (à titre d'exemple)

| Phase | Durée estimée |
|---|---|
| Cadrage & conception | 1 semaine |
| Développement core (transfert + découverte) | 2-3 semaines |
| Développement interfaces PC/Mobile | 2 semaines |
| Sécurisation | 1 semaine |
| Tests | 1-2 semaines |
| Packaging & documentation | 1 semaine |
| **Total estimé** | **8-10 semaines** |

---

*Document généré comme base de travail — à ajuster selon les contraintes techniques réelles (plateformes ciblées, budget, équipe disponible).*
