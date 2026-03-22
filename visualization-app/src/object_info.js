/*
 * SeleNet
 * 
 * Authors : Nada Yassine, Meli Scott Douanla 
 */
import * as Cesium from "cesium";


export function display_details(viewer,dataSource,id){

    //var entities = dataSource.entities.values     
    var entity = dataSource.entities.getById(id)

    var infoPanel = document.getElementById("infoTitle")
    var infoContent = document.getElementById("infoContent");

    infoContent.innerHTML = "";

    const regexSensor = RegExp("Sensor")
    const regexSat1 = RegExp("Sat_")
    const regexSat2 = RegExp("Satellite")
   
    if(entity.polyline){
        console.log(entity.polyline.show._intervals)
        entity.polyline.show._intervals._intervals.forEach(interval => {
            if(Cesium.JulianDate.greaterThanOrEquals(interval.stop, viewer.clock.currentTime) && Cesium.JulianDate.greaterThanOrEquals(viewer.clock.currentTime, interval.start)){
               
                const start = document.createElement("p");
                // TODO shorten the datetime format
                start.textContent = "Visible since: " + Cesium.JulianDate.toIso8601(interval.start, 0);

                const stop = document.createElement("p");
                // TODO shorten the datetime format
                stop.textContent = "Visible until: " + Cesium.JulianDate.toIso8601(interval.stop, 0);

                infoContent.appendChild(start);
                infoContent.appendChild(stop);
                
            }
            
        })
    }

    if(entity.id.match(regexSensor)){
        const entities = dataSource.entities.values
        const regex = new RegExp(id)

        var nbrSat = 0

        CountSat(entity.id,dataSource,viewer)

        entities.forEach(Entity => {
            
            if(Entity.polyline){
                var references = Entity.polyline.positions._value
                
                if(references[0]._targetId.match(regex) || references[1]._targetId.match(regex)){
                    console.log(Entity.name)
                    if(Entity.show==true){
                        //console.log(Entity.show)
                        nbrSat+=1
                    }
                }
            }
        })
        
        // const link = document.createElement("a");
        // link.textContent = "Follow this link for more information on this object";
        // link.href = "https://fr.wikipedia.org/wiki/"+entity.name
        // link.target = "_blank"; 

        // infoContent.appendChild(link)

        searchInfo(entity.name)
    }

    if(entity.id.match(regexSat1) || entity.id.match(regexSat2)){
        // const link = document.createElement("a");
        // link.textContent = "Follow this link for more information on this sensor";
        // link.href = "https://fr.wikipedia.org/wiki/"+entity.name
        // link.target = "_blank"; 
        // infoContent.appendChild(link)

        if(entity.polyline){
            return
        }
        const time = viewer.clock.currentTime;
        const position = entity.position.getValue(time);
        const cartographic = Cesium.Cartographic.fromCartesian(position);
        const altitude = cartographic.height;
        console.log("Altitude:", altitude, "meters");


        // Compute altitude
        const altitudeKm = (altitude / 1000).toFixed(2);
        const altText = document.createElement("p");
        altText.textContent = "Altitude : " + altitudeKm + " km";
        infoContent.appendChild(altText);

        // Compute speed
        const position1 = entity.position.getValue(time);


        // TODO change -30 and 30 by the value used for the generation
        const previousTime = Cesium.JulianDate.addSeconds(time, -30, new Cesium.JulianDate());
        const position0 = entity.position.getValue(previousTime);
        const distance = Cesium.Cartesian3.distance(position1, position0);
        let speed = distance / 30;
        speed = Math.round(speed);

        console.log("Speed :", speed, "m/s");

        const speedText = document.createElement("p");
        speedText.textContent = "Speed : " + speed + " m/s";
        infoContent.appendChild(speedText);

        searchInfo(entity.name)
    }

    infoPanel.textContent = entity.name

    if(entity.polyline){

    }else{
        fetch("assets/images/image.json")
        .then(response => response.json())
        .then(data => {

            // récupérer une image par son id
            const image = data.images.find(img => img.id === entity.id);

            const imgElement = document.createElement("img");
            imgElement.src = image.src;
            imgElement.alt = image.description;

            infoContent.appendChild(imgElement);

        }).catch(err => console.error("No image for this object"));
        getWikipediaInfo(entity.name) 
    }
}


export function searchInfo(objectName) {

    const results = document.getElementById("infoContent");
    //results.innerHTML = "";

    const sources = [
        {name: "NASA", site: "nasa.gov"},
        {name: "Wikipedia", site: "wikipedia.org"},
        {name: "IEEE", site: "ieee.org"}
    ];

    sources.forEach(source => {

        const link = document.createElement("a");

        const url = `https://www.google.com/search?q=${encodeURIComponent(objectName + " site:" + source.site)}`;

        link.href = url;
        link.target = "_blank";
        link.textContent = "Search on " + source.name;

        const line = document.createElement("p");
        line.appendChild(link);

        results.appendChild(line);

    });
}


export function getWikipediaInfo(objectName) {
    const url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(objectName);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // TODO : Translate : Vérifie s'il y a une image dans la page
            if (data.originalimage && data.originalimage.source) {
                const imgElement = document.createElement("img");
                imgElement.src = data.originalimage.source;
                imgElement.alt = objectName;

                infoContent.appendChild(imgElement);
                //console.log(`Image pour ${objectName}:`, data.originalimage.source);
            } else if (data.thumbnail && data.thumbnail.source) {
                // TODO : Translate : fallback sur la miniature si l'image originale n'existe pas
                const imgElement = document.createElement("img");
                imgElement.src = data.thumbnail.source;
                imgElement.alt = objectName;

                infoContent.appendChild(imgElement);
                console.log(`Thumbnail for ${objectName}:`, data.thumbnail.source);
            } else {
                console.log(`No image fournd for ${objectName}`);
            }
        })
        .catch(err => console.error("Error retrieving Wikipedia information:", err));
}


export function CountSat(id,dataSource,viewer){

    const entities = dataSource.entities.values
    const regex = new RegExp(id)
    entities.forEach(Entity => {
            
            if(Entity.polyline){
                var references = Entity.polyline.positions._value
                
                if(references[0]._targetId.match(regex) || references[1]._targetId.match(regex)){
                    console.log(Entity)
                    // if(Entity.show==true){
                    //     //console.log(Entity.show)
                    //     nbrSat+=1
                    // }
                }
            }
        })
}
