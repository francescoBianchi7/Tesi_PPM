import { Config } from "./config.js";

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


window.getPicture=function() {
    fetch(`${Config.BASE_URL}/pictures`,{
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response=>response.json())
        .then(json=>{
            console.log("receive:", json)
        let image = document.getElementById("test-img");
        image.src = json;
        document.getElementById('test-img')
            .style.display = "block";
    })
}

const search=document.querySelector(".search_box input"),
        images=document.querySelectorAll(".image-box");

search.addEventListener("keyup", e=>{
    if(e.key==="Enter"){
        let searchValue=search.value,
            value=searchValue.toLowerCase();

            images.forEach(image=>{
                console.log(image.dataset.name.toLowerCase());
                if(image.dataset.name.toLowerCase().includes(value)){
                    return image.style.display="block";
                }
                image.style.display="none";
            });
    }
});

search.addEventListener("keyup", () =>{
    if(search.value !=="")return;
    images.forEach(image=>{
        image.style.display="block"
    })
});

/*window.showList=function (){
    let aut= document.getElementById("authors_list")
    if(aut.data!==""){
        document.getElementById('painting_list').data='onion'
    }
}*/
const author= document.querySelector(".select-ddb"),
    list=document.querySelector(".painting_list")

author.addEventListener("change", (event)=>{
    if(author.value!=="") {
        list.textContent=author.value
    }
})

window.painting = function(){
    var author=document.getElementById("name");
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