

window.downloadImage=function () {

var canvas = document.getElementById("canvas1");
var anchor = document.createElement("a");
anchor.href = canvas.toDataURL("image/png");
anchor.download = "IMAGE.PNG";
anchor.click();

}
const canvas1 = document.getElementById("canvas1");

const ctx = canvas1.getContext("2d");

const image1 = new Image();
        image1.src = "/static/created_images/Botticelli,%20Venere1.jpg";
        image1.onload = () => {
            // Draw the first image
            ctx.drawImage(image1, 0, 0, canvas1.width / 2, canvas1.height);
        };

        const image2 = new Image();
        image2.src = "/static/images/Botticelli/Botticelli,Birth of Venus.jpg";
        image2.onload = () => {
            // Draw the second image
            ctx.drawImage(image2, canvas1.width / 2, 0, canvas1.width / 2, canvas1.height);
        };


function image() {
            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');
            var image = new Image();
            image.onload = function() {
               context.drawImage(image, 50, 50);
            };
            image.src = '/static/created_images/Botticelli,%20Venere1.jpg';
         }

document.getElementById('download').addEventListener("click", downloadImage)