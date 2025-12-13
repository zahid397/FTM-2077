// ===================================
// CONFIG
// ===================================
const API = "https://ftm-2077.onrender.com";
const DEFAULT_PERSONA = "JARVIS";

// ===================================
// GLOBAL STATE
// ===================================
let isRunning = false;
let audioUnlocked = false;

// ===================================
// DOM
// ===================================
const inputEl = document.getElementById("missionInput");
const outputEl = document.getElementById("missionOutput");
const playVoiceBtn = document.getElementById("playVoiceBtn");
const voicePlayer = document.getElementById("voicePlayer");

// ===================================
// AUDIO SETUP (MOBILE SAFE)
// ===================================
voicePlayer.preload = "auto";
voicePlayer.setAttribute("playsinline", "true");

function unlockAudio() {
  if (audioUnlocked) return;
  audioUnlocked = true;

  const silentWav =
    "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=";

  voicePlayer.src = silentWav;
  voicePlayer.load();

  voicePlayer.play()
    .then(() => {
      voicePlayer.pause();
      voicePlayer.currentTime = 0;
      console.log("🔊 Audio unlocked");
    })
    .catch(() => {});
}

document.addEventListener("click", unlockAudio, { once: true });
document.addEventListener("touchstart", unlockAudio, { once: true });

function playVoice() {
  if (!voicePlayer.src) return;
  if (voicePlayer.readyState < 2) {
    voicePlayer.oncanplay = () => voicePlayer.play();
  } else {
    voicePlayer.currentTime = 0;
    voicePlayer.play();
  }
}

// ===================================
// TYPING EFFECT
// ===================================
function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function typeText(target, text, speed = 18) {
  for (let i = 0; i < text.length; i++) {
    target.textContent += text[i];
    target.parentElement.scrollTop =
      target.parentElement.scrollHeight;
    await sleep(speed);
  }
}

// ===================================
// SEND MISSION (API)
// ===================================
async function sendMission() {
  if (isRunning) return;
  const text = inputEl.value.trim();
  if (!text) return;

  isRunning = true;
  playVoiceBtn.style.display = "none";

  outputEl.textContent += `\n\n> ${text}\n`;
  inputEl.value = "";

  try {
    const res = await fetch(`${API}/api/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command: text,
        persona: DEFAULT_PERSONA
      })
    });

    const data = await res.json();

    await typeText(
      outputEl,
      data.text || "[NO RESPONSE]",
      18
    );

    // optional voice
    if (data.audio) {
      voicePlayer.src = data.audio.startsWith("http")
        ? data.audio
        : `${API}${data.audio}`;
      playVoiceBtn.style.display = "block";
    }

  } catch (e) {
    outputEl.textContent += "\n❌ SYSTEM ERROR\n";
  } finally {
    isRunning = false;
  }
}

// ===================================
// ENTER KEY SUPPORT
// ===================================
inputEl.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMission();
  }
});

// ===================================
// MATRIX BACKGROUND
// ===================================
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

const chars = "01FTM2077ΩΔ";
const drops = Array(Math.floor(canvas.width / 20)).fill(1);

function drawMatrix() {
  ctx.fillStyle = "rgba(0,0,0,0.05)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#00ff00";
  ctx.font = "15px monospace";

  drops.forEach((y, i) => {
    const t = chars[Math.random() * chars.length | 0];
    ctx.fillText(t, i * 20, y * 20);

    if (y * 20 > canvas.height && Math.random() > 0.975) {
      drops[i] = 0;
    }
    drops[i]++;
  });

  requestAnimationFrame(drawMatrix);
}
drawMatrix();

// ===================================
// VISUAL FEEDBACK (VOICE)
// ===================================
voicePlayer.onplay = () =>
  document.body.classList.add("speaking");

voicePlayer.onended = () =>
  document.body.classList.remove("speaking");

// ===================================
// READY
// ===================================
console.log("🟢 FTM-2077 CORE JS LOADED");
