// ================================
// CONFIG
// ================================
const API_BASE = "https://ftm-2077.onrender.com"; 
// ⚠️ backend root URL — ঠিক আছে যেটা তুই screenshot এ দেখাইছিস

// ================================
// UNLOCK SYSTEM
// ================================
function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();

    if (!key) {
        alert("Enter access key");
        return;
    }

    // Frontend-only unlock (visual)
    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";

        if (typeof bootFace === "function") {
            bootFace();
        }

        return;
    }

    alert("Invalid Key");
}

// ================================
// AUDIO PLAYER (MOBILE SAFE)
// ================================
function playVoice(audioUrl) {
    if (!audioUrl) return;

    try {
        const audio = new Audio(audioUrl);
        audio.volume = 1.0;

        audio.play().catch(err => {
            console.warn("Audio autoplay blocked:", err);
        });
    } catch (e) {
        console.error("Audio error:", e);
    }
}

// ================================
// SEND MISSION
// ================================
async function sendMission() {
    const inputEl = document.getElementById("missionInput");
    const outputEl = document.getElementById("missionOutput");

    const command = inputEl.value.trim();
    if (!command) return;

    outputEl.textContent = "Processing...\n";

    try {
        const res = await fetch(`${API_BASE}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command,
                persona: "JARVIS"
            })
        });

        if (!res.ok) {
            throw new Error("Backend unreachable");
        }

        const data = await res.json();

        // Pretty output
        let text = "";
        if (data.status) text += `STATUS       : ${data.status}\n`;
        if (data.persona) text += `PERSONA      : ${data.persona}\n`;
        if (data.command) text += `COMMAND      : ${data.command}\n\n`;

        if (data.analysis) {
            text += `ANALYSIS:\n${data.analysis}\n\n`;
        }

        if (data.probability !== undefined) {
            text += `PROBABILITY  : ${data.probability}%\n`;
        }

        if (data.audio) {
            text += `AUDIO FILE   : ${data.audio}\n`;
        }

        outputEl.textContent = text || JSON.stringify(data, null, 2);

        // 🔊 PLAY VOICE
        if (data.audio) {
            playVoice(data.audio);
        }

    } catch (err) {
        console.error(err);
        alert("Backend unreachable");
    }
}

// ================================
// ENTER KEY SUPPORT
// ================================
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("missionInput");

    if (input) {
        input.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMission();
            }
        });
    }
});
