import { Config } from "./config.js";
function myFunction() {
        window.location.href="http://programminghead.com";  
}

console.log("i'm loaded");

/*

const response = await fetch(`${config.BASE_URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });


*/
let AI_image;

window.checksubmit=function () {
    let des = document.getElementById('textbox')
    if (des.value.length < 5){
        console.log('insert valid description')
        window.alert('please insert a valid description')
    }else
    {
        var message = document.getElementById("textbox");
        var entry = {
            message: message.value
        };
        // takes 2 argument an url or endpoint where to post or get data from
        // and an init constructor,object full of instructions
        fetch(`${Config.BASE_URL}/generate`, {
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(entry),
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
                console.log(data)
                window.getPicture();
            })
        })
    }
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
        let image = document.getElementById("AI_image");
        image.src = json;
        AI_image=json;
        console.log(AI_image)
        document.getElementById('AI_image')
            .style.display = "block";
    })
}


window.openNav=function() {
  document.getElementById("myNav").style.height = "100%";
}
window.closeNav=function() {
  document.getElementById("myNav").style.height = "0%";
}

window.withoutFormat=function (pictureLabel){
     var author = document.getElementById("selected_author");
     author.substring("", pictureLabel.lastIndexOf("."));
}



window.checkform=function () {
        var f = document.forms["description_form"].elements;
        var cansubmit = true;

        for (var i = 0; i < f.length; i++) {
            if (f[i].value.length === 0)
                cansubmit = false;
        }

        if (cansubmit) {
            document.getElementById('submitbutton').disabled = !cansubmit;
        }
    }

//IMG ZOOM
window.zoomImage=function() {
    if (document.getElementById('zoomedImage')){
            const image = document.getElementById('zoomedImage');
            image.classList.toggle('zoomed');
            image.position.absolute

        }else if(document.getElementById('zoomedImage1')) {
            const image = document.getElementById('zoomedImage');
            image.classList.toggle('zoomed');
        }
    }
const obj = { hello: "world" };
console.log("the image is", AI_image)

