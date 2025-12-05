/* ==========================================================
   FTM-2077 HOLOGRAM FACE ENGINE
   Author: Zahid Hasan
   Handles:
   - Boot Glow Sequence
   - Hologram Flicker
   - AI Speaking Pulse
   - Random Glitch Shake
   ========================================================== */

const face = document.getElementById("holo-face");
const container = document.getElementById("holo-face-container");
const scanline = document.getElementById("scanline");

// -----------------------------
// 1. POWER ON BOOT SEQUENCE
// -----------------------------
function holoBoot() {
    face.style.opacity = "0";
    face.style.filter = "blur(8px) brightness(0.3)";

    setTimeout(() => {
        face.style.transition = "0.6s ease-out";
        face.style.opacity = "1";
        face.style.filter = "blur(0px) brightness(1.3)";
    }, 300);
}

holoBoot();

// -----------------------------
// 2. AI SPEAK REACTION EFFECT
// -----------------------------
function aiSpeakPulse() {
    face.style.transition = "0.05s linear";
    face.style.transform = "scale(1.05)";
    face.style.filter = "brightness(1.8) drop-shadow(0 0 25px #00f6ff)";

    setTimeout(() => {
        face.style.transform = "scale(1)";
        face.style.filter = "brightness(1.2)";
    }, 120);
}

// External trigger:
// Call this when backend returns audio or AI is talking:
window.ftmFaceSpeak = () => aiSpeakPulse();


// -----------------------------
// 3. RANDOM GLITCHING EFFECT
// -----------------------------
function randomGlitch() {
    const glitch = Math.random();

    if (glitch < 0.15) {  // 15% chance
        container.style.transform = `translate(${Math.random() * 4 - 2}px, ${Math.random() * 4 - 2}px)`;
        setTimeout(() => container.style.transform = "translate(0px,0px)", 60);
    }
}

setInterval(randomGlitch, 180);


// -----------------------------
// 4. SCANLINE SYNC (optional)
// -----------------------------
setInterval(() => {
    scanline.style.opacity = Math.random() * 0.6 + 0.2;
}, 150);


// -----------------------------
// 5. FACE REPLACE (AI Changing)
# Example: ftmSetFace("assets/generated/ai_face_ultron.png")
function ftmSetFace(path) {
    face.src = path;
    aiSpeakPulse();
}

window.ftmSetFace = ftmSetFace;
