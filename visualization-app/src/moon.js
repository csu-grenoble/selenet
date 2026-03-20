/*
 * SeleNet
 * 
 * Authors : Nada Yassine, Meli Scott Douanla 
 */

import * as Cesium from "cesium";
//import Sandcastle from "Sandcastle";
import "./css/panel.css"
import "./css/time.css"
import "./css/info.css"
//import "../css/bucket.css"
import { handle_panel,create_panel } from "./panel";
import { updateClocks } from "./time";
import { display_details } from "./object_info";
console.log(window.CESIUM_BASE_URL);

Cesium.Ion.defaultAccessToken = process.env.API_URL



// Set the ellipsoid to be the moon before creating the viewer
Cesium.Ellipsoid.default = Cesium.Ellipsoid.MOON;


Cesium.Ion.defaultAccessToken = process.env.API_URL
const viewer = new Cesium.Viewer("cesiumContainer", {
  terrainProvider: false,
  baseLayer: false,
  timeline: true,
  animation: true,
  baseLayerPicker: false,
  geocoder: false,
  shadows: true,
  shouldAnimate: true,
  ellipsoid: Cesium.Ellipsoid.MOON
});

const scene = viewer.scene;

// Add Moon Terrain 3D Tiles
try {
  const tileset1 = await Cesium.Cesium3DTileset.fromIonAssetId(2684829, {
    // Allow clamp to 3D Tiles
    enableCollision: true,
  });
  viewer.scene.primitives.add(tileset1);
} catch (error) {
  console.log(`Error loading tileset: ${error}`);
}

const dataSource = await Cesium.CzmlDataSource.load("/global_simu_data.czml")
viewer.dataSources.add(dataSource);


const panel = document.getElementById("sidePanel");
const toggleBtn = document.getElementById("panelToggle");

toggleBtn.onclick = () => {
  panel.classList.toggle("closed");
  // toggleBtn.textContent = toggleBtn.textContent=="▶" ? "◀": "▶";
  
};

const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);

handler.setInputAction(function(click) {
    const pickedObject = viewer.scene.pick(click.position);

    if (Cesium.defined(pickedObject) && pickedObject.id) {
        const entity = pickedObject.id;
        console.log("Entity clicked:", entity.id);
        display_details(viewer,dataSource,entity.id)
    }

}, Cesium.ScreenSpaceEventType.LEFT_CLICK);

create_panel(dataSource)

// Mise à jour à chaque frame
viewer.clock.onTick.addEventListener(() => {updateClocks(viewer)});
viewer.clock.onTick.addEventListener(() => {handle_panel(dataSource);})

