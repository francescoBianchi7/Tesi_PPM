import { config } from "config.js";
function myFunction() {
        window.location.href="http://programminghead.com";  
}
const response = await fetch(`${config.BASE_URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });