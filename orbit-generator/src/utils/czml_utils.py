#
# SeleNet
#
# Authors : Nada Yassine, Meli Scott Douanla 
#

import json

def generate_header_czml(iso_start, iso_end):
    """
    Create the CZML document header packet.

    Defines the global simulation clock, time interval,
    and animation playback parameters.
    """    
    return {
        "id": "document",
        "name": "Global_Simulation",
        "version": "1.0",
        "clock": {
            "interval": f"{iso_start}/{iso_end}",
            "currentTime": iso_start,
            "multiplier": 300, # Speed of animation
            "range": "LOOP_STOP",
            "step": "SYSTEM_CLOCK_MULTIPLIER"
        }
    }

def generate_html_description(info):
    """
    Generate a dynamic HTML block from all keys present in the 'info' dictionary.
    """    
    description_text = info.get('description', 'Pas de description.')

    exclude_keys = ['description', 'display_name', 'id']

    table_rows = ""
    for key, value in info.items():
        if key not in exclude_keys:
            label = key.replace('_', ' ').capitalize()
            
            table_rows += f"""
            <tr style="border-bottom: 1px solid #555;">
                <td style="padding: 5px; color: #aaa;">{label}</td>
                <td style="padding: 5px; text-align: right;">{value}</td>
            </tr>
            """

    return f"""
    <div class="cesium-info-box-description">
        <p>{description_text}</p>
        <table style="width:100%; border-collapse: collapse; font-size:12px;">
            {table_rows}
        </table>
    </div>
    """

def generate_satellite_packet(id_sat, iso_start, iso_end, name, description, positions, color_rgba):
    """
    Create a CZML packet describing a satellite.

    Includes billboard appearance, trajectory path,
    time availability, and interpolated position data.
    """    
    return {
        "id": f"Sat_{id_sat}",
        "name": name,
        "description": description,
        "availability": f"{iso_start}/{iso_end}",
        "billboard": {
            "show": True,
            "pixelSize": 12,
            "color": {"rgba": color_rgba},
            "eyeOffset": {"cartesian": [0, 0, 0]}, 
            "horizontalOrigin":"CENTER",
            "image":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
            "pixelOffset":{
                "cartesian2":[
                0,0
                ]
            }
        },
        "path": {
            "show": True,
            "width": 1,
            "material": {"solidColor": {"color": {"rgba": color_rgba}}},
            "leadTime": 0,
            "trailTime": 100000
        },
        "position": {
            "epoch": iso_start,
            "referenceFrame": "INERTIAL",
            "cartesian": positions,
            "interpolationAlgorithm": "LAGRANGE",
            "interpolationDegree": 5
        }
    }

def generate_fixed_station_packet(station_id, name, lon, lat, iso_start, iso_end ):
    """
    Create a CZML packet representing a fixed ground station or a sensor.

    The station is clamped to the surface and displayed
    with a label and a point marker.
    """ 
    return {
        "id": f"Gnd_{station_id}",
        "name": name,
        "availability": "0000-01-01T00:00:00Z/9999-12-31T23:59:59Z",
        "label": {
            "text": name,
            "font": "10pt monospace",
            "style": "FILL_AND_OUTLINE",
            "outlineWidth": 2,
            "verticalOrigin": "BOTTOM",
            "pixelOffset": {"cartesian2": [0, 15]},
            "heightReference": "CLAMP_TO_GROUND"
        },
        "point": {
            "show": True,
            "pixelSize": 8,
            "color": {"rgba": [0, 255, 255, 255]}, 
            "outlineColor": {"rgba": [0, 0, 0, 255]}, # Petit contour noir
            "outlineWidth": 1,
            "heightReference": "CLAMP_TO_GROUND"
        },
        "position": {
            "cartographicDegrees": [lon, lat, 0.0]
        }
    }

def generate_SatToSat_link_packet(sat1, sat2, intervals):
    """
    Create a CZML polyline packet representing
    a dynamic link between two satellites.

    Visibility is controlled by time intervals.
    """    
    return {
        "id": f"Link_Satellite/{sat1}-to-Satllite/{sat2}",
        "name": f"Link Sat{sat1} - Sat{sat2}",
        "polyline": {
            "show": intervals, 
            "width": 2,
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [0, 255, 255, 255]
                    }
                }
            },
            "arcType": "NONE", 
            "positions": {
                "references": [f"Sat_{sat1}#position", f"Sat_{sat2}#position"]            }
        }
    }


def generate_PointToSat_link_packet(sat_id, point_id, intervals, description_intervals):
    """
    Create a CZML polyline packet representing
    a link between a satellite and a fixed point.

    Visibility is controlled by time intervals.
    """
    return {
        "id": f"Link_{sat_id}_to_{point_id}",
        "name": f"Link Sat{sat_id} - {point_id}",
        "description": description_intervals,
        "polyline": {
            "show": intervals, 
            "width": 2,
            "material": {
                "solidColor": {
                    "color": {
                        "rgba": [255, 0, 255, 255]
                    }
                }
            },
            "arcType": "NONE", 
            "positions": {
                "references": [f"Sat_{sat_id}#position", f"Gnd_{point_id}#position"]
            }
        }
    }
