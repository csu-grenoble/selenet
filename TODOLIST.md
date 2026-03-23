# ToDoList 🚧


## Databases

* [ ] add sensors list for each site
* [x] add [Apollo S16](https://en.wikipedia.org/wiki/Apollo_16) to [ground_object.db.json](orbit-generator/ground_objects.db.json)
  * A. Torrent Duch et al., The Moon's crust and upper mantle discontinuities revealed by seismic interferometry methods applied to Apollo seismic data, Journal of Geophysical Research: Planets, 130, e2025JE009090, (2025), https://doi.org/10.1029/2025JE009090


## Orbit generation

* [ ] WIP : translate variables and constants names in english
* [ ] WIP : translate comments in english 
* [ ] add more infos to vizualising into [ground_object.db.json](orbit-generator/ground_objects.db.json)
* [ ] add more infos to vizualising into [satellites.db.json](orbit-generator/satellites.db.json)

## Vizualisation

* [ ] lint source code
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
