const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const letters = "01FTM2077ΩΔ";
const drops = Array(Math.floor(canvas.width / 20)).fill(1);

function draw() {
    ctx.fillStyle = "rgba(0,0,0,0.05)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#0f0";
    ctx.font = "16px monospace";

    drops.forEach((y, i) => {
        const text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * 20, y * 20);

        drops[i] = y * 20 > canvas.height && Math.random() > 0.975 ? 0 : y + 1;
    });
}
setInterval(draw, 50);
