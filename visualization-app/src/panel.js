 export function handle_panel(dataSource){

    
    var entities = dataSource.entities.values
    entities.forEach(entity => {
        if(entity.billboard || entity.id.match(SensorRegex)){
            const checkbox = document.getElementById(entity.id)
            checkbox.addEventListener("change" , display_Sat(entity.id,checkbox,dataSource))
        }
    })

    //Sat85.show = checkbox_moon1.checked;
    //Sat916300.show = checkbox_moon2.checked;
}

var SensorRegex= new RegExp("Sensor")

export function create_panel(dataSource){
    var panel = document.getElementById("sidePanel")
    var entities = dataSource.entities.values
    entities.forEach(entity => {
        if(entity.billboard){
            const container = document.getElementById("box_sat");

            const label = document.createElement("label");
            const checkbox = document.createElement("input");

            checkbox.type = "checkbox";
            checkbox.id = entity.id;
            checkbox.checked = true;

            label.appendChild(checkbox);
            label.append(entity.name);

            container.appendChild(label);
            
        }
    })

    //var SensorRegex= new RegExp("Sensor")

    entities.forEach(entity => {
        if(entity.id.match(SensorRegex)){
            const container = document.getElementById("box_sensor")
            const label = document.createElement("label")
            const checkbox = document.createElement("input")

            checkbox.type = "checkbox"
            checkbox.id= entity.id
            checkbox.checked = true

            label.appendChild(checkbox)
            label.append(entity.name)

            container.appendChild(label)
        }
    })
}

function show85(id,dataSource){
    const link = dataSource.entities.getById(id)
    var name = link.name
    
    const entities = dataSource.entities.values
    entities.forEach(entity => {
        var regex = new RegExp("85")
        if(entity.name.match(/85/g)){
            entity.show = true
        }

    });

}

function display_Sat(id,checkbox,dataSource){
    //var checked = checkbox.checked
    var entities = dataSource.entities.values
    entities.forEach(entity => {
        var regex = new RegExp(id)
        if(entity.polyline){
            //console.log(entity.name)
            var positions = entity.polyline.positions
            //console.log(positions._value)
            var references = positions._value
            if(references[0]._targetId.match(regex) ){
                entity.show = checkbox.checked
                const second_entity = dataSource.entities.getById(references[1]._targetId)
                entity.show = second_entity.show ? entity.show:false
            }else if(references[1]._targetId.match(regex)){
                entity.show = checkbox.checked
                const second_entity = dataSource.entities.getById(references[0]._targetId)
                entity.show = second_entity.show ? entity.show:false
            }else{
            }
        }
        
    })
    const sat = dataSource.entities.getById(id)
    sat.show = checkbox.checked
           
}
