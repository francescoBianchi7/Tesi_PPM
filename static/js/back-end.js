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


window.getSelectedCollection=function (){
    let opt=document.getElementById('collection_list')
    return opt.value
}

window.paints_by_collection=function (){
    let selected = document.getElementById("collection_list");
    if(selected.value==='empty'){
        console.log('no value')
     //  remove_options(document.getElementById("painting_list"))
       // document.getElementById("painting_list").value='empty'
    }
    else {
        fetch(`${Config.BASE_URL}/back_end/get_paints_by_collection`, {
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(selected.value),
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
                    console.log(value.description)
                    console.log(value.path)
                    var img_box = document.createElement('div')
                    var caption=document.createElement('div')
                    img_box.className = 'grid-item'
                    var img = document.createElement('img')
                    var text = document.createElement("h6")
                    caption.className='caption'
                    text.textContent = key;
                    caption.appendChild(text)
                    img.className='collectionimage'
                    img.src = value.path;
                    img_box.appendChild(img);
                    img_box.appendChild(caption);

                    var description_box= document.createElement('div')
                    description_box.className='img-description'
                    var img_description= document.createElement('p')
                    img_description.innerText=value.description
                    img_description.textContent=value.description
                    description_box.appendChild(img_description)

                    var checkbox=document.createElement('input')
                    checkbox.type='checkbox'
                    checkbox.className='checkbox'

                    var cell = document.createElement('div')
                    cell.className='collection-cell'
                    cell.appendChild(img_box)
                    cell.appendChild(description_box)
                    cell.appendChild(checkbox)
                    console.log(cell)
                    document.getElementById('be-container').appendChild(cell)

                }
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


window.collection_list=function (){
    fetch(`${Config.BASE_URL}/back_end/get_collections`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response=>response.json())
        .then(json=>{
            console.log("received", JSON.stringify(json))
            let list=document.getElementById("collection_list")
            let empty= document.createElement('option')
            empty.value=''
            empty.innerHTML=''
            list.appendChild(empty)
            for(const i in json) {
                console.log("f", json[i])
                let option = document.createElement("option")
                option.value = json[i]
                option.innerText = json[i]
                list.appendChild(option)
            }
        })
}


document.addEventListener("DOMContentLoaded", collection_list);

