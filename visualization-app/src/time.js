/*
 * SeleNet
 * 
 * Authors : Nada Yassine, Meli Scott Douanla 
 */

function getLunarTime(dateUTC) {
  // TODO find the correct formulae
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


export function updateClocks(viewer) {
  const julian = viewer.clock.currentTime;
  const earthDate = Cesium.JulianDate.toDate(julian);

  document.getElementById("earthTime").textContent =
    earthDate.toISOString().substring(11, 19) + " UTC";

  document.getElementById("moonTime").textContent =
    getLunarTime(earthDate);
}
