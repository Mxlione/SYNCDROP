# 📂 SyncDrop

> Transférez des fichiers entre vos appareils sur un même Wi-Fi. Rien à installer en face,
> rien d'hébergé nulle part, rien qui sorte de votre réseau.

![Status](https://img.shields.io/badge/statut-pre--alpha-orange)
![License](https://img.shields.io/badge/licence-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Dependencies](https://img.shields.io/badge/d%C3%A9pendances-aucune-brightgreen)

*Read this in [English](README.md).*

---

## L'idée

Un appareil lance SyncDrop. Il affiche une adresse. Tous les autres ouvrent cette adresse dans
un navigateur.

```
$ python3 -m syncdrop

  SyncDrop is ready.

      http://192.168.1.42:8080

  Open that on your phone. There is nothing to install.
  Ctrl-C to stop.
```

C'est tout le produit. Le téléphone n'a besoin d'aucune application, d'aucun compte, d'aucun
magasin d'applications et d'aucune connexion internet. Il a besoin d'un navigateur, qu'il a déjà.

```
   Un appareil le lance                        Tous les autres
   ┌───────────────────────────┐                ┌──────────────────┐
   │   python3 -m syncdrop     │                │    navigateur    │
   │                           │                │                  │
   │   http://192.168.1.42:8080│←── Wi-Fi local│  ouvrent cette   │
   │   [ QR code ]             │                │  adresse         │
   └───────────────────────────┘                └──────────────────┘

   Pas de cloud. Pas de compte. Pas de déploiement. Rien ne sort du réseau local.
```

---

## Pourquoi pas une application

Xender, AirDroid et les autres fonctionnent, et tous demandent d'installer quelque chose des
deux côtés. C'est cette partie-là qui mérite d'être supprimée.

- **Pas d'application desktop.** Electron embarque 900 Mo de `node_modules` pour dessiner une
  fenêtre que le navigateur de la même machine dessine déjà.
- **Pas d'application mobile.** Une validation de magasin, 100 Mo à télécharger et une boîte de
  dialogue de permissions, pour déplacer une photo d'un bout à l'autre d'une pièce.
- **Pas de cloud.** Rien à héberger, rien à payer, et aucun tiers qui détient vos fichiers
  pendant le transfert.

Il reste un programme assez petit pour être lu en une après-midi, et une page web.

---

## Installation

Il n'y a rien à installer sur l'appareil qui reçoit. Jamais. Sur celui qui le lance :

```bash
pip install syncdrop
syncdrop
```

Ou depuis une copie du dépôt, avec rien d'autre que Python :

```bash
PYTHONPATH=src python3 -m syncdrop
```

Un fichier `.py` unique à télécharger, sans dépôt et sans `pip`, c'est la
[tâche 39](TASKS.md#phase-8--v10--documentation-and-packaging) et ça n'existe pas encore.

SyncDrop n'a **aucune dépendance d'exécution**. Tout ce dont il a besoin est dans la
bibliothèque standard de Python, y compris l'encodeur de QR codes. C'est délibéré : il doit
fonctionner sur une machine qui n'a aucun réseau pour installer quoi que ce soit, puisque
fonctionner sans internet est tout l'intérêt.

---

## État

Développement initial. Rien n'est encore publié.

| | |
|---|---|
| Choix de la bonne adresse réseau | 🟢 fonctionne |
| QR code | 🟢 fonctionne |
| Envoi et réception | ⬜ pas commencé |
| Appairage | ⬜ pas commencé |
| Interface web | ⬜ pas commencé |

**Sur une machine à six adresses, dont cinq sont fausses.** La première chose que fait SyncDrop
est de décider quelle adresse afficher, et c'est la première chose qui peut échouer en silence :
un portable avec Docker, libvirt et LXC installés a six adresses IPv4, et exactement une que le
téléphone peut joindre. Affichez l'une des cinq autres et la page ne charge simplement jamais,
sans la moindre erreur pour l'expliquer.

SyncDrop note chaque adresse trouvée et dit sur quoi il s'est fondé :

```
 score  interface          address          why
   140  wlp0s20f3          192.168.226.126  the route the system itself would take, named like real hardware
     0  lo                 127.0.0.1        loopback, reaches nothing but this machine
  -135  docker0            172.17.0.1       named like a virtual interface, in a range virtualisation hands itself, …
  -135  virbr0             192.168.122.1    named like a virtual interface, in a range virtualisation hands itself, …
```

Le QR code est encodé par SyncDrop lui-même, pour tenir la promesse « aucune dépendance ».
Il est vérifié module par module contre un encodeur indépendant, sur les versions 1 à 10, les
quatre niveaux de correction et les huit masques — 1280 symboles, zéro différence. Écrire cette
vérification a révélé trois bugs réels, dont chacun produisait un symbole qui ressemblait
parfaitement à un QR code et ne se scannait pas.

---

## Feuille de route

- [ ] **v0.1** — Choix de la bonne adresse, et le QR code
- [ ] **v0.2** — Envoi et réception, avec de gros fichiers
- [ ] **v0.3** — Appairage : QR code, code PIN, sessions
- [ ] **v0.4** — Interface web
- [ ] **v0.5** — Progression en direct, plusieurs appareils à la fois
- [ ] **v0.6** — Dossiers, file d'attente, reprise, presse-papier partagé
- [ ] **v1.0** — Documentation, packaging, un fichier unique à télécharger

Le détail des tâches est dans [TASKS.md](TASKS.md).

---

## Cadre d'usage

SyncDrop déplace vos fichiers entre vos appareils, sur un réseau que vous contrôlez. Il n'a pas
d'authentification au-delà d'un jeton de session : tant qu'il tourne, quiconque est sur le même
réseau et connaît l'adresse peut s'en servir. Ne le laissez pas tourner sur un réseau auquel
vous ne faites pas confiance.

---

## Licence

MIT — voir [LICENSE](LICENSE).
