// ================================
// CONFIG
// ================================
const API = "https://ftm-2077.onrender.com"; 
// ⚠️ Backend root URL

// ================================
// AUDIO SETUP (GLOBAL)
// ================================
const voicePlayer = document.getElementById("voicePlayer");
voicePlayer.preload = "auto";
let audioUnlocked = false;

// 🔓 HARD AUDIO UNLOCK (Mobile Safari / Chrome fix)
function unlockAudio() {
    if (audioUnlocked) return;
    audioUnlocked = true;

    // 1-frame silent WAV (base64)
    const silentWav =
        "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=";

    voicePlayer.src = silentWav;
    voicePlayer.load();
    voicePlayer.play()
        .then(() => {
            voicePlayer.pause();
            voicePlayer.currentTime = 0;
        })
        .catch(() => {});
}

// Unlock audio on first user interaction
document.addEventListener("click", unlockAudio, { once: true });
document.addEventListener("touchstart", unlockAudio, { once: true });

// ================================
// UNLOCK SYSTEM (UI ONLY)
// ================================
function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();

    if (!key) {
        alert("Enter access key");
        return;
    }

    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";
        if (typeof bootFace === "function") bootFace();
        return;
    }

    alert("Invalid Key");
}

// ================================
// SEND MISSION
// ================================
async function sendMission() {
    const input = document.getElementById("missionInput");
    const output = document.getElementById("missionOutput");

    const text = input.value.trim();
    if (!text) return;

    output.textContent = "Processing command...";
    input.value = "";

    try {
        const res = await fetch(`${API}/api/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        if (!res.ok) throw new Error("Backend error");

        const data = await res.json();

        // ----------------
        // SHOW OUTPUT
        // ----------------
        output.textContent = JSON.stringify(data, null, 2);

        // ----------------
        // PLAY VOICE
        // ----------------
        if (data.audio) {
            const audioUrl = data.audio.startsWith("http")
                ? data.audio
                : `${API}${data.audio}`;

            console.log("Playing audio:", audioUrl);

            voicePlayer.pause();
            voicePlayer.src = audioUrl;
            voicePlayer.load();

            voicePlayer.play().catch(err => {
                console.warn("Autoplay blocked, tap screen once:", err);
            });
        }

    } catch (err) {
        console.error(err);
        output.textContent = "ERROR: Backend unreachable";
        alert("Backend unreachable");
    }
}
