import spiceypy as spice
import os
import numpy as np
import config
import math
import matplotlib.pyplot as plt
from utils import radio_utils
from utils.perf_utils import monitor_perf


def load_kernels():
    """
    Load all required SPICE kernels (leap seconds, planetary ephemeris,
    and generic constants) from the configured kernel directory.
    """    
    try:
        # Load Leap Second Kernel
        lsk_path = os.path.join(config.KERNEL_DIR, 'LSK', 'naif0012.tls')
        if os.path.exists(lsk_path):
            spice.furnsh(lsk_path)
        else:
            print(f"Error: LSK not found at {lsk_path}")

        # Load Planetary Ephemeris (Planets & Moon)
        spk_path = os.path.join(config.KERNEL_DIR, 'SPK', 'de432s.bsp')
        if os.path.exists(spk_path):
            spice.furnsh(spk_path)
            print("Kernels de base chargés.")
        else:
            print(f"Error: SPK not found at {spk_path}")

        # Load GENERIC kernel
        generic_path = os.path.join(config.KERNEL_DIR, 'GENERIC', 'pck00010.tpc')
        if os.path.exists(generic_path):
            spice.furnsh(generic_path)
        else:
            print(f"Error: GENERIC file not found at {generic_path}")
            
    except Exception as e:
        print(f"Erreur chargement kernels de base : {e}")


def get_satellite_info(bsp_path):
    """
    Extract the satellite ID and time coverage from a BSP file.

    Returns:
        (id_sat, et_start, et_end) or (None, None, None) if unavailable.
    """
    try:
        ids = spice.stypes.SPICEINT_CELL(100)
        spice.spkobj(bsp_path, ids)
        
        if len(ids) == 0:
            return None, None, None
        
        id_sat = ids[0]
        cover = spice.stypes.SPICEDOUBLE_CELL(2000)
        spice.spkcov(bsp_path, id_sat, cover)
        
        if spice.wncard(cover) == 0:
            return None, None, None
            
        # wnfetd returns (start, end)
        start, end = spice.wnfetd(cover, 0)
        return id_sat, start, end
    except Exception as e:
        print(f"Error getting info for {bsp_path}: {e}")
        return None, None, None


def compute_trajectory(id_sat, et_start, nb_points, step):
    """
    Compute the satellite trajectory over time relative to the Moon.

    Returns a flat list of time-offset positions:
    [elapsed, x, y, z, elapsed, x, y, z, ...]
    Coordinates are converted from km to meters for Cesium.
    """
    positions = []
    
    for i in range(nb_points):
        elapsed = i * step
        et_current = et_start + elapsed
        try:
            pos, _ = spice.spkpos(str(id_sat), et_current, 'J2000', 'NONE', 'MOON')
            
            x, y, z = pos[0], pos[1], pos[2]

            positions.extend([elapsed, x, y, z])
        except:
            pass 
            
    return positions


def get_iso_date(et_time):
    """
    Convert a SPICE ephemeris time (ET) to an ISO 8601 string.
    """    
    return spice.timout(et_time, "YYYY-MM-DDTHR:MN:SC.###Z")


def distance_3D(p1, p2): 
    """
    Compute the Euclidean 3D distance between two position vectors.
    """    
    return math.sqrt((p2[1] - p1[1])**2 +
                     (p2[2] - p1[2])**2 +
                     (p2[3] - p1[3])**2)


def find_communication_links(satellites_data):
    """
    Determine communication links between satellites based only on distance.

    For each time step, two satellites are considered in contact
    if their separation is below a configurable threshold.
    """
    threshold = config.DISTANCE_CONTACT_KM
    nb_steps = len(satellites_data[0]['positions_xyz'])

    satellite_links = []

    for i in range(len(satellites_data)):
        sat1 = satellites_data[i]

        for j in range(i + 1, len(satellites_data)):
            sat2 = satellites_data[j]

            links = []

            for t in range(nb_steps):
                v1 = sat1['positions_xyz'][t]
                v2 = sat2['positions_xyz'][t]

                d = distance_3D(v1, v2)
                visible = d <= threshold

                links.append({
                    'time': v1[0],  # elapsed time
                    'v1': v1,
                    'v2': v2,
                    'distance': d,
                    'visible': visible
                })

            if links:
                satellite_links.append({
                    'sat1': sat1['id'],
                    'sat2': sat2['id'],
                    'links': links
                })

    return satellite_links


def sphere_blocks_link(v1, v2, sphere_center, sphere_radius):
    """
    Check whether a sphere (the Moon) blocks the line of sight
    between two satellites.

    Returns True if the segment intersects the sphere.
    """

    # Convert and extract directly into numpy arrays 
    p1 = np.array(v1[1:4])
    p2 = np.array(v2[1:4])
    center = np.array(sphere_center)

    # Direct vector of the segment and vector to the center
    segment_vec = p2 - p1        
    p1_to_center = center - p1   

    # Length of the segment squared
    len_sq = np.dot(segment_vec, segment_vec)

    # Case where p1 and p2 are the same point
    if len_sq == 0:
        return False

    # Orthogonal projection onto the line defined by the segment
    t = np.dot(p1_to_center, segment_vec) / len_sq

    # Constraint t to the [0,1]  
    t = np.clip(t, 0.0, 1.0)

    # Compute the closest point on the segment
    closest_point = p1 + (segment_vec * t)

    # Compute the Euclidean distance to the center
    dist = np.linalg.norm(closest_point - center)

    return dist < sphere_radius


