// js/bouncingBall.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("bouncingBall.js loaded");

  const canvas = document.getElementById("gameCanvas");
  if (!canvas) {
    console.error("Canvas element with id 'gameCanvas' not found. Check games.html has <canvas id='gameCanvas'> and script src='js/bouncingBall.js' is correct.");
    return;
  }

  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.error("Could not get 2D context from canvas.");
    return;
  }

  // ball properties
  let x = canvas.width / 2;
  let y = canvas.height / 2;
  let vx = 2;
  let vy = 2;
  const radius = 20;
  const gravity = 0.1;
  const bounce = 0.8;

  function update() {
    try {
      // clear
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // gravity
      vy += gravity;

      // move
      x += vx;
      y += vy;

      // bounce on walls
      if (x + radius > canvas.width) {
        x = canvas.width - radius;
        vx = -vx;
      } else if (x - radius < 0) {
        x = radius;
        vx = -vx;
      }

      // bounce on floor/ceiling
      if (y + radius > canvas.height) {
        y = canvas.height - radius;
        vy = -vy * bounce;
        // tiny threshold to stop jittering
        if (Math.abs(vy) < 0.15) vy = 0;
      } else if (y - radius < 0) {
        y = radius;
        vy = -vy * bounce;
      }

      // draw ball
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = "red";
      ctx.fill();
    } catch (err) {
      console.error("Error during update loop:", err);
      // stop animation to avoid flooding console
      return;
    }

    requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
});
