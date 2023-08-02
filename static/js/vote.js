import { Config } from "./config.js";

const imgs=document.querySelectorAll(".image-box");

document.querySelectorAll(".image-box").forEach(i=>{
    console.log("im working ")
    var check = i.querySelector(".my-check")
    check.addEventListener('click',(e)=> {
        console.log("im working 1")
        var vo = i.querySelector(".times-voted")
        var box=i.querySelector(".vote-box")
        console.log("votes", vo.innerHTML)
        console.log("im working 2")
        if (check.style.backgroundColor!== 'red') {
            check.style.backgroundColor= 'red'
            vo.innerHTML = parseInt(vo.innerHTML)+ 1
            console.log("votes", vo)
        } else if (check.style.backgroundColor=== 'red'){
            check.style.backgroundColor= 'white'
            vo.innerHTML = parseInt(vo.innerHTML)- 1
            console.log("votes", vo)
        }
    })
})

document.changeVote=function (){

}