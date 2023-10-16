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

window.get_paintings = function(){
    fetch(`${Config.BASE_URL}/start_paints`, {
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
                img_box.className = 'grid-item'
                img_box.dataset.name = key
                var img = document.createElement('img')
                var text = document.createElement("h6")
                var caption=document.createElement('div')
                caption.className='caption'
                caption.innerText=key
                text.textContent = key;
                img.src = value;
                //img.className="w-full h-64 object-cover img-fluid"
                //img.style.filter='blur(15px)'

                img_box.appendChild(img);
                img_box.appendChild(caption);
                document.querySelector(".grid-container").appendChild(img_box)
            }
            document.querySelectorAll(".grid-item").forEach(ib=>{
                ib.addEventListener("click", e=>{
                    changeSelection(ib,ib.dataset.name, ib.getElementsByTagName('img' )[0].src)
                    })
                })
        })
}
document.addEventListener("DOMContentLoaded", get_paintings);
document.addEventListener("DOMContentLoaded", author_list);