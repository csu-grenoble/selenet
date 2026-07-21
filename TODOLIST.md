# ToDoList 🚧


## Databases

* [ ] add sensors list for each site
  * A. Torrent Duch et al., The Moon's crust and upper mantle discontinuities revealed by seismic interferometry methods applied to Apollo seismic data, Journal of Geophysical Research: Planets, 130, e2025JE009090, (2025), https://doi.org/10.1029/2025JE009090
* [ ] add more [landing sites](https://en.wikipedia.org/wiki/Moon_landing) into the [database](orbit-generator/ground_objects.db.json).
  * [x] add [Blue Ghost Mission 1](https://fireflyspace.com/missions/blue-ghost-mission-1/)
  * [x] add [Apollo S16](https://en.wikipedia.org/wiki/Apollo_16) to [database](orbit-generator/ground_objects.db.json)
  * [ ] add impact of [SpaceX Falcon 9 (NORAD 62719)](https://www.n2yo.com/satellite/?s=62719) (5 August 2026 near Einstein Crater ?)
  * [ ] add Centaur rocket impact
  * [ ] add LCROSS https://en.wikipedia.org/wiki/LCROSS
* [ ] add more orbiters into the [database](orbit-generator/satellites.db.json)
  * [ ] add https://en.wikipedia.org/wiki/Chandrayaan-1

## Kernels

* [ ] add ref to the origin of tke kernel files
  * [ ] https://www.researchgate.net/publication/268579859_NASA_GSFC_lunar_reconnaissance_orbiter_LRO_orbit_estimation_and_prediction


## Orbit generation

* [ ] lint source code
* [ ] WIP : translate variables and constants names in english
* [ ] WIP : translate comments in english 
* [ ] add more infos to vizualising into [ground_object.db.json](orbit-generator/ground_objects.db.json)
* [ ] add more infos to vizualising into [satellites.db.json](orbit-generator/satellites.db.json)
* [ ] add dopler graphes for sat to sat links

## Vizualisation

* [ ] lint source code
* [ ] show dopler graphes for sat to sat links
* [ ] improve the labels of satellites and ground endpoints/sites
* [ ] translate comments in english 
* [ ] add more info related to objets (speed, min max dopler, altitude, FSPL, link margin @ SF12)
* [ ] add `i18n` for `fr`
* [ ] fix starttime at now (not 1994)
* [ ] add Earth in viz
* [x] (object_info.js) round speed
* [ ] (object_info.js) : change -30 and 30 by the value used for the generation
* [ ] control on camera for showing Sun
* [ ] control on camera for showing Earth
* [ ] control on camera for showing Mars
* [ ] web responsive : resize the viewer when full screen and higher screen
* [ ] better position for object info panel  
* [ ] complete the credits for assets

## Mars

* [ ] version for Mars with SPICE with [Asset #3644333](https://ion.cesium.com/assetdepot/3644333?query=mars)


## Notes

### Cesium for Earth
```js
Cesium.Ellipsoid.default = Cesium.Ellipsoid.WGS84;

// Set the  asset 
const Cesium_IonAssetId = 2275207; // Earth
```

### Cesium for Mars

```js
Cesium.Ellipsoid.default = Cesium.Ellipsoid.MARS;

// Set the  asset 
const Cesium_IonAssetId = 3644333; // Mars
```
