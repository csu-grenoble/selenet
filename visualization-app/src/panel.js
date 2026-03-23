/*
 * SeleNet
 * 
 * Authors : Nada Yassine, Meli Scott Douanla 
 */

export function handle_panel(dataSource){

    
    var entities = dataSource.entities.values
    entities.forEach(entity => {
        if(entity.billboard || entity.id.match(regexGnd)){
            const checkbox = document.getElementById(entity.id)
            checkbox.addEventListener("change" , display_Sat(entity.id,checkbox,dataSource))
        }
    })
}

var regexGnd= new RegExp("Gnd")

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

    entities.forEach(entity => {
        if(entity.id.match(regexGnd)){
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
