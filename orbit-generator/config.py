#
# SeleNet
#
# Authors : Nada Yassine, Meli Scott Douanla 
#

import os 

# --- CHEMIN ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR_BACKEND = CURRENT_DIR 

KERNEL_DIR = os.path.join(BASE_DIR_BACKEND, 'kernels')

DB_FILE = os.path.join(BASE_DIR_BACKEND, 'satellites_db.json')

OUTPUT_DIR = os.path.join(BASE_DIR_BACKEND, '..', 'visualization-app', 'public')

ANALYSIS_DIR = os.path.join(BASE_DIR_BACKEND, '..', 'contacts-analysis')

OUTPUT_FILENAME = 'global_simu_data.czml'

# --- SIMULATION PARAMETERS ---
PAS_EN_SECONDES = 30
NOMBRE_DE_POINTS = 5000

# --- PHYSICAL CONTACT THRESHOLD ---
DISTANCE_CONTACT_KM = 5000 # Max distance for inter-satellite contact in km

# --- COLORS ---
COULEURS_SATELLITES = [
    [255, 0, 0, 255],    # Red
    [0, 255, 0, 255],    # Green
    [0, 0, 255, 255],    # Blue
    [255, 255, 0, 255],  # Yellow
    [0, 255, 255, 255],  # Cyan
    [255, 0, 255, 255],  # Magenta
    [255, 165, 0, 255]   # Orange
]
# --- RADIO CHARACTERISTICS ---

P_TX = 14 # dBm
G_TX = 2 # dB 
G_RX = 5 # dB
FREQ_MHZ = 868 # MHz
P_THREASHOLD = -141 # dBm

MIN_ELEVATION = 5

