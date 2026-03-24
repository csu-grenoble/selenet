# SeleNet :: Moteur de Calcul

Ce dossier contient les scripts Python et les données nécessaires pour calculer les positions précises des satellites (LRO, Clementine, Apollo) autour de la Lune et générer les fichiers de visualisation pour Cesium.

## 1. Présentation
Le module utilise [SPICE](https://naif.jpl.nasa.gov/naif/) via la bibliothèque [SpicePy](https://spiceypy.readthedocs.io/en/stable/index.html), une interface python développée par les ingénieurs de la NASA.

**SPICE** est la bibliothèque officielle de la NASA (NAIF) pour la navigation spatiale.

Dans ce projet, nous utilisons celles-ci pour :
* lire les fichiers de données de la NASA (appelés "Kernels").
* convertir les dates humaines en temps machine précis.
* calculer les coordonnées X, Y, Z des satellites seconde par seconde.

## 2. Installation (Première fois)

Avant de lancer quoi que ce soit, il faut préparer l'environnement Python pour ne pas polluer votre ordinateur.

Ouvrez un terminal à la racine du dossier **orbit-generator** et lancez :

```bash
# 1. Créer un environnement virtuel 
python3 -m venv .venv

# 2. Activer l'environnement
# Sur Linux / Mac :
source .venv/bin/activate
# Sur Windows :
# .venv\Scripts\activate

# 3. Installer les librairies requises (SPICE et Numpy)
pip install spiceypy numpy matplotlib
```

## 3. Lancement
Une fois l'environnement mis en place, il faut se placer dans le dossier **src/**. 

Lancer la commande `python src/main.py` ou `python3 src/main.py`

Cette commande va permettre de générer à la fin le fichier CZML qui sera utilisé par la partie visuelle.

## 4. Structure du code et fonctions
Le module est structuré pour etre modulaire et automatisé.

Voici l'explication de chaque dossier et fichiers :

* **`kernels/`** : Le dossier le plus important. Il contient les données brutes de la NASA.
    - `*.bsp` (SPK) : Les fichiers de Position (Trajectoire de la Lune, de LRO, etc.).
    - `*.tls` (LSK) : Le fichier de Temps (Gère les secondes intercalaires).
  
* **`src/`** : 
  * **`managers/`** : ce dossier gère les entités.
  * **`utils/`** : ce dossier 
    * centralise des fonctions utilitaires pour la manipulation de la bibliothèque SpiceyPy (`spice_utils.py`) et la génération de paquets au format `CZML` (`czml_utils.py`).
    * regoupe l'ensemble des algorithmes pour le calcul des liens de communication et les effets Doppler
    * intègre des outils de performance (`perf_utils.py`)
  
* **`config.py`** : Ce fichier centralise les paramètres globaux du moteur de calcul, tels que les chemins d'accès aux Kernels SPICE, les pas de temps de simulation et les constantes physiques pour les bilans de liaison.
  
* **`ground_objects.db.json`** : Ce fichier répertorie les coordonnées géographiques (latitude, longitude, altitude) de tous les objets/points fixes sur le sol lunaire.
  
* **`satellites.db.json`** : Ce fichier répertorie les caractéristiques techniques concernant les satellites étudiés.

* **`main.py`** : Ce fichier sert d'orchestrateur principal du projet; il appelle les différents managers pour faire tous les calculs et générer le fichier `CZML` final regroupant toutes les entités.


## 5. Algorithme et concepts techniques

Cette section détail la logique derriere le moteur orbit-generator. Le passage des données de la NASA (kernel) à une visualisation et des analyses de communication repose sur trois piliers : la gestion des référentiels, le calcul géométrique et la modélisation physique du signal.

### 5.1 Référentiel et coordonnnées

Le calcul des positions dans l'espace nécessite une définition du repère utilisé. Dans ce projet nous avons utilisé le référentiel J2000 proposé par SPICE. 

  Ce référentiel est utilisé pour calculer des trajectoires orbitales. C'est un repère fixe par rapport aux étoiles lointaines.

Or apres coup, ce référentiel n'est pas la meilleur option. Il faudrait opté pour le référentiel IAU_MOON.

#### 5.1.1 Transformation des données des kernels en position X,Y,Z

Cette étape est le point de passage entre les fichiers binaires bruts (`.bsp`) et les coordonnées cartésiennes utilisables pour la simulation.

1. Appel depuis la fonction **process_all_satellites**

     positions_km = spice_utils.compute_trajectory(
    id_sat, et_start, config.NUMBER_OF_STEPS, config.SECONDS_PER_STEP)

2. Calcul des positions dans la fonction **compute_trajectory**
   
La fonction spkpos interroge les kernels chargés en mémoire le vecteur de position d'un objet par rapport à un autre à un instant précis. Elle effectue une interpolation mathématique définis dans les fichiers de la NASA (`.bsp`). 

        pos, _ = spice.spkpos(str(id_sat), et_current, 'J2000', 'NONE', 'MOON')
        
        x, y, z = pos[0], pos[1], pos[2]

        positions.extend([elapsed, x, y, z])

### 5.2 Calcul de Position et Éléments Orbitaux

Pour chaque satellite, le script `main.py` effectue une itération temporelle (pas de temps défini dans config.py).

- **Conversion Temporelle** : Passage du format UTC (ISO 8601) au temps SPICE.

- **Calcul d'État** : Utilisation de la fonction spkpos pour récupérer le vecteur de position relative.

- **Génération CZML** : Les positions sont stockées.

### 5.3 Analyse de visibilité (lien de communication)
#### 5.3.1 Lien de communication inter-satellites

Le calcul de la connectivité entre deux satellites repose sur une validation de la distance Euclidienne. 
Pour chaque instant t de la simulation, le moteur calcule la distance relative entre les deux entités dans la fonction **`find_communication_link`** : 

    v1 = sat1['positions_xyz'][t]
    v2 = sat2['positions_xyz'][t]

    d = distance_3D(v1, v2)
    visible = d <= threshold


#### 5.3.2 Lien de communication satellite - point fixe

Dans ce cas, le calcul se fait en deux étape de validation

##### A.Validation Géométrique (Angle d'élévation)

Le satellite ne doit pas seulement etre proche, il doit etre au dessus de l'horizon local.

- **Vecteur Zénith** : Pour un point fixe (lat, lon), nous calculons le vecteur normal à la surface en utilisant le modèle de l'ellipsoïde lunaire via la fonction **`surfnm`** de la bibliothèque SPICE.

- **Calcul d'angle** : Nous calculons le vecteur entre le point fixe et le satellite. L'angle entre ce vecteur et le zénith est obtenu par la fonction **`vsep`** de la bibliothèque SPICE.

- **Condition** : L'élévation est de 90∘−angle zénithal. Le lien est géométriquement possible si l'élévation est supérieure à un seuil (5∘ : ce seuil est pour l'instant choisi de manière arbitraire).

##### B. Bilan de liaison

Ensuite nous vérifions si le signal radio est physiquement exploitable par le récepteur. Pour cela nous calculons la puissance reçu au niveau du satellite en utilisant l'équation du bilan de liaison : 

    P_rx = G_t + G_r + P_tx - FSPL

**Composant du calcul** : 
- P_tx​ : Puissance de l'émetteur (dBm).
- Gt​ / Gr​ : Gains respectifs des antennes d'émission et de réception (dB).
- FSPL : Perte de propagation en espace libre (Free Space Path Loss).

La variable FSPL représente l'affaiblissement du signal lié à la distance. Elle est obtenue grâce à la formule simplifiée suivante :

    FSPL = 20log10​(d)+20log10​(f)−147.55

- d : Distance entre les deux entités (mètres).
- f : Fréquence de travail (Hertz).
- −147.55 : Constante de calcul incluant la vitesse de la lumière.

**Paramètre du modèle** : 

Dans cette première version du projet, les constantes physiques (puissance, gains, fréquences) sont centralisées dans le fichier `config.py`. Ces valeurs ont été définies en concertation avec les porteurs de projet pour correspondre aux spécifications techniques réelles des équipements embarqués. 

Le lien n'est considéré comme "actif" que si Prx​ est supérieur au seuil de sensibilité du récepteur, c'est-à-dire -140 dB (valeur choisie après concertation avec les porteurs du projet)


### 5.4 Décalage de fréquence - Effet Doppler
Lorsqu'un lien de communication est détecté entre un satellite et un point fixe au sol, nous calculons le décalage de fréquence et générons le graphe correspondant. 

Les calculs sont implémenté dans le fichier **`doppler_utils.py`** dans la fonction **`doppler_shifts`**.

#### 5.4.1 Calcul de la vitesse radiale relative
Pour calculer le Doppler, nous ne nous interessons pas à la vitesse absolue des satelittes, mais uniquement à leur vitesse radiale (la vitesse à laquelle ils s'approchent ou s'éloignent l'un de l'autre).

Le moteur utilise les vecteurs d'état fournis par SPICE (qui contiennent la position et la vitesse [P,V]) pour effectuer ce calcul :

    Vecteur Vitesse Relative : Vrel​=Vsat2​−Vsat1​

#### 5.4.2 Calcul du décalage de fréquence
Le décalage Doppler *delta_f* est calculé selon la formule : 

    Δf= v_r / c_light ​​⋅f0​

où : 
- `v_r`​ : Vitesse radiale (m/s).
- `c_light` : Vitesse de la lumière (≈299792458 m/s).
- `f0`​ : Fréquence nominale de la porteuse (Hz) définie dans `config.py` (FREQ_MHZ).


## References
* SPICE : An Observation Geometry System for Space Science Missions https://naif.jpl.nasa.gov/naif/
  * https://naif.jpl.nasa.gov/naif/tutorials.html
  * https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/
* Annex et al., (2020). SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit. Journal of Open Source Software, 5(46), 2050, https://doi.org/10.21105/joss.02050
* SpicePy documentation https://spiceypy.readthedocs.io/en/stable/index.html