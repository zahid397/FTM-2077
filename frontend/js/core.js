// =======================================
// FTM-2077 :: CORE FRONTEND ENGINE (FINAL)
// =======================================

// 🔗 BACKEND BASE URL (Render)
const API = "https://ftm-2077.onrender.com";

// -------------------------------
// DOM ELEMENTS
// -------------------------------
const inputEl = document.getElementById("missionInput");
const outputEl = document.getElementById("missionOutput");
const executeBtn = document.getElementById("executeBtn");

// -------------------------------
// MAIN FUNCTION
// -------------------------------
async function sendMission() {
    if (!inputEl || !outputEl) return;

    const text = inputEl.value.trim();
    if (!text) {
        outputEl.innerText = "⚠️ No command entered.";
        return;
    }

    outputEl.innerText = "⏳ Processing mission...\n";

    try {
        const res = await fetch(`${API}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: text,          // ✅ REQUIRED BY BACKEND
                persona: "JARVIS"       // ✅ DEFAULT PERSONA
            })
        });

        if (!res.ok) {
            const err = await res.text();
            throw new Error(err || "Request failed");
        }

        const data = await res.json();

        // Pretty output
        outputEl.innerText = formatOutput(data);

        // 🔊 AUTO PLAY AUDIO (if available)
        if (data.audio) {
            const audio = new Audio(`${API}${data.audio}`);
            audio.play().catch(() => {
                console.warn("Audio autoplay blocked by browser");
            });
        }

    } catch (err) {
        outputEl.innerText =
            "❌ ERROR: Unable to reach backend.\n\n" +
            err.message;
    }
}

// -------------------------------
// OUTPUT FORMATTER
// -------------------------------
function formatOutput(data) {
    if (!data || typeof data !== "object") {
        return String(data);
    }

    if (data.detail) {
        return "⚠️ " + JSON.stringify(data.detail, null, 2);
    }

    let result = "";

    if (data.status) result += `STATUS: ${data.status}\n`;
    if (data.persona) result += `PERSONA: ${data.persona}\n`;
    if (data.command) result += `COMMAND: ${data.command}\n`;
    if (data.probability !== undefined)
        result += `PROBABILITY: ${data.probability}%\n\n`;

    if (data.analysis) {
        result += "ANALYSIS:\n";
        result += data.analysis + "\n\n";
    }

    if (data.audio) {
        result += "🔊 Voice response generated.\n";
    }

    return result || JSON.stringify(data, null, 2);
}

// -------------------------------
// EVENT BINDINGS
// -------------------------------
if (executeBtn) {
    executeBtn.addEventListener("click", sendMission);
}

// Enter key support
if (inputEl) {
    inputEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMission();
        }
    });
}

// -------------------------------
// SYSTEM BOOT LOG
// -------------------------------
console.log("🟢 FTM-2077 FRONTEND CORE ONLINE");
