// ================================
// AI FACE CORE (FTM-2077)
// ================================

let facePixels = [];

// -------------------------------
// BOOT FACE
// -------------------------------
function bootFace() {
    const face = document.getElementById("ai-face");
    if (!face) return;

    face.innerHTML = "";
    facePixels = [];

    for (let i = 0; i < 400; i++) {
        const p = document.createElement("div");
        p.className = "pixel";
        face.appendChild(p);
        facePixels.push(p);
    }

    idleFace();
}

// -------------------------------
// IDLE ANIMATION
// -------------------------------
function idleFace() {
    facePixels.forEach(p => {
        p.style.opacity = Math.random() > 0.8 ? 1 : 0.2;
    });
}

// -------------------------------
// PROCESSING ANIMATION
// -------------------------------
function processingFace() {
    facePixels.forEach((p, i) => {
        setTimeout(() => {
            p.style.opacity = 1;
        }, i * 2);
    });
}

// -------------------------------
// SPEAKING ANIMATION (VOICE)
// -------------------------------
function speakingFace() {
    let pulse = true;

    const interval = setInterval(() => {
        facePixels.forEach(p => {
            p.style.opacity = pulse ? 1 : 0.3;
        });
        pulse = !pulse;
    }, 120);

    return interval;
}

// -------------------------------
// GOD MODE FACE
// -------------------------------
function godModeFace() {
    facePixels.forEach(p => {
        p.style.background = "red";
        p.style.opacity = 1;
    });
}

// -------------------------------
// RESET FACE
// -------------------------------
function resetFace() {
    facePixels.forEach(p => {
        p.style.background = "";
        p.style.opacity = 0.4;
    });
}

// Auto boot on load
document.addEventListener("DOMContentLoaded", bootFace);
