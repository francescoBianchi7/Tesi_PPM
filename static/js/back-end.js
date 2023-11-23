import {Config} from "./config.js";
console.log("loaded")
const loader = document.querySelector("#loading");




window.getSelectedCollection=function (){
    let opt=document.getElementById('collection_list')
    return opt.value
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
const container = document.querySelector('#be-container');
removeAllChildNodes(container);

//TBD remove shown painting on collection switch
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
                removeAllChildNodes(container)

                for(const [key, value] of Object.entries(json)) {

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
                    var closebtn=document.createElement('span')
                    closebtn.className='close'
                    closebtn.innerHTML='&times;'
                    img_box.appendChild(closebtn)
                    img_box.appendChild(img);
                    img_box.appendChild(caption);

                    var description_box= document.createElement('div')
                    description_box.className='img-description'
                    var img_description= document.createElement('p')
                    img_description.innerText=value.description
                    img_description.textContent=value.description
                    img_description.className='m-3'
                    description_box.appendChild(img_description)

                    var checkbox=document.createElement('input')
                    checkbox.type='checkbox'
                    checkbox.className='checkbox'
                    checkbox.disabled=true
                    checkbox.checked=true

                    var cell = document.createElement('div')
                    cell.className='collection-cell'

                    cell.appendChild(img_box)
                    cell.appendChild(description_box)
                    cell.appendChild(checkbox)
                    console.log(cell)
                    document.getElementById('be-container').appendChild(cell)

                }
                openPopUp()
            })
    }
}


  // Hide the pop-up window when the close button is clicked

window.openPopUp=function(){
  var popupLink = document.querySelectorAll('.close');
  var popupWindow = document.getElementById("popup-window");
  var closeButton = document.getElementById("close-button");
  var popupText=document.getElementById("popup-text")
  var deleteButton=document.getElementById('delete-button')
  // Show the pop-up window when the link is clicked
  popupLink.forEach((c)=>{
      c.addEventListener("click", function(event) {
          var s="do you want to remove:"
          console.log(c.parentNode.children.item(1))
          deleteButton.addEventListener('click',function(){
              deleteFile(c.parentNode.lastElementChild.textContent)
          });
          popupText.textContent=s+c.parentNode.lastElementChild.textContent
          event.preventDefault();
          popupWindow.style.display = "block";
      });
  });

   closeButton.addEventListener("click", function() {
    popupWindow.style.display = "none";
  });
}


window.deleteFile=function (p_name){
    console.log('da', p_name)
    console.log('ad',document.getElementById('collection_list').value)
    let entry={
        name: p_name,
        collection: document.getElementById('collection_list').value
    }
    console.log('entry: ',entry)
    fetch(`${Config.BASE_URL}/back_end/remove_painting`, {
              method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })

    }).then(response=>response.json())
        .then(json=>{
            console.log(json+"removed correctly")
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
//TND
window.paints_finetune = function (){
    let selected = document.getElementById("collection_list");
    if(selected.value==='empty'){
        console.log('no value')
    }
    else {
        fetch(`${Config.BASE_URL}/back_end/get_finetuning`, {
            method: "POST",
            credentials: "include", //cookies on the page
            body: JSON.stringify(selected.value),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        })
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
            empty.value='empty'
            empty.innerHTML=''
            list.appendChild(empty)
            for(const i in json) {
                console.log("f", json[i])
                let option = document.createElement("option")
                option.value = json[i]
                option.innerText = json[i]
                option.style.width="100%"
                list.appendChild(option)
            }
        })
}


document.addEventListener("DOMContentLoaded", collection_list);

