import { Config } from "./config.js";
console.log("final load")




window.backToGenerate=function (){
    window.location=window.location.origin+"/game"
}
window.toUserCollection=function (){
    window.location=window.location.origin+"/userCollection"
}


window.get_similarity=function() {
    fetch(`${Config.BASE_URL}/get_similarity`, {
        method: "GET",
        credentials: "include", //cookies on the page
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(response => response.json())
        .then(json => {
            console.log(json)
            let similarityScore = json; // Example similarity score (0 to 100)

            // Normalize the similarity score to a percentage (0-100)
            let normalizedScore = similarityScore;
            // Set the width of the bars based on the similarity score
            document.getElementById("similarity").style.width = normalizedScore + "%";
            //document.getElementById("similarityTemp").style.width = (100 - normalizedScore) + "%";
            document.getElementById("similarity-txt").innerHTML = "similarity: " + normalizedScore + "%";
        })
}

document.getElementById('back-to-index').addEventListener('click',backToGenerate)
document.getElementById('finish creation').addEventListener('click',toUserCollection)

document.addEventListener('DOMContentLoaded',get_similarity)