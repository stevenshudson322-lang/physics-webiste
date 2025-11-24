const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// ball properties
let x = 250;
let y = 150;
let vx = 2;
let vy = 2;
const radius = 20;
const gravity = 0.1;
const bounce = 0.8;

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // gravity
    vy += gravity;

    // move
    x += vx;
    y += vy;

    // bounce on walls
    if (x + radius > canvas.width || x - radius < 0) {
        vx = -vx;
    }

    // bounce on floor
    if (y + radius > canvas.height) {
        y = canvas.height - radius;
        vy = -vy * bounce;
    }

    // draw ball
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = "red";
    ctx.fill();

    requestAnimationFrame(update);
}

update();
