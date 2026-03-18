
//import * as Cesium from "cesium";
//import Sandcastle from "Sandcastle";

import * as Cesium from "cesium";

Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNjI4NjNlZi04MWMxLTRjYmItYTI0NC0zYjUyZGIxZmI0NmMiLCJpZCI6MzgxMTY4LCJpYXQiOjE3Njg5MDQ4ODZ9.WkcKtn2zfciDwC1n-qdnR77-h9BMcRrYL11CbrJbAAE';


const viewer = new Cesium.Viewer("cesiumContainer", {
  shouldAnimate: true,
});


try {
  const tileset1 = await Cesium.Cesium3DTileset.fromIonAssetId(2684829, {
    // Allow clamp to 3D Tiles
    enableCollision: true,
  });
  viewer.scene.primitives.add(tileset1);
} catch (error) {
  console.log(`Error loading tileset: ${error}`);
}
viewer.dataSources.add(
    Cesium.CzmlDataSource.load("/simple.czml"),
  );