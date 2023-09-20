import {Config} from "./config.js";

const   search=document.querySelector(".search_box input"),
        images_block=document.querySelectorAll(".images"),
        imgs=document.querySelectorAll(".image-box > img"),
        images=document.querySelectorAll(".image-box");

var selected, selectedpath, selectedbox;

document.getElementById("temp_select").addEventListener("",e=>{
    document.getElementById("is-btn").disabled=false
    console.log(document.getElementById("is-btn").isEnabled())
})


search.addEventListener("keyup", e=>{
    let searchValue=search.value,
        value=searchValue.toLowerCase();
    document.querySelectorAll(".image-box").forEach(image=>{
        console.log(image.dataset.name.toLowerCase());
        if(image.dataset.name.toLowerCase().includes(value)){
            return image.style.display="block";
        }
        image.style.display="none";
    });
});

search.addEventListener("keyup", () =>{
    if(search.value !=="")return;
    images.forEach(image=>{
        image.style.display="block";
    })
});

window.submitSelected = function(name, path){
    var entry={
        name: name,
        path: path
    };
    // takes 2 argument an url or endpoint where to post or get data from
    // and an init constructor,object full of instructions
    fetch(`${Config.BASE_URL}/getPainting`, {
        method: "POST",
        credentials: "include", //cookies on the page
        body: JSON.stringify(entry),
        cache: "no-cache",
        mode: 'no-cors',
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(){
        console.log(entry)
    })
}

window.changeSelection=function (ib,name,path){
    if(selectedbox)
        selectedbox.style.borderColor='black'
    if(ib.style.borderColor!=='red') {
        selected = name;
        selectedpath = path;
        selectedbox=ib;
        ib.style.borderColor='red'
        console.log("you selected", selected);
        console.log("path is", selectedpath);
        document.getElementById("temp_select").textContent = selected
        document.getElementById("is-btn").disabled = false
        submitSelected(name, path)
    }
}


window.getSelected=function (){
    return selected;
}

window.get_paintings = function(){
    fetch(`${Config.BASE_URL}/start_paints`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        mode: 'no-cors',
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response=>response.json())
        .then(json=>{
            console.log("received", JSON.stringify(json))
            let list=json.keys
            for(const [key, value] of Object.entries(json)) {
                console.log("AP", key, value)
                var img_box = document.createElement('div')
                img_box.className = 'image-box'
                img_box.dataset.name = key
                var img = document.createElement('img')
                var text = document.createElement("h6")
                text.textContent = key;
                img.src = value;
                img.style.filter='blur(15px)'
                img_box.appendChild(img);
                img_box.appendChild(text);
                document.querySelector(".images").appendChild(img_box)
            }
            document.querySelectorAll(".image-box").forEach(ib=>{
                ib.addEventListener("click", e=>{
                    changeSelection(ib,ib.dataset.name, ib.getElementsByTagName('img' )[0].src)
                    })
                })
        })
}
document.addEventListener("DOMContentLoaded", get_paintings);

