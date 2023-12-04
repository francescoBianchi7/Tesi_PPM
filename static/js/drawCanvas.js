

// JavaScript (script.js)
import {Config} from "./config.js"


document.addEventListener('DOMContentLoaded', function () {
    // Add click event to the image container
    const imageContainer = document.getElementById('be-container');
    imageContainer.addEventListener('click', function (event) {
        if (event.target.tagName === 'IMG') {
            // If the clicked element is an image, open the canvas for that specific image
            const imageSource = event.target.src;
            const name= event.target.parentNode.lastElementChild.textContent

            openCanvas(imageSource,name);
        }
    });
});

function openCanvas(imageSource, name) {
    const canvasContainer = document.getElementById('canvasContainer');
    canvasContainer.style.display = 'block';

    const canvas = document.getElementById('imageCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 600;  // Set the desired width
    canvas.height = 800; // Set the desired height
    const img = new Image();
    img.onload = function () {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
    img.src = imageSource;

    enableDrawing(canvas,img);

    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'buttonContainer';
    buttonContainer.style.display='flex'
    buttonContainer.style.justifyContent='space-evenly'
    const closeButton = document.createElement('button');
    closeButton.innerHTML = 'Close';
    closeButton.id = 'closeButton';
    closeButton.className = 'blurButton';
    closeButton.onclick = function () {
        canvasContainer.style.display = 'none';
    };
    buttonContainer.appendChild(closeButton);

    const clearButton = document.createElement('button');
    clearButton.innerHTML = 'Clear Drawing';
    clearButton.id = 'clearButton';
    clearButton.className = 'blurButton';
    clearButton.onclick = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
    buttonContainer.appendChild(clearButton);

    const saveButton = document.createElement('button');
    saveButton.innerHTML = 'Save Drawing';
    saveButton.id = 'saveButton';
    saveButton.className = 'blurButton';
    saveButton.onclick = function () {
        saveImage(canvas,name)
    };
    buttonContainer.appendChild(saveButton);

    const existingButtonContainer = document.getElementById('buttonContainer');
    if (existingButtonContainer) {
        existingButtonContainer.remove();
    }

    canvasContainer.appendChild(buttonContainer);
}

function enableDrawing(canvas,img) {
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let startX, startY;

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    function startDrawing(e) {
        isDrawing = true;
        const rect = canvas.getBoundingClientRect();
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
    }

     function draw(e) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;

    const radiusX = Math.abs(currentX - startX) / 2;
    const radiusY = Math.abs(currentY - startY) / 2;
    const centerX = startX + radiusX;
    const centerY = startY + radiusY;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the original image with a blur effect for the entire canvas
    ctx.filter = 'blur(20px)'; // Adjust the blur radius as needed
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    ctx.filter = 'none'; // Reset filter

    // Draw the original image without blur only inside the ellipse
    ctx.save(); // Save the current context state
    ctx.beginPath();
    ctx.ellipse(centerX, centerY, radiusX, radiusY, 0, 0, 2 * Math.PI);
    ctx.clip();
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    ctx.restore(); // Restore the context state
    }

    function stopDrawing() {
        isDrawing = false;
    }
}
function saveImage(canvas, name) {

    var link = canvas.toDataURL('image/png');
    console.log('ling',link)

    var entry = {
           blurred: link,
            name: name
        };
    fetch(`${Config.BASE_URL}/back_end/save_blurred_img`, {
        method: "POST",
        credentials: "include", //cookies on the page
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
}