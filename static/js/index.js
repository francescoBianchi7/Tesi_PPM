import { Config } from "./config.js";
function myFunction() {
        window.location.href="http://programminghead.com";
}

console.log("i'm loaded");
const loader = document.querySelector("#loading");
/* Open */


let AI_image;
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


window.checksubmit=function () {
    let des = document.getElementById('textbox')
    if (des.value.length < 5){
        console.log('insert valid description')
        window.alert('please insert a valid description')
    }else{
        if(document.getElementById('AI_image')){
            document.getElementById('AI_image').src=''
        }
        var message = document.getElementById("textbox");
        var entry = {
            message: message.value
        };

        //openNav()
        // takes 2 argument an url or endpoint where to post or get data from
        // and an init constructor,object full of instructions
        fetch(`${Config.BASE_URL}/postDescription`,{
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            console.log(response)
            window.location=window.location.origin+"/loading"
        })
    }
}


/**fetch(`${Config.BASE_URL}/generate`, {
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
                closeNav()
                window.location=window.location.origin+"/result"
                window.showOnscreen(data);
            })
        })**/