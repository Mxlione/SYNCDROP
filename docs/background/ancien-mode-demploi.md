# SyncDrop — Mode d'emploi

SyncDrop transfère des fichiers entre deux appareils **en direct (P2P), sans passer par un serveur ni le cloud**. Tout est chiffré de bout en bout (AES-256).

---

## 1. Les deux fichiers à récupérer

| Plateforme | Fichier | Emplacement |
|---|---|---|
| Android | `app-release.apk` (118 Mo) | `mobile/android/app/build/outputs/apk/release/app-release.apk` |
| Linux | `syncdrop_2.4.0_amd64.deb` (75 Mo) | `desktop/release/syncdrop_2.4.0_amd64.deb` |

---

## 2. Installation sur Android

### Méthode A — avec `adb` (débogage USB activé)
```bash
adb install app-release.apk
```

### Méthode B — sans `adb` (recommandé pour les tests)
1. Copier `app-release.apk` sur le téléphone (câble USB, clé USB, ou envoi par mail/Bluetooth).
2. Sur le téléphone, ouvrir le fichier `.apk` (via le gestionnaire de fichiers ou les notifications).
3. Android demande l'autorisation **« Installer des applications inconnues »** → l'accepter pour le gestionnaire de fichiers utilisé.
4. Confirmer l'installation. L'application **SyncDrop** apparaît dans le tiroir d'applications.

> ⚠️ L'APK n'est pas signé par le Play Store : c'est normal pour une version de test. Android affichera un avertissement, c'est attendu.

---

## 3. Installation sur Linux (Debian / Ubuntu / dérivés)

```bash
sudo apt install ./syncdrop_2.4.0_amd64.deb
```

Les dépendances (libgtk-3-0, libnss3, libxss1, libxtst6, xdg-utils…) sont résolues automatiquement par `apt`.

### Lancement
- Menu des applications → **SyncDrop** (catégorie Réseau), ou
- Terminal : `syncdrop`

### Désinstallation
```bash
sudo apt remove syncdrop
```

---

## 4. Premier lancement

1. Ouvrir SyncDrop sur les **deux** appareils (ex. : téléphone Android + PC Linux).
2. Les deux appareils doivent être sur le **même réseau Wi-Fi / LAN** (ex. : même box).
3. L'écran d'accueil affiche la **recherche d'appareils** : le réseau est scanné automatiquement, les appareils SyncDrop voisins apparaissent dans la liste « Appareils détectés ».

---

## 5. Appairage de deux appareils

### Option A — détection automatique
1. Sur l'appareil A, l'appareil B apparaît dans « Appareils détectés » (avec son nom et son IP).
2. Toucher l'appareil B → la connexion s'établit directement.

### Option B — code QR
1. Sur l'appareil A : **« Connecter un appareil »** → l'écran d'appairage affiche un **QR code** + un **code PIN** (ex. `749 - 283`), valable 5 minutes.
2. Sur l'appareil B : scanner le QR code avec l'appareil photo ou saisir le code PIN.
3. La session est sécurisée par un jeton éphémère — aucun serveur externe n'est impliqué.

---

## 6. Transférer des fichiers

1. Une fois connectés, l'écran **Transferts** affiche l'appareil lié en haut.
2. **« Parcourir mes fichiers »** (ou glisser-déposer sur desktop) → choisir photos, vidéos, documents. Pas de limite de taille.
3. La progression s'affiche en temps réel (vitesse en Mo/s, temps restant).
4. Les fichiers reçus arrivent dans le dossier de réception :
   - Android : dossier de réception SyncDrop (configurable dans **Paramètres → Dossier de réception**)
   - Linux : `/Téléchargements/SyncDrop` par défaut

---

## 7. Paramètres utiles

Dans l'onglet **Paramètres** :
- **Nom de diffusion** : nom visible par les autres appareils
- **Visibilité publique** : détectable ou non par les pairs du réseau
- **Acceptation automatique** : pour les pairs certifiés uniquement (recommandé)
- **Appareils de confiance** : liste des appareils déjà certifiés
- **Tester le débit** : diagnostic de vitesse Wi-Fi Direct

---

## 8. Dépannage rapide

| Problème | Solution |
|---|---|
| « Aucun appareil détecté » | Vérifier que les deux appareils sont sur le **même réseau** ; désactiver le pare-feu ou autoriser SyncDrop ; relancer le scan. |
| Le QR code expire | Toucher **« Régénérer le code »** (valable 5 min). |
| Images de démo non affichées | Les visuels de démonstration sont chargés depuis Internet — vérifier la connexion. |
| L'app Linux ne démarre pas | `sudo apt install -f` pour réparer les dépendances, puis relancer `syncdrop`. |
| Transfert lent | Privilégier le Wi-Fi 5 GHz ; éloigner les obstacles entre les appareils. |