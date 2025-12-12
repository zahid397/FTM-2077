// ================================
// FTM-2077 OMEGA :: CORE ENGINE
// ================================

// 🔗 BACKEND BASE URL (Render)
const API_BASE = "https://ftm-2077.onrender.com";

// ================================
// DOM ELEMENTS
// ================================
const inputEl = document.getElementById("missionInput");
const outputEl = document.getElementById("missionOutput");
const executeBtn = document.getElementById("executeBtn");

// ================================
// MAIN EXECUTION FUNCTION
// ================================
async function sendMission() {
    const command = inputEl.value.trim();

    if (!command) {
        outputEl.innerText = "⚠️ No command entered.";
        return;
    }

    // UI feedback
    outputEl.innerText = "⏳ Processing mission...\n";

    try {
        const res = await fetch(`${API_BASE}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command   // 🔥 backend expects THIS
            })
        });

        if (!res.ok) {
            const errText = await res.text();
            throw new Error(errText || "Request failed");
        }

        const data = await res.json();

        // Pretty print output
        outputEl.innerText = formatOutput(data);

    } catch (err) {
        outputEl.innerText =
            "❌ ERROR: Unable to reach backend.\n\n" +
            err.message;
    }
}

// ================================
// OUTPUT FORMATTER
// ================================
function formatOutput(data) {
    if (typeof data === "string") {
        return data;
    }

    if (data.detail) {
        return "⚠️ " + JSON.stringify(data.detail, null, 2);
    }

    return JSON.stringify(data, null, 2);
}

// ================================
// EVENT BINDINGS
// ================================
if (executeBtn) {
    executeBtn.addEventListener("click", sendMission);
}

// Enter key support
if (inputEl) {
    inputEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMission();
        }
    });
}

// ================================
// SYSTEM BOOT MESSAGE
// ================================
console.log("🟢 FTM-2077 CORE ONLINE");
