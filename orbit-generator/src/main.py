import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import spiceypy as spice
import config
from managers import satellite_manager as sat_mgr
from managers import fixe_point_manager as fp_mgr
from utils import spice_utils, czml_utils

def main():
    print("--- Start CZML Generation ---")
    
    # 1. Setup & Init
    if not os.path.exists(config.OUTPUT_DIR): os.makedirs(config.OUTPUT_DIR)
    spice_utils.load_kernels()
    db_satellites = sat_mgr.load_satellite_db(config.DB_FILE)
    
    # 2. Process Satellites - we compute there trajectory
    spk_path = os.path.join(config.KERNEL_DIR, 'SPK')
    spk_files = [f for f in os.listdir(spk_path) if f.endswith('.bsp') and f != 'de432s.bsp']
    
    czml_data, sat_list, g_time = sat_mgr.process_all_satellites(spk_files, spk_path, db_satellites)
    
    if not g_time["start"]:
        print("Error: No data processed."); return

    et_ref = spice.str2et(g_time["start"])

    # 3. Inter-Satellite Links
    czml_data += sat_mgr.handle_inter_satellite_links(sat_list, et_ref)

    # 4. Fixed Points (on the Moon) Links
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    fixe_coord_path = os.path.join(base_dir, "fixe_coord.js")
    points_of_interest = fp_mgr.load_fixed_points(fixe_coord_path)
    czml_data += fp_mgr.handle_fixed_point_links(sat_list, points_of_interest, g_time, et_ref)

    # 5. Write Output
    output_path = os.path.join(config.OUTPUT_DIR, config.OUTPUT_FILENAME)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(czml_data, f, indent=1)
    
    print(f"\n--- SUCCESS: {output_path} ---")
    spice.kclear()

if __name__ == "__main__":
    main()