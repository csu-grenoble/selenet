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
from utils import spice_utils, czml_utils, doppler_utils
from .satellite_manager import compute_intervals
from utils.perf_utils import monitor_perf


def load_fixed_points(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().replace("export default", "").strip().rstrip(";")
            return json.loads(content)
    except Exception as e:
        print(f"Error loading fixed points: {e}")
        return []

@monitor_perf
def handle_fixed_point_links(satellites_data, points_of_interest, global_time, et_ref):
    czml_packets = []
    
    # Generate station markers
    for pt in points_of_interest:
        czml_packets.append(czml_utils.generate_fixed_station_packet(
            pt["text"], pt["text"], pt["longitude"], pt["latitude"], 
            global_time["start"], global_time["end"]))

    # Compute links
    moon_links = spice_utils.compute_moon_fp_sat_links(satellites_data, points_of_interest)

    # Save the moon links in a json file for outside analysis
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return super().default(obj)
    
    output_path = os.path.join(config.ANALYSIS_DIR, "moon_links.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(moon_links, f, indent=1, cls=NumpyEncoder)
    
    # For each link, we compute visibility intervals and Doppler shift graphs
    for link in moon_links:
        sat_id = link['sat_id']

        intervals = compute_intervals(link['times'])
        real_time_intervals = spice_utils.convert_intervals_to_real_time(intervals, et_ref)
        description_intervals = doppler_utils.doppler_shifts(intervals, link['times'],sat_id, link['point'], et_ref)

        czml_packets.append(czml_utils.generate_PointToSat_link_packet(
            sat_id, link['point'], real_time_intervals, description_intervals))
            
    return czml_packets