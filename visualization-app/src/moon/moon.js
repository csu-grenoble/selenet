
import * as Cesium from "cesium";
//import Sandcastle from "Sandcastle";
import "../css/panel.css"
import "../css/time.css"
//import "../css/bucket.css"
import { handle_panel } from "./panel";
import { updateClocks } from "./time";
console.log(window.CESIUM_BASE_URL);

// Set the ellipsoid to be the moon before creating the viewer
Cesium.Ellipsoid.default = Cesium.Ellipsoid.MOON;

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


// Mise à jour à chaque frame
viewer.clock.onTick.addEventListener(() => {updateClocks(viewer)});
viewer.clock.onTick.addEventListener(() => {handle_panel(dataSource);})

