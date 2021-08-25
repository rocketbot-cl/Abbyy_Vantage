function addOptions(skillsId) {
    var select = document.getElementById("skillsId")
    for (skillId of skillsId) {
        var opt = document.createElement('option');
        opt.value = skillId["id"];
        opt.innerHTML = skillId["name"];
        select.appendChild(opt);
        if (skillId["id"].toLowerCase() == document.skillsId_skillId) {
            opt.selected = true
        }
    }

}

data = getDataFromRB({module_name:"Abbyy_Vantage", command_name:"getHtmlSkillsId"})
.then(data => {
    var selectOption = {"id" : "-1", "name" : "---- Select Option ----", "type" : "nada"}
    data["skillsId"].push(selectOption)
    skillsId = data["skillsId"]
    skillsId.reverse()
    addOptions(skillsId)
})

