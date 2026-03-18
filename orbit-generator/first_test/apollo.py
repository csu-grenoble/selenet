import spiceypy as spice
import json 
import numpy as np
import os

# --- 1. KERNEL LOADING ---
spice.furnsh('../kernels/LSK/naif0012.tls')
spice.furnsh('../kernels/SPK/de432s.bsp')
spice.furnsh('../kernels/SPK/a16_subsat_ssd_lp150q.bsp') 

# --- 2. BOUCLE CONFIGURATION ---
pas_en_secondes = 60
nombre_de_points = 1000 

# --- 3. APOLLO 16 SETUP (detection of the ID and dates) ---
ids = spice.stypes.SPICEINT_CELL(100)
spice.spkobj('../kernels/SPK/a16_subsat_ssd_lp150q.bsp', ids)
id_apollo = ids[0]

# Get start/end dates from the file
cover = spice.stypes.SPICEDOUBLE_CELL(2000)
spice.spkcov('../kernels/SPK/a16_subsat_ssd_lp150q.bsp', id_apollo, cover)
apollo_et_debut, apollo_et_fin = spice.wnfetd(cover, 0)

# We define the availability interval for the CZML header
# CZML requires ISO 8601 format (e.g., 2012-03-15T10:00:00Z)
iso_start = spice.timout(apollo_et_debut, "YYYY-MM-DDTHR:MN:SC.###Z")
# We calculate the end based on the number of points we simulate
et_final_simu = apollo_et_debut + (nombre_de_points * pas_en_secondes)
iso_end = spice.timout(et_final_simu, "YYYY-MM-DDTHR:MN:SC.###Z")

print(f"--- Calculating Trajectory for APOLLO ---")
print(f"Start: {iso_start}")
print(f"End:   {iso_end}")

# --- 4. CALCULATION LOOP ---
czml_positions = []

for i in range(nombre_de_points):
    temps_ecoule = i * pas_en_secondes
    et_actuel = apollo_et_debut + temps_ecoule
    
    try:
        # Calculate position relative to MOON in J2000 frame (Inertial)
        pos, _ = spice.spkpos(str(id_apollo), et_actuel, 'J2000', 'NONE', 'MOON')
        
        x = pos[0] * 1000 # Convert km to meters for Cesium
        y = pos[1] * 1000
        z = pos[2] * 1000
        
        czml_positions.extend([temps_ecoule, x, y, z])

    except spice.stypes.SpiceyError:
        pass

# --- 5. GENERATE CZML FILE ---

# Packet 1: The Document Header (Clock and Time)
document_packet = {
    "id": "document",
    "name": "Apollo_Mission",
    "version": "1.0",
    "clock": {
        "interval": f"{iso_start}/{iso_end}",
        "currentTime": iso_start,
        "multiplier": 300, # Speed of animation
        "range": "LOOP_STOP",
        "step": "SYSTEM_CLOCK_MULTIPLIER"
    }
}

# Packet 2: The Satellite Data
satellite_packet = {
    "id": "Apollo_Sat",
    "name": "Apollo",
    "description": "Trajectory of the Apollo mission around the Moon.",
    "availability": f"{iso_start}/{iso_end}",
    "billboard": {
        "show": True,
        "pixelSize": 10,
        "color": {"rgba": [255, 0, 0, 255]}, # Rouge
        "eyeOffset": {"cartesian": [0, 0, 0]}
    },
    "label": {
        "text": "Apollo",
        "show": True,
        "font": "12pt Lucida Console",
        "horizontalOrigin": "LEFT",
        "pixelOffset": {"cartesian2": [12, 0]},
        "fillColor": {"rgba": [255, 0, 0, 255]},
        "outlineColor": {"rgba": [255, 0, 0, 255]},
        "outlineWidth": 2,
        "style": "FILL_AND_OUTLINE"
    },
    "path": {
        "show": True,
        "width": 1,
        "material": {
            "solidColor": {
                "color": {"rgba": [255, 0, 0, 255]}
            }
        },
        "leadTime": 0,
        "trailTime": 100000 # Shows the path behind the satellite
    },
    "position": {
        "epoch": iso_start, # The t=0 reference
        "referenceFrame": "INERTIAL",
        "cartesian": czml_positions,
        "interpolationAlgorithm": "LAGRANGE",
        "interpolationDegree": 5
    }
}

# Write to JSON file
output_filename = "apollo.czml"
dossier_cible = "CZML"
if not os.path.exists(dossier_cible):
    os.makedirs(dossier_cible)

chemin_complet = os.path.join(dossier_cible, output_filename)

with open(chemin_complet, 'w') as f:
    json.dump([document_packet, satellite_packet], f)

print(f"--- SUCCESS ---")
print(f"File generated: {chemin_complet}")
print(f"Number of position values: {len(czml_positions)}")

spice.kclear()