# ToDoList 🚧

* [ ] lint source code
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
