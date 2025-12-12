// ================================
// CONFIG
// ================================
const API = "https://ftm-2077.onrender.com"; 
// 🔧 backend root ( /api নিজে যোগ হবে )

// ================================
// AUDIO SETUP (GLOBAL)
// ================================
const voicePlayer = document.getElementById("voicePlayer");
let audioUnlocked = false;

voicePlayer.preload = "auto";
voicePlayer.setAttribute("playsinline", "true"); // 🔧 iOS fix

// 🔓 HARD AUDIO UNLOCK (Mobile fix)
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

// User interaction needed once
document.addEventListener("click", unlockAudio, { once: true });
document.addEventListener("touchstart", unlockAudio, { once: true });

// ================================
// UNLOCK SYSTEM (UI ONLY)
// ================================
function unlockSystem() {
    const keyInput = document.getElementById("godKey");
    const key = keyInput.value.trim();

    if (!key) {
        alert("Enter access key");
        return;
    }

    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "flex";

        if (typeof bootFace === "function") bootFace();
        unlockAudio(); // 🔧 ensure audio ready
        return;
    }

    alert("Invalid Key");
    keyInput.value = "";
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
            throw new Error("Server error");
        }

        const data = await res.json();

        // ----------------
        // SHOW OUTPUT
        // ----------------
        output.textContent += `\n\n${JSON.stringify(data, null, 2)}`;
        scrollBox.scrollTop = scrollBox.scrollHeight;

        // ----------------
        // PLAY VOICE
        // ----------------
        if (data.audio) {
            const audioUrl = data.audio.startsWith("http")
                ? data.audio
                : `${API}${data.audio}`;

            console.log("🎧 Playing:", audioUrl);

            voicePlayer.pause();
            voicePlayer.src = audioUrl;
            voicePlayer.load();

            voicePlayer.play().catch(() => {
                output.textContent += "\n[Tap screen to hear audio]";
            });
        }

    } catch (err) {
        console.error(err);
        output.textContent += "\n❌ ERROR: Backend unreachable";
    }
}
