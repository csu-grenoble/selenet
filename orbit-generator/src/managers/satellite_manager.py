#
# SeleNet
#
# Authors : Nada Yassine, Meli Scott Douanla 
#

import numpy as np
import json
import os
import spiceypy as spice
import config  
from utils import spice_utils, czml_utils 
from utils.perf_utils import monitor_perf

def load_satellite_db(db_file) : 
    if os.path.exists(config.SATELLITES_DB_FILE): 
        with open(config.SATELLITES_DB_FILE, 'r', encoding='utf-8') as f : 
            return json.load(f)

    print(f"Warning: DB file not found at {config.SATELLITES_DB_FILE}")
    return {}

@monitor_perf
def process_all_satellites(spk_files, spk_path, db_satellites):
    czml_data = []
    satellites_data = []
    global_time = {"start": None, "end": None}

    for index, file in enumerate(spk_files):
        full_path = os.path.join(spk_path, file)
        spice.furnsh(full_path)
        try:
            id_sat, et_start, et_end = spice_utils.get_satellite_info(full_path)
            if id_sat is None: continue

            # Sync Time & Header
            if global_time["start"] is None:
                global_time["start"] = spice_utils.get_iso_date(et_start)
                duration = config.NOMBRE_DE_POINTS * config.PAS_EN_SECONDES
                global_time["end"] = spice_utils.get_iso_date(et_start + duration)
                czml_data.append(czml_utils.generate_header_czml(global_time["start"], global_time["end"]))

            # Trajectory
            positions_km = spice_utils.compute_trajectory(
                id_sat, et_start, config.NOMBRE_DE_POINTS, config.PAS_EN_SECONDES
            )
            if not positions_km: 
                continue

            # 3. Préparation des données pour l'AFFICHAGE Cesium (Mètres)
            # Cesium interprète les coordonnées cartésiennes en mètres
            positions_meters = []
            for i in range(0, len(positions_km), 4):
                t = positions_km[i]
                x_m = positions_km[i+1] * 1000
                y_m = positions_km[i+2] * 1000
                z_m = positions_km[i+3] * 1000
                positions_meters.extend([t, x_m, y_m, z_m])


            # Metadata & Packet
            info_db = db_satellites.get(file, {})
            #sat_name = info_db.get('nom_affichage', f"Obj {id_sat}")
            sat_name = info_db.get('nom_affichage', f"Sat{id_sat}")

            desc_html = czml_utils.generate_html_description(info_db)
            color = config.SATELLITES_COLOR_MAP[index % len(config.SATELLITES_COLOR_MAP)]
            
            czml_data.append(czml_utils.generate_satellite_packet(
                id_sat, global_time["start"], global_time["end"], sat_name, desc_html, positions_meters, color))

            # Store for link communication
            vectors = [positions_km[i:i+4] for i in range(0, len(positions_km), 4)]
            satellites_data.append({'id': id_sat, 'et_global_start': spice.str2et(global_time["start"]),'et_sat_start': et_start, 'et_sat_end': et_end, 'positions_xyz': vectors})
        finally:
            spice.unload(full_path)
            
    return czml_data, satellites_data, global_time

@monitor_perf
def handle_inter_satellite_links(satellites_data, et_ref):
    links_packets = []
    first_pass = spice_utils.find_communication_links(satellites_data)
    
    _, moon_radii = spice.bodvrd('MOON', 'RADII', 3)
    display_links = spice_utils.display_which_links(first_pass, [0,0,0], moon_radii[0])
    
    for link in display_links:
        intervals = compute_intervals(link['times'])
        real_time = spice_utils.convert_intervals_to_real_time(intervals, et_ref)
        links_packets.append(czml_utils.generate_SatToSat_link_packet(link['sat1'], link['sat2'], real_time))
        
    return links_packets

def compute_intervals(times):
    if not times: return []
    intervals = []
    current = {'show': times[0]['bool'], 'start': times[0]['time'], 'end': None}
    for t in times[1:]:
        if t['bool'] != current['show']:
            current['end'] = t['time']
            intervals.append(current)
            current = {'show': t['bool'], 'start': t['time'], 'end': None}
    intervals.append(current)
    return intervals