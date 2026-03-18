
//import * as Cesium from "cesium";

import "./css/time.css"
import "./css/panel.css"
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNjI4NjNlZi04MWMxLTRjYmItYTI0NC0zYjUyZGIxZmI0NmMiLCJpZCI6MzgxMTY4LCJpYXQiOjE3Njg5MDQ4ODZ9.WkcKtn2zfciDwC1n-qdnR77-h9BMcRrYL11CbrJbAAE';


const viewer = new Cesium.Viewer("cesiumContainer", {
  shouldAnimate: true,
  //ellipsoid: Cesium.Ellipsoid.MOON
});

const dataSource = await Cesium.CzmlDataSource.load("./simple.czml");
viewer.dataSources.add(dataSource);


function getLunarTime(dateUTC) {
  const lunarDayMs = 29.5 * 24 * 60 * 60 * 1000;

  const reference = Date.UTC(2000, 0, 1); // J2000
  const elapsed = dateUTC.getTime() - reference;

  const lunarMs = ((elapsed % lunarDayMs) + lunarDayMs) % lunarDayMs;
  const lunarHours = (lunarMs / lunarDayMs) * 24;

  const h = Math.floor(lunarHours);
  const m = Math.floor((lunarHours - h) * 60);
  const s = Math.floor((((lunarHours - h) * 60) - m) * 60);

  return `${h.toString().padStart(2,"0")}:${m.toString().padStart(2,"0")}:${s.toString().padStart(2,"0")}`;
}



function updateClocks() {
  const julian = viewer.clock.currentTime;
  const earthDate = Cesium.JulianDate.toDate(julian);

  document.getElementById("earthTime").textContent =
    earthDate.toISOString().substring(11, 19) + " UTC";

  document.getElementById("moonTime").textContent =
    getLunarTime(earthDate);
}

const panel = document.getElementById("sidePanel");
const toggleBtn = document.getElementById("panelToggle");

toggleBtn.onclick = () => {
  panel.classList.toggle("closed");
  // toggleBtn.textContent = toggleBtn.textContent=="▶" ? "◀": "▶";
  // panel.classList.toggle("collapsed");
  // toggleBtn.textContent =
  //   panel.classList.contains("collapsed") ? "▶" : "◀";
};




// Mise à jour à chaque frame
viewer.clock.onTick.addEventListener(updateClocks);


const entity = dataSource.entities.getById("Satellite/ISS");
entity.billboard.show = true


const checkbox = document.getElementById("toggleTileset");

// état initial
checkbox.checked = true;
//tileset.show = true;

// équivalent du callback Sandcastle
checkbox.addEventListener("change", function () {
  const checked = checkbox.checked;
  entity.billboard.show = !entity.billboard.show
  //tileset.show = checked;
});

entity.show = checkbox.checked;
