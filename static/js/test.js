import { Config } from "./config.js";
var selected, selectedpath;
window.submit_entry = function(){
    var name=document.getElementById("name");
    var message=document.getElementById("message");

    var entry={
        name: name.value,
        message: message.value
    };
    // takes 2 argument an url or endpoint where to post or get data from
    // and an init constructor,object full of instructions
    fetch(`${Config.BASE_URL}/test/entry`, {
        method: "POST",
        credentials: "include", //cookies on the page
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response){
            if(response.status !==200){
                console.log('response was not 200: ${response.status}')
                return ;
            }
            response.json().then(function(data){
                console.log(data)
            })
        }).then(function (){
            if(entry.value!=='')
                document.getElementById('testbtn').disabled=false
    })
}

const   search=document.querySelector(".search_box input"),
        images_block=document.querySelectorAll(".images"),
        imgs=document.querySelectorAll(".image-box > img"),
        images=document.querySelectorAll(".image-box");
imgs.forEach(i=>{
    i.style.filter='blur(10px)'
})

search.addEventListener("keyup", e=>{
    if(e.key==="Enter"){
        let searchValue=search.value,
            value=searchValue.toLowerCase();
            console.log("x", value)
            document.querySelectorAll(".image-box").forEach(image=>{
                console.log("check",image.dataset.name.toLowerCase());
                if(image.dataset.name.toLowerCase().includes(value)){
                    console.log("found", image.dataset.name.toLowerCase());
                    return image.style.display="block";
                }
                image.style.display="none";
            });
    }
});
search.addEventListener("keyup", () =>{
    if(search.value !=="")return;
    document.querySelectorAll('.image-box').forEach(image=>{
        image.style.display="block";

    })
});

window.getPicture = function(id) {
    fetch(`${Config.BASE_URL}test/get_paint_db`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(id),
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response=>response.json()).then(json=>{
        console.log(json)
        var src=json
        console.log("GOOGOGOAGOSDGOSA",src)
        document.getElementById("test-img").src=src
    })
}
/*window.showList=function (){
    let aut= document.getElementById("authors_list")
    if(aut.data!==""){
        document.getElementById('painting_list').data='onion'
    }
}*/
const author= document.querySelector(".select-ddb"),
    list=document.querySelector(".painting_list"),
    list2 =document.querySelector(".temp"),
    list_p=document.querySelector(".paintings_list")


window.painting = function(){
    var entry= author.value
    console.log("test", author.value)
    // takes 2 argument an url or endpoint where to post or get data from
    // and an init constructor,object full of instructions
    fetch(`${Config.BASE_URL}/test/paint`, {
        method: "POST",
        credentials: "include", //cookies on the page
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response){
            if(response.status !==200){
                console.log('response was not 200: ${response.status}')
                return ;
            }
            response.json().then(function(data){
                console.log("data", data)
                console.log(Object.keys(data).length)
                list2.textContent=data[1]
                window.painting_selection(data)
                document.getElementById("paintings").disabled=false
            })
        })
}

window.changeSelection=function (name,path){
    selected=name;
    selectedpath=path;
    console.log("you selected", selected);
    console.log("path is", selectedpath);
    document.getElementById("temp_select").textContent=selected
        document.getElementById("is-btn").disabled=false
}

window.withoutFormat=function (pictureLabel){
     var author = document.getElementById("selected_author");
     var pic= pictureLabel.substring("", pictureLabel.lastIndexOf("."));
     return pic
}

window.withoutFormatDB=function (pictureLabel){
     pictureLabel=pictureLabel.replace('(',' ')
     pictureLabel=pictureLabel.replace(')','')
     pictureLabel=pictureLabel.substring("", pictureLabel.lastIndexOf(","));
     pictureLabel=pictureLabel.replace(" ' ",'')
     console.log("aadad", pictureLabel)
     return pictureLabel
}

window.painting_selection=function (paint_list){
    var num=Object.keys(paint_list).length,
        select=document.getElementById("paintings_list");
    if(select.options.length>0)
        window.removeAllValues(select)

    var first=document.createElement('option')
    first.value=0
    first.innerHTML=""

    select.appendChild(first)
    for(var i=1;i<=num;i++){
        var opt = document.createElement('option');
        opt.value = i;
        opt.innerHTML = paint_list[i-1];
        select.appendChild(opt);
    }
}

window.removeAllValues=function(select){
    let options = select.getElementsByTagName('option');

    for (var i=options.length; i--;) {
        select.removeChild(options[i]);
    }
}

window.activateBtn=function (){
    if(document.getElementById("painting_list").value !== ''){
        console.log("btn is active");
    }
}

window.get_paintings = function(){
    fetch(`${Config.BASE_URL}/test/search_paint_db`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
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
                    changeSelection(ib.dataset.name, ib.getElementsByTagName('img' )[0].src)
                    })
                })
        })
}
document.addEventListener("DOMContentLoaded", get_paintings);