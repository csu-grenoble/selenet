import spiceypy as spice
import os
import numpy as np
import config
import math
import matplotlib.pyplot as plt
from utils import spice_utils
from utils.perf_utils import monitor_perf


def generate_doppler_graph(times, doppler_shifts, sat_id, label): 
    """
    Generate and save a Doppler shift graph
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "..", "visualization-app", "public"))
    
    output_rel_dir = os.path.join("assets", "doppler_graphs", str(sat_id).strip())
    full_output_dir = os.path.join(public_dir, output_rel_dir)
    
    os.makedirs(full_output_dir, exist_ok=True)

    t_min = np.array(times) / 60.0 

    df_khz = np.array(doppler_shifts) / 1000

    plt.figure(figsize=(6, 4))
    plt.plot(t_min, df_khz, color='#1f77b4', linewidth=2, label='Doppler Shift')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)

    plt.title(f"Doppler : Satellite {sat_id}\nStation : {label}", fontsize=12, pad=15)
    plt.xlabel("Time since the start of the simulation (min)", fontsize=10)
    plt.ylabel("Frequency shift (kHz)", fontsize=10)
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')

    clean_label = label.replace(" ","_")
    filename = f"doppler_{sat_id}_{clean_label}.png"
    
    full_filepath = os.path.join(full_output_dir, filename)
    
    # plt.savefig(full_filepath, dpi=150, bbox_inches='tight')
    plt.savefig(full_filepath, dpi=100, bbox_inches='tight')
    plt.close()

    web_path = f"/{output_rel_dir}/{filename}".replace("\\", "/")
    return web_path

def doppler_shifts(intervals, times, sat_id, point_name, et_ref): 
    """
    Compute Doppler shifts when a communication link is established and generate graphs for each interval.
    """
    description_intervals = []
    f0 = config.FREQ_MHZ * 1e6
    c_light = 299792.458
    
    for i, interval in enumerate(intervals): 
        iso_time = spice_utils.convert_intervals_to_real_time([interval], et_ref)[0]['interval']

        if interval['show']:
            safe_end = interval['end'] if interval['end'] is not None else times[-1]['time']

            plot_times = []
            plot_doppler = []

            pts = [p for p in times if interval['start'] <= p['time'] <= safe_end]

            for j in range(len(pts) - 1): 
                p1 = pts[j]
                p2 = pts[j+1]
                dt = p2['time'] - p1['time']
                if dt <= 0: continue
                v_radial = (p2['dist'] - p1['dist']) / dt
                shift = -f0 * (v_radial / c_light)
                plot_times.append(p1['time'])
                plot_doppler.append(shift)

            if len(plot_times) > 1: 
                img_path = generate_doppler_graph(plot_times, plot_doppler, sat_id, f"{point_name}_pass_{i}")
                
                description_intervals.append({
                    "interval": iso_time,
                    "string": f"<h3>Doppler - {point_name}</h3><img src='{img_path}' style='width:100%; height:auto;'/>"
                })
            else:
                description_intervals.append({"interval": iso_time, "string": "<h3>Insufficient data</h3>"})
        else:
            description_intervals.append({"interval": iso_time, "string": "<h3>No communication link established</h3>"})
    
    return description_intervals
