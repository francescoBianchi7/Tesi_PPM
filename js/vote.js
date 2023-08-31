import { Config } from "./config.js";

const imgs=document.querySelectorAll(".image-box");

window.commitVote=function(path,votes){
    var entry={
        path: path,
        votes: votes
    };
    fetch(`${Config.BASE_URL}/votes_update`, {
        method: "POST",
        credentials: "include", //cookies on the page
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(){
        console.log(entry)
    })
}


window.voting=function() {
    document.querySelectorAll(".image-box-v").forEach(i => {
        console.log("im working ")
        var check = i.querySelector(".my-check")
        check.addEventListener('click', (e) => {
            console.log("im working 1")
            var vo = i.querySelector(".times-voted")
            var box = i.querySelector(".vote-box")
            console.log("votes", vo.innerHTML)
            console.log("im working 2")
            if (check.style.backgroundColor !== 'red') {
                check.style.backgroundColor = 'red'
                vo.innerHTML = parseInt(vo.innerHTML) + 1
                console.log("votes", vo)
                var im=i.querySelector("img")
                commitVote(im.src,parseInt(vo.innerHTML))
            } else if (check.style.backgroundColor === 'red') {
                check.style.backgroundColor = 'white'
                vo.innerHTML = parseInt(vo.innerHTML) - 1
                console.log("votes", vo)
                var im=i.querySelector("img")
                commitVote(im.src,parseInt(vo.innerHTML))
            }
        })
    })
}


window.get_created= function(){
    fetch(`${Config.BASE_URL}/get_created`, {
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
                img_box.className = 'image-box-v'
                img_box.dataset.name = key
                var img = document.createElement('img')


                img.src = key;
                img_box.appendChild(img);
                var vote_box=vbox_create(value)
                img_box.appendChild(vote_box)
                document.querySelector(".images_f").appendChild(img_box)
            }
            voting()

        })
}

window.vbox_create=function(value){
        var vote_box=document.createElement("div")
        vote_box.className='vote-box'
        var text=document.createElement("h5")
        text.textContent='voted:'
        var votes = document.createElement("h3")
        votes.className='times-voted'
        votes.textContent = value;
        var input=document.createElement('input')
        input.type='button'
        input.className='my-check'
        vote_box.appendChild(text);
        vote_box.appendChild(votes);
        vote_box.appendChild(input);
        return vote_box
}
document.changeVote=function (){

}

document.addEventListener('DOMContentLoaded', get_created)
