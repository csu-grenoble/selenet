 export function handle_panel(dataSource){
    const Sat85 = dataSource.entities.getById("Sat_-85");
    const Sat916300   = dataSource.entities.getById("Sat_-916300")
    Sat85.billboard.show = true


    const checkbox_moon1 = document.getElementById("toggleOrbits");
    const checkbox_moon2 = document.getElementById("toggleLinks")

    
    // équivalent du callback Sandcastle
    checkbox_moon1.addEventListener("change", function () {
        const checked = checkbox_moon1.checked;
        //Sat85.billboard.show = !Sat85.billboard.show
    });

    checkbox_moon2.addEventListener("change", function() {
        const checked = checkbox_moon2.checked;
    })

    Sat85.show = checkbox_moon1.checked;
    Sat916300.show = checkbox_moon2.checked;
}

function showLink(id){
    const link = dataSource.entities.getById(id)
    var name = link.name
    
}

