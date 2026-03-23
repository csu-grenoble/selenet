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

SATELLITES_DB_FILE = os.path.join(BASE_DIR_BACKEND, 'satellites.db.json')

GROUND_OBJECTS_DB_FILE = os.path.join(BASE_DIR_BACKEND, 'ground_objects.db.json')

OUTPUT_DIR = os.path.join(BASE_DIR_BACKEND, '..', 'visualization-app', 'public')

ANALYSIS_DIR = os.path.join(BASE_DIR_BACKEND, '..', 'contacts-analysis')

OUTPUT_FILENAME = 'global_simu_data.czml'

# --- SIMULATION PARAMETERS ---
PAS_EN_SECONDES = 30
NOMBRE_DE_POINTS = 1000 

# --- PHYSICAL CONTACT THRESHOLD ---
DISTANCE_CONTACT_KM = 5000 # Max distance for inter-satellite contact in km

# --- COLORS ---
SATELLITES_COLOR_MAP = [
    [255, 0, 0, 255],    # Red
    [0, 255, 0, 255],    # Green
    [0, 0, 255, 255],    # Blue
    [255, 255, 0, 255],  # Yellow
    [0, 255, 255, 255],  # Cyan
    [255, 0, 255, 255],  # Magenta
    [255, 165, 0, 255]   # Orange
]

# --- RADIO CHARACTERISTICS FOR THE Thingsat Lunar IoT Constellation ---

P_TX = 14 # dBm (TX Max Power. Up to 22 dBm)
G_TX = 2 # dBi (antenna gain)
G_RX = 5 # dBi (antenna gain)

FREQ_MHZ = 868 # MHz
P_THREASHOLD = -141 # dBm (-143 dBm for Semtech LR2021)

MIN_ELEVATION = 5
