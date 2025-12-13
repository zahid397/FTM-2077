// ================================
// CONFIG
// ================================
const API = "https://ftm-2077.onrender.com"; // backend root

// ================================
// AUDIO SETUP (GLOBAL)
// ================================
const voicePlayer = document.getElementById("voicePlayer");
let audioUnlocked = false;

voicePlayer.preload = "auto";
voicePlayer.setAttribute("playsinline", "true"); // iOS fix

// 🔓 HARD AUDIO UNLOCK (Mobile-safe)
function unlockAudio() {
    if (audioUnlocked) return;
    audioUnlocked = true;

    const silentWav =
        "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=";

    try {
        voicePlayer.src = silentWav;
        voicePlayer.load();
        voicePlayer.play().then(() => {
            voicePlayer.pause();
            voicePlayer.currentTime = 0;
            console.log("🔊 Audio unlocked");
        });
    } catch (_) {}
}

// user interaction (only once)
["click", "touchstart"].forEach(evt =>
    document.addEventListener(evt, unlockAudio, { once: true })
);

// ================================
// UNLOCK SYSTEM (UI ONLY)
// ================================
function unlockSystem() {
    const keyInput = document.getElementById("godKey");
    const key = keyInput.value.trim();

    if (!key) {
        alert("⚠️ Enter access key");
        return;
    }

    // ⚠️ better than hardcoding everywhere
    const VALID_KEY = "OMEGA-777";

    if (key !== VALID_KEY) {
        alert("❌ Invalid Key");
        keyInput.value = "";
        return;
    }

    document.getElementById("login-screen").style.display = "none";
    document.getElementById("system-ui").style.display = "flex";

    unlockAudio();
    if (typeof bootFace === "function") bootFace();
}

// ================================
// SEND MISSION
// ================================
async function sendMission() {
    const input = document.getElementById("missionInput");
    const output = document.getElementById("missionOutput");
    const scrollBox = document.getElementById("scrollBox");

    const text = input.value.trim();
    if (!text) return;

    output.textContent += `\n\n> ${text}`;
    input.value = "";
    scrollBox.scrollTop = scrollBox.scrollHeight;

    try {
        const res = await fetch(`${API}/api/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();

        // ----------------
        // TEXT OUTPUT
        // ----------------
        if (data.text) {
            output.textContent += `\n\n${data.text}`;
        } else {
            output.textContent += `\n\n${JSON.stringify(data, null, 2)}`;
        }

        scrollBox.scrollTop = scrollBox.scrollHeight;

        // ----------------
        // VOICE OUTPUT
        // ----------------
        if (data.audio) {
            const audioUrl = data.audio.startsWith("http")
                ? data.audio
                : `${API}${data.audio}`;

            console.log("🎧 Playing:", audioUrl);

            voicePlayer.pause();
            voicePlayer.currentTime = 0;
            voicePlayer.src = audioUrl;
            voicePlayer.load();

            voicePlayer.play().catch(() => {
                output.textContent += "\n🔊 Tap anywhere to enable audio";
            });
        }

    } catch (err) {
        console.error("❌ Mission error:", err);
        output.textContent += "\n❌ ERROR: Backend unreachable or failed";
    }
}
