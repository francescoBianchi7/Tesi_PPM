import {Config} from "./config";

window.submitNewImg = function() {
    var paintingname = document.getElementById("paintingName")
    var author = document.getElementById("author")
    var file = document.getElementById("shown_file")
    const fileField = document.querySelector('input[type="file"]');

    if (file.value === '' || author.value === '' || paintingname.value === '') {
        console.log('not a valid submit')
        window.alert('please insert a valid description')
    } else {

        let formData =new FormData()
        formData.append("name",paintingname.value)
        console.log("name",formData.get("name"))
        formData.append("author",author.value)
        console.log("author",formData.get("author"))
        formData.append("file", fileField.files[0])
        console.log("file",formData.get("file"))
        console.log(fileField.files)
        var len = document.getElementById('training_files').files.length;
        console.log(len)
        for (let i=0; i<len; i++){
            let t="training"+i.toString()
            console.log("tr to send",document.getElementById('training_files').files[i])
            formData.append("training[]", document.getElementById('training_files').files[i]);
            console.log("files", formData.get("training[]"))
        }
        for(const [key, value] of formData) {
            console.log("all", key, value)
        }
        openNav()
        // takes 2 argument an url or endpoint where to post or get data from
        // and an init constructor,object full of instructions
        fetch(`${Config.BASE_URL}/upload-img`, {
            method: "POST",
            body: formData
            //headers: new Headers({
            //    "content-type": "application/json"
            //})
        }).then(function () {
            console.log(formData)
            window.alert(formData.get("name")+"added to database")
            author_list()
            paints_by_author()
        })
    }
}

window.paints_by_author=function () {
    var selected = document.getElementById("authors_list");
    if (selected.value === 'empty') {
        remove_options(document.getElementById("painting_list"))
        document.getElementById("painting_list").value = 'empty'
    }
}
window.author_list=function (){
    fetch(`${Config.BASE_URL}/authors`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response=>response.json())
        .then(json=>{
            console.log("received", JSON.stringify(json))
            let element=document.getElementById("authors_list")
            remove_options(element)
            for(const i in json) {
                console.log("f", json[i])
                let option = document.createElement("option")
                option.value = json[i]
                option.innerText = json[i]
                document.getElementById("authors_list").appendChild(option)
            }
        })
}