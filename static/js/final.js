import { Config } from "./config.js";
console.log("final load")


window.setimage=function (){
    let temp=document.getElementById("zoomedImage")
    console.log(AI_image)
    temp.src=AI_image
    document.getElementById('zoomedImage')
            .style.display = "block";
}

window.downloadFile=function() {
        document.getElementById()
         window.open()
      }

// script.js
// script.js

var similarityScore = 15; // Example similarity score (0 to 100)

        // Normalize the similarity score to a percentage (0-100)
var normalizedScore = similarityScore;

        // Set the width of the bars based on the similarity score
document.getElementById("similarity").style.width = normalizedScore + "%";
//document.getElementById("similarityTemp").style.width = (100 - normalizedScore) + "%";

document.getElementById("similarity-txt").innerHTML = "similarity: "+  normalizedScore + "%";
//document.getElementById("similarityTemp").innerHTML = "Image 2 (" + (100 - normalizedScore) + "%)";