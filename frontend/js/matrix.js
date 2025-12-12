// ================================
// MATRIX CORE :: FTM-2077
// ================================

const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

// -------------------------------
// RESIZE HANDLING
// -------------------------------
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// -------------------------------
// MATRIX DATA
// -------------------------------
const letters = "01FTM2077ΩΔ";
const fontSize = 16;
let columns = Math.floor(canvas.width / fontSize);
let drops = Array(columns).fill(1);

// -------------------------------
// STATE CONTROL
// -------------------------------
let matrixSpeed = 50;
let matrixColor = "#00ff66";
let running = true;

// -------------------------------
// DRAW LOOP
// -------------------------------
function drawMatrix() {
    if (!running) return;

    ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = matrixColor;
    ctx.font = `${fontSize}px monospace`;

    drops.forEach((y, i) => {
        const text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, y * fontSize);

        if (y * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        } else {
            drops[i]++;
        }
    });
}

// -------------------------------
// LOOP CONTROL
// -------------------------------
let interval = setInterval(drawMatrix, matrixSpeed);

// -------------------------------
// EXTERNAL CONTROLS (HOOKABLE)
// -------------------------------
function matrixProcessingMode() {
    matrixColor = "#ffaa00";
    matrixSpeed = 30;
    resetLoop();
}

function matrixIdleMode() {
    matrixColor = "#00ff66";
    matrixSpeed = 60;
    resetLoop();
}

function matrixGodMode() {
    matrixColor = "#ff0033";
    matrixSpeed = 20;
    resetLoop();
}

function resetLoop() {
    clearInterval(interval);
    interval = setInterval(drawMatrix, matrixSpeed);
}

// Expose to global
window.matrixProcessingMode = matrixProcessingMode;
window.matrixIdleMode = matrixIdleMode;
window.matrixGodMode = matrixGodMode;
