import { Config } from "./config.js";
function myFunction() {
        window.location.href="http://programminghead.com";  
}

console.log("i'm loaded");

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
                console.log("picture is", data)
                window.showOnscreen(data);
            })
        })
    }
}

window.showOnscreen=function(data){
    if(!document.getElementById('AI_image')) {
        let image = document.createElement("img")
        image.id = 'AI_image';
        document.getElementById("img_block").appendChild(image);
    }
    document.getElementById('AI_image').src = data;

    AI_image=data;
    console.log(AI_image)
    document.getElementById('AI_image')
        .style.display = "block";
    document.getElementById('AI_image')
        .style.position= "center";
    if(document.getElementById("AI_image").src!=='') {
          document.getElementById('endBtn').disabled = false
    }
}


window.openNav=function() {
  document.getElementById("myNav").style.height = "100%";
}
window.closeNav=function() {
  document.getElementById("myNav").style.height = "0%";
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

