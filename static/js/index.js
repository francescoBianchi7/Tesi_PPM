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

function blurBackground() {
      blurContext.filter = 'blur(10px)'; // Adjust the blur radius as needed
      blurContext.drawImage(mainImage, 0, 0, blurCanvas.width, blurCanvas.height);
      blurContext.filter = 'none';
    }

function blurImage() {
    var img = document.getElementById('selected-img');

    var tracker = new tracking.ObjectTracker(['face']);
    tracker.setStepSize(1.7);

    tracking.track('#img', tracker);

    tracker.on('track', function (event) {
        event.data.forEach(function (rect) {
            window.plot(rect.x, rect.y, rect.width, rect.height);
        });
    });
    window.plot = function (x, y, w, h) {
        var rect = document.createElement('div');
        document.querySelector('.demo-container').appendChild(rect);
        rect.classList.add('rect');
        rect.style.width = w + 'px';
        rect.style.height = h + 'px';
        rect.style.left = (img.offsetLeft + x) + 'px';
        rect.style.top = (img.offsetTop + y) + 'px';
    }
}

window.setUpCanvas=function (canvas, img, value){
    const blurCanvas = canvas
    const blurContext = blurCanvas.getContext('2d');
    const ctx = canvas.getContext("2d");
    const image = new Image();
    tracking.Fast.
    image.src = value

    image.onload = () => {
        // Draw the first image
        const mainImage = img
        const tracker = new tracking.ObjectTracker('face');

        tracker.setInitialScale(4);
        tracker.setStepSize(2);
        tracker.setEdgesDensity(0.1);

        tracking.track(image, tracker);

        function blurBackground() {
            blurContext.filter = 'blur(10px)'; // Adjust the blur radius as needed
            blurContext.drawImage(mainImage, 0, 0, blurCanvas.width, blurCanvas.height);
            blurContext.filter = 'none';
        }

        tracker.on('track', (event) => {
            blurContext.clearRect(0, 0, blurCanvas.width, blurCanvas.height);

            if (event.data.length === 0) {
                // No subject found, blur the entire image
                blurBackground();
            } else {
                // Subject found, create a mask to keep it unblurred
                event.data.forEach(rect => {
                    blurContext.clearRect(rect.x, rect.y, rect.width, rect.height);
                });
            }
        });
        // Use tracking.js to detect faces
    }
}

document.addEventListener("DOMContentLoaded", setUpCanvas)
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