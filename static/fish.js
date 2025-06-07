// fish.js
const canvas = document.getElementById("fishCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const fishImage = new Image();
fishImage.src = "/static/wordcloud.jpg";

const fish = [
    { img: fishImage, x: 100, y: 100, dx: 1, dy: 0.5, width: 100, height: 60 },
    { img: fishImage, x: 300, y: 200, dx: -0.5, dy: 1, width: 100, height: 60 },
    { img: fishImage, x: 500, y: 400, dx: 0.7, dy: -0.3, width: 100, height: 60 }
];

function drawFish(f) {
    if (f.img.complete) {
        ctx.drawImage(f.img, f.x, f.y, f.width, f.height);
    }
}

function updateFish(f) {
    f.x += f.dx;
    f.y += f.dy;

    if (f.x + f.width > canvas.width || f.x < 0) f.dx *= -1;
    if (f.y + f.height > canvas.height || f.y < 0) f.dy *= -1;
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fish.forEach(f => {
        drawFish(f);
        updateFish(f);
    });
    requestAnimationFrame(animate);
}

animate();
