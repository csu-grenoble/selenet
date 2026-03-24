# SeleNet :: Calculation Engine 

This folder contains the Python scripts and data necessary to calculate the precise positions of satellites (LRO, Clementine, Apollo) around the Moon and to generate visualization files for Cesium.

## 1. Presentation

The module uses [SPICE](https://naif.jpl.nasa.gov/naif/) through the [SpicePy](https://spiceypy.readthedocs.io/en/stable/index.html) library, a Python interface developed by NASA engineers.

**SPICE** is NASA's official library (NAIF) for space navigation.
In this project, we use it to:
* Read NASA data files (called "Kernels").
* Convert human dates into precise machine time.
* Calculate X, Y, Z coordinates of satellites second by second.

## 2. Installation (First time)

Before launching anything, you must prepare the Python environment to avoid polluting your computer.

Open a terminal at the root of the orbit-generator folder and run:

```bash
# 1. Create a virtual environment 
python3 -m venv .venv

# 2. Activate the environment
# On Linux / Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 3. Install required libraries (SPICE and Numpy)
pip install spiceypy numpy matplotlib
``` 

## 3. Launching

Once the environment is set up, you must navigate to the **src/** folder.

Run the command `python src/main.py` or `python3 src/main.py`

This command will generate the final CZML file that will be used by the visual component.

## 4. Code structure and functions

The module is structured to be modular and automated.

Here is the explanation for each folder and file:

* **kernels/**: The most important folder. It contains raw NASA data.
  * *.bsp (SPK): Position files (Trajectory of the Moon, LRO, etc.).
  * *.tls (LSK): Time file (Manages leap seconds).

* **src/**:
  * **managers/**: This folder manages entities.
  * **utils/**: This folder:
    * Centralizes utility functions for manipulating the SpiceyPy library (`spice_utils.py`) and generating CZML format packets (`czml_utils.py`).
    * Gather all algorithms for calculating communication links and the Doppler effect.
    * Integrates performance tools (`perf_utils.py`).

* **config.py**: This file centralizes the global parameters of the calculation engine, such as access paths to SPICE Kernels, simulation time steps, and physical constants for link budgets.

* **ground_objects.db.json**: This JSON file lists the geographic coordinates (latitude, longitude, altitude) of all fixed points of interest/sites on the lunar surface.

* **satellites.db.json**: This JSON file lists the technical characteristics concerning the studied satellites.

* **main.py**: This file serves as the main orchestrator of the project; it calls the various managers to perform all calculations and generate the final CZML file grouping all entities.

## 5. Algorithm and technical concepts

This section details the logic behind the orbit-generator engine. The transition from NASA data (kernels) to visualization and communication analysis relies on three pillars: reference frame management, geometric calculation, and physical signal modeling.

### 5.1 Reference Frame and coordinates

Calculating positions in space requires a definition of the coordinate system used. In this project, we used the J2000 reference frame provided by SPICE.

This reference frame is used to calculate orbital trajectories. It is a fixed frame relative to distant stars.

However, in hindsight, this reference frame is not the best option. After some research, the IAU_MOON reference frame may be a better option.

#### 5.1.1 Transformation of kernel data into X,Y,Z positions

This step is the transition point between raw binary files (.bsp) and the Cartesian coordinates usable for the simulation.

1. Call from the **process_all_satellites** function

    positions_km = spice_utils.compute_trajectory(
    id_sat, et_start, config.NUMBER_OF_STEPS, config.SECONDS_PER_STEP)

2. Calculation of positions in the **compute_trajectory** function

The spkpos function queries the kernels loaded in memory for the position vector of one object relative to another at a specific instant. It performs a mathematical interpolation defined in the NASA files (.bsp).

### 5.2 Position Calculation and Orbital Elements

For each satellite, the main.py script performs a time iteration (time step defined in config.py).

- **Time Conversion**: Transition from UTC format (ISO 8601) to SPICE time.

- **State Calculation**: Use of the spkpos function to retrieve the relative position vector.

- **CZML Generation**: The positions are stored.

### 5.3 Visibility Analysis (communication link)
#### 5.3.1 Inter-satellite communication link

The calculation of connectivity between two satellites is based on a validation of the Euclidean distance.
For each instant t of the simulation, the engine calculates the relative distance between the two entities in the **find_communication_link** function:

    v1 = sat1['positions_xyz'][t]
    v2 = sat2['positions_xyz'][t]

    d = distance_3D(v1, v2)
    visible = d <= threshold

#### 5.3.2 Satellite - fixed point communication link

In this case, the calculation is done in two validation steps

##### A. Geometric Validation (Elevation Angle)

The satellite must not only be close, it must be above the local horizon.

- **Zenith Vector**: For a fixed point (lat, lon), we calculate the vector normal to the surface using the lunar ellipsoid model via the surfnm function from the SPICE library.

- **Angle Calculation**: We calculate the vector between the fixed point and the satellite. The angle between this vector and the zenith is obtained by the vsep function from the SPICE library.

- **Condition**: The elevation is 90∘−zenith angle. The link is geometrically possible if the elevation is greater than a threshold (5∘: this threshold is currently chosen arbitrarily).

##### B. Link Budget

Next, we verify if the radio signal is physically exploitable by the receiver. To do this, we calculate the power received at the satellite level using the link budget equation:

**Calculation Component**:

- Ptx​: Transmitter power (dBm).
- Gt​ / Gr​: Respective gains of the transmitting and receiving antennas (dB).
- FSPL: Free Space Path Loss.

The variable FSPL represents the signal weakening related to distance. It is obtained using the following simplified formula:

    FSPL = 20log10​(d)+20log10​(f)−147.55

- d: Distance between the two entities (meters).
- f: Working frequency (Hertz).
- -147.55: Calculation constant including the speed of light.

**Model Parameter**:

In this first version of the project, physical constants (power, gains, frequencies) are centralized in the config.py file. These values were defined in consultation with the project owners to correspond to the actual technical specifications of the onboard equipment.

The link is only considered "active" if Prx​ is greater than the receiver sensitivity threshold, which is -140 dB (value chosen after consultation with the project owners).

### 5.4 Frequency shift - Doppler Effect

When a communication link is detected between a satellite and a fixed point on the ground, we calculate the frequency shift and generate the corresponding graph.

Calculations are implemented in the **doppler_utils.py** file in the **doppler_shifts** function.

#### 5.4.1 Calculation of relative radial velocity

To calculate the Doppler, we are not interested in the absolute speed of the satellites, but only in their radial velocity (the speed at which they approach or move away from a point).

The engine uses the state vectors provided by SPICE (which contain position and velocity [P,V]) to perform this calculation:

#### 5.4.2 Calculation of frequency shift

The Doppler shift delta_f is calculated according to the formula:

    Δf= v_r / c_light ​​⋅f0​

where:
- v_r​: Radial velocity (m/s).
- c_light: Speed of light (≈299792458 m/s).
- f0: Nominal carrier frequency (Hz) defined in config.py (FREQ_MHZ).

## References
* SPICE : An Observation Geometry System for Space Science Missions https://naif.jpl.nasa.gov/naif/
  * https://naif.jpl.nasa.gov/naif/tutorials.html
  * https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/
* Annex et al., (2020). SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit. Journal of Open Source Software, 5(46), 2050, https://doi.org/10.21105/joss.02050
* SpicePy documentation https://spiceypy.readthedocs.io/en/stable/index.html
