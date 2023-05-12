console.log("final load")



window.setimage=function (){
    let temp=document.getElementById("zoomedImage")
    console.log(AI_image)
    temp.src=AI_image
    document.getElementById('zoomedImage')
            .style.display = "block";
}