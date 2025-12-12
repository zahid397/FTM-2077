// ===============================
// FTM-2077 :: CORE INTERFACE
// ===============================

// 🔗 BACKEND BASE URL (Render)
const API_BASE = "https://ftm-2077.onrender.com";

// 🎭 Default Persona
let ACTIVE_PERSONA = "JARVIS";

// -------------------------------
// SEND MISSION TO BACKEND
// -------------------------------
async function sendMission() {
    const input = document.getElementById("missionInput");
    const output = document.getElementById("missionOutput");

    const command = input.value.trim();
    if (!command) {
        output.innerText = "⚠️ No command entered.";
        return;
    }

    output.innerText = "⏳ Processing...";
    input.value = "";

    try {
        const res = await fetch(`${API_BASE}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command,
                persona: ACTIVE_PERSONA
            })
        });

        if (!res.ok) {
            throw new Error("Backend error");
        }

        const data = await res.json();

        // 🧠 Show analysis
        let display = "";
        display += `STATUS      : ${data.status}\n`;
        display += `PERSONA     : ${data.persona}\n`;
        display += `COMMAND     : ${data.command}\n\n`;
        display += `ANALYSIS:\n${data.analysis || "No analysis"}\n\n`;
        display += `PROBABILITY : ${data.probability || 0}%\n`;

        // 🔊 Audio info
        if (data.audio) {
            display += `\nAUDIO FILE  : ${data.audio}\n`;
            playVoice(data.audio);
        }

        output.innerText = display;

    } catch (err) {
        console.error(err);
        output.innerText = "❌ Backend unreachable or error occurred.";
        alert("Backend unreachable");
    }
}

// -------------------------------
// PLAY GENERATED VOICE
// -------------------------------
function playVoice(path) {
    try {
        const audio = new Audio(`${API_BASE}${path}`);
        audio.play();
    } catch (e) {
        console.warn("Audio playback failed", e);
    }
}

// -------------------------------
// PERSONA SWITCH (OPTIONAL)
// -------------------------------
function setPersona(p) {
    ACTIVE_PERSONA = p.toUpperCase();
    document.getElementById("missionOutput").innerText =
        `Persona switched to ${ACTIVE_PERSONA}`;
}

// -------------------------------
// SYSTEM BOOT CONFIRM
// -------------------------------
console.log("🟢 FTM-2077 CORE LOADED");
