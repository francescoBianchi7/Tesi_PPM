import { Config } from "./config.js";


window.generate=function () {
fetch(`${Config.BASE_URL}/generate`, {
            method: "GET",
            credentials: "include", //cookies on the page
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
                console.log("picture is", data)
                window.location=window.location.origin+"/result"
            })
        })
}

document.addEventListener("DOMContentLoaded", generate);