import {Config} from "./config.js";


function downloadImage(canvas) {
var anchor = document.createElement("a");
anchor.href = canvas.toDataURL("image/png");
anchor.download = "IMAGE.PNG";
anchor.click();
}

function draw_canvas(path1, path2, canvas) {
    const ctx = canvas.getContext("2d");
    const image1 = new Image();
    image1.src = path1;
    image1.onload = () => {
        // Draw the first image
        ctx.drawImage(image1, 0, 0, canvas.width / 2, canvas.height);
    }

    const image2 = new Image();
    image2.src = path2;
    image2.onload = () => {
        // Draw the second imag
        ctx.drawImage(image2, canvas.width / 2, 0, canvas.width / 2, canvas.height);
    }
}


function image(path) {
     var canvas = document.getElementById('canvas');
     var context = canvas.getContext('2d');
     var image = new Image();
     image.onload = function() {
          context.drawImage(image, 50, 50);
     };
     image.src = path;
}
function create_download_btn(){
    var button=document.createElement('a');
    button.className='download-button'
    var spn = document.createElement('span')
    spn.style.color='white'
    var svg =document.createElement('svg');
    svg.className='download-icon'
    svg.setAttribute('xmlns',"http://www.w3.org/2000/svg")
    svg.setAttribute('viewBox','0 0 24 24')
    var dwnldimage=document.createElement('image')
    dwnldimage.setAttribute('height', 24)
    dwnldimage.setAttribute('width', 24)
    dwnldimage.setAttribute('href', '/static/css/assets/downlinearrow.png')
    svg.appendChild(dwnldimage)
    spn.appendChild(svg)
    spn.innerText='Download'
    button.appendChild(spn)
    return button
}

window.get_user_paintings = function() {
    fetch(`${Config.BASE_URL}/userCollection/getUserImgs`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response => response.json())
        .then(json => {
            console.log(json)
            console.log("received", JSON.stringify(json))
            let list=json.keys;
            let i=0
            for(const [key, value] of Object.entries(json)) {
                console.log("counter",i)
                    i=i+1
                console.log("AP", key, value)
                console.log("key",key)
                console.log( "value:", value.original_path, value.original_name)
                var canvas_box = document.createElement('div')
                canvas_box.className = 'canvas-cell'
                //canvas_box.dataset.name = key
                var separator=document.createElement('div')
                separator.className='collection-separator'
                var canvas = document.createElement('canvas')
                canvas.className='canvas'
                var description_box=document.createElement('div')
                description_box.className='canvas-description'
                var description_title = document.createElement("h5")
                var description_p=document.createElement('p')
                var download=create_download_btn()
                console.log("ad1", value.original_name)
                description_title.innerText=value.original_name
                console.log("ad2", value.description)
                description_p.innerText=value.description
                description_box.appendChild(description_title)
                description_box.appendChild(description_p)
                description_box.appendChild(download)
                //img_box.appendChild(canvas)
                //img.style.filter='blur(15px)'
                //setUpCanvas(img, value,img_box)
                canvas_box.appendChild(canvas)

                canvas_box.appendChild(description_box);
                document.querySelector(".content-container").appendChild(separator)
                document.querySelector(".content-container").appendChild(canvas_box)
                console.log("ad3", key)
                draw_canvas(value.original_path,key,canvas)
                //download.addEventListener('click', downloadImage(canvas))
            }
            document.querySelectorAll(".canvas-cell").forEach(ib=>{
                ib.getElementsByTagName('a')[0].addEventListener("click", e=>{
                    downloadImage(ib.getElementsByTagName('canvas' )[0])
                    })
                })
        })
}

document.addEventListener('DOMContentLoaded',get_user_paintings);
