import { Config } from "./config.js";
function myFunction() {
        window.location.href="http://programminghead.com";
}

console.log("i'm loaded");
const loader = document.querySelector("#loading");

let AI_image;
window.displayLoading=function () {
    loader.classList.add("display");
    // to stop loading after some time
    //let text=document.createElement('h2')
    //text.innerHTML="The AI is generating your image, please wait"
    //text.style.color='black'
    document.getElementById('AI_box_txt').style.display='flex'
}

// hiding loading
window.hideLoading=function () {
    loader.classList.remove("display");
    document.getElementById('AI_box_txt').style.display='none'
}


window.checksubmit=function () {
    let des = document.getElementById('textbox')
    if (des.value.length < 5){
        console.log('insert valid description')
        window.alert('please insert a valid description')
    }else{
        document.getElementById('submit_btn').disabled=true
        if(document.getElementById('AI_image')){
            document.getElementById('AI_image').src=''
        }
        var message = document.getElementById("textbox");
        var entry = {
            message: message.value
        };
        displayLoading()
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
                hideLoading()
                window.showOnscreen(data);
                document.getElementById('submit_btn').disabled=false
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
