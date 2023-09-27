import {Config} from "./config.js";
console.log("loaded")
const loader = document.querySelector("#loading");

/* Open */
window.openNav=function() {
    console.log("clicked")
    displayLoading()
  document.getElementById("myNav").style.display = "block";

}

/* Close */
window.closeNav=function () {
    hideLoading()
  document.getElementById("myNav").style.display = "none";
}

window.displayLoading=function () {
    loader.classList.add("display");
    // to stop loading after some time
    //let text=document.createElement('h2')
    //text.innerHTML="The AI is generating your image, please wait"
    //text.style.color='black'
}

// hiding loading
window.hideLoading=function () {
    loader.classList.remove("display");
}

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
            closeNav()
            window.alert(formData.get("name")+"added to database")
            author_list()
            paints_by_author()
        })
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

window.paints_by_author=function (){
    var selected = document.getElementById("authors_list");
    if(selected.value==='empty'){
        remove_options(document.getElementById("painting_list"))
        document.getElementById("painting_list").value='empty'
    }
    else {
        fetch(`${Config.BASE_URL}/get_paints_by_author`, {
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(selected.value),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            if (response.status !== 200) {
                console.log('response was not 200: ${response.status}')
                return;
            }
            response.json().then(function (data) {
                console.log("paints", data)
                var x = document.getElementById("painting_list")
                let element = document.getElementById("painting_list");
                remove_options(element)
                for (const i in data) {
                    let option = document.createElement("option")
                    console.log("x", data[i])
                    option.value = data[i]
                    console.log("x1", option.value)
                    option.innerText = data[i]
                    console.log("x2", option.innerText)
                    document.getElementById("painting_list").appendChild(option)

                }
            })
        })
    }
}

window.deleteFile=function (){
    let aut=document.getElementById("authors_list")
    let painted=document.getElementById("painting_list")
    var entry={
        author: aut.value,
        painted: painted.value
    }
    console.log(entry)

    fetch(`${Config.BASE_URL}/remove_painting`, {
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
    }).then(response=>response.json())
        .then(json=>{
            var author=document.getElementById("authors_list")
            author.value='empty'
            var paint=document.getElementById("painting_list")
            paint.value='empty'
            author_list()
            paints_by_author()
            window.alert(json.value+"removed correctly")
        })
}

window.contains = function( value ) {
    let list=document.getElementById("authors_list")
    for ( var i = 0, l = list.length; i < l; i++ ) {
        if ( list[i].value === value ) {
            return true;
        }
    }
    return false;
}
window.remove_options=function (element){
    if(element) {
        var options=element.options
        for(var i=options.length-1; i>0;i--) {
            if(options[i].value!=='empty')
                console.log("asd",options[i])
                element.removeChild(options[i]);
        }
    }
}



document.addEventListener("DOMContentLoaded", author_list);