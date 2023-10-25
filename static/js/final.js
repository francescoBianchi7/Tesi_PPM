import { Config } from "./config.js";
console.log("final load")




window.backToGenerate=function (){
    window.location=window.location.origin+"/game"
}
window.toUserCollection=function (){
    window.location=window.location.origin+"/userCollection"
}
// script.js
// script.js
document.getElementById('back-to-index').addEventListener('click',backToGenerate)
document.getElementById('finish creation').addEventListener('click',toUserCollection)

var similarityScore = 15; // Example similarity score (0 to 100)

        // Normalize the similarity score to a percentage (0-100)
var normalizedScore = similarityScore;

        // Set the width of the bars based on the similarity score
document.getElementById("similarity").style.width = normalizedScore + "%";
//document.getElementById("similarityTemp").style.width = (100 - normalizedScore) + "%";

document.getElementById("similarity-txt").innerHTML = "similarity: "+  normalizedScore + "%";
//document.getElementById("similarityTemp").innerHTML = "Image 2 (" + (100 - normalizedScore) + "%)";