def display_which_links(satellite_links, moon_center, moon_radius):
    """
    Determine which communication links are actually visible,
    accounting for Moon obstruction.

    Returns visibility status for each time step. Format : 
    [
        {'sat1': id1, 'sat2': id2,
            'times': [
            {'time': t1, 'bool': True/False},
            ...]
        },
    ...]
    """
    visible_links = []

    for link in satellite_links:
        sat1 = link['sat1']
        sat2 = link['sat2']

        valid_times = []

        for step in link['links']:

            if not step['visible']:
                valid_times.append({
                    'time': step['time'],
                    'bool': False,
                })
                continue

            if not sphere_blocks_link(
                step['v1'],
                step['v2'],
                moon_center,
                moon_radius
            ):
                valid_times.append({
                    'time': step['time'],
                    'bool': True,
                })
            else : 
                valid_times.append({
                    'time': step['time'],
                    'bool': False,
                })

        if valid_times:
            visible_links.append({
                'sat1': sat1,
                'sat2': sat2,
                'times': valid_times
            })

    return visible_links


def convert_intervals_to_real_time(intervals, et_ref):
    """
    Convert relative time intervals into absolute ISO 8601 intervals
    suitable for CZML visualization.
    """
    czml_intervals = []
    
    for interval in intervals:
        # Compute absolute start time
        et_start = et_ref + interval['start']
        iso_start = spice.timout(et_start, "YYYY-MM-DDTHR:MN:SC.###Z")

        # Handle end of interval
        if interval['end'] is not None:
            et_end = et_ref + interval['end']
            iso_end = spice.timout(et_end, "YYYY-MM-DDTHR:MN:SC.###Z")
        else:
             iso_end = "9999-12-31T23:59:59Z" # Default "infinite" value if not closed

        czml_intervals.append({
            "interval": f"{iso_start}/{iso_end}",
            "boolean": interval['show']
        })
        
    return czml_intervals


def latlon_to_unit(lat, lon):
    """
    Convert latitude/longitude into a 3D unit vector.
    """
    lat = np.radians(lat)
    lon = np.radians(lon)
    return np.array([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat)
    ])


def get_fixe_point_details(lon, lat, body_name='MOON') : 
    """
    Compute XYZ position and the zenoth vector of a point on the ground
    """
    _, radii = spice.bodvrd(body_name, 'RADII', 3)
    re, rp = radii[0], radii[2]
    f = (re - rp) / re 

    point_pos = spice.georec(np.radians(lon), np.radians(lat), 0, re, f)

    zenith_vec = spice.surfnm(radii[0], radii[1], radii[2], point_pos)

    return point_pos, zenith_vec

def calculate_elevation_angle(sat_pos, point_pos, zenith_vec) : 
    """
    Calculate the elevation of the satellite above the site's horizon (in degrees)
    """
    dir_vec = spice.vsub(sat_pos, point_pos)

    zenith_angle = spice.vsep(zenith_vec, dir_vec)

    elevation = 90.0 - np.degrees(zenith_angle)

    return elevation
    
@monitor_perf
def compute_moon_fp_sat_links(satellites_data, points_of_interest):
    """
    Determine visibility between satellites and fixed lunar points
    thanks to elevation angle and radio link budget.
    """

    # Pre-calculate XYZ positions and Zenith vectors for each point of interest
    poi_data = {}
    for poi in points_of_interest:
        pos, zenith = get_fixe_point_details(
            poi["longitude"], 
            poi["latitude"], 
            'MOON'
        )
        poi_data[poi["text"]] = {
            "pos": pos,
            "zenith": zenith
        }

    results = []

    for sat in satellites_data:
        sat_id = str(sat.get('id', ''))
        t_start_sat = sat.get('et_sat_start')

        for poi_name, data in poi_data.items():
            time_series = []
            site_pos = data["pos"]
            zenith_vec = data["zenith"]

            for entry in sat['positions_xyz']:
                t, x, y, z = entry
                sat_pos = np.array([x, y, z])

                # Elevation relative to the local horizon
                elevation = calculate_elevation_angle(
                    sat_pos, site_pos, zenith_vec
                )

                distance_km = np.linalg.norm(sat_pos - site_pos)
                
                # Received power (P_rx)
                p_rx = radio_utils.calculate_received_power(distance_km)

                # --- DOUBLE VALIDATION ---
                # The link is active if the satellite is "above" AND the signal is strong enough
                visible = radio_utils.is_link_valid(elevation, p_rx)

                time_series.append({
                    'time': t,
                    'bool': bool(visible), 
                    'pos': sat_pos, 
                    'dist': distance_km
                })

            results.append({
                'sat_id': sat_id,
                'point': poi_name,
                'times': time_series, 
                'et_sat_start': t_start_sat
            })

    return results