#
# SeleNet
#
# Authors : Nada Yassine, Meli Scott Douanla 
#

import spiceypy as spice
import os
import numpy as np
import config
import math
import numpy as np


def calculate_FSPL(dist_km, freq_hz) : 
    """
    Compute the Free Space Path Loss in dB for a given distance and frequency
    """
    return 20 * np.log10(dist_km*1000) + 20 * np.log10(freq_hz) - 147.55

def calculate_received_power(distance_km) : 
    """
    Compute the received power at the receiver in dB
    """
    freq_hz = config.FREQ_MHZ * 1000000
    fspl = calculate_FSPL(distance_km,freq_hz)

    p_rx = config.P_TX + config.G_TX + config.G_RX - fspl

    return p_rx

def is_link_valid(elevation, p_rx) : 
    """
    Determine if the communication link is valid based on elevation and received power
    """
    return elevation > 0 and elevation >= config.MIN_ELEVATION and p_rx >= config.P_THREASHOLD 

