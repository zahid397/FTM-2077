// ================================
// CONFIG
// ================================
const API = "https://ftm-2077.onrender.com"; 
// ⚠️ যদি backend URL আলাদা হয়, এখানে শুধু এটা বদলাবি

// ================================
// UNLOCK SYSTEM
// ================================
function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();

    if (!key) {
        alert("Enter access key");
        return;
    }

    // শুধু frontend unlock animation
    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";
        bootFace();
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
    const voicePlayer = document.getElementById("voicePlayer");

    const text = input.value.trim();
    if (!text) return;

    output.textContent = "Processing command...";
    input.value = "";

    try {
        const res = await fetch(`${API}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        if (!res.ok) {
            throw new Error("Backend error");
        }

        const data = await res.json();

        // ================================
        // SHOW OUTPUT
        // ================================
        output.textContent = JSON.stringify(data, null, 2);

        // ================================
        // PLAY VOICE (IMPORTANT PART)
        // ================================
        if (data.audio) {
            const audioUrl = API + data.audio;
            console.log("Playing audio:", audioUrl);

            voicePlayer.pause();
            voicePlayer.src = audioUrl;
            voicePlayer.load();

            // Mobile fix (user interaction already happened)
            voicePlayer.play().catch(err => {
                console.warn("Audio autoplay blocked:", err);
            });
        }

    } catch (err) {
        console.error(err);
        output.textContent = "ERROR: Backend unreachable";
        alert("Backend unreachable");
    }
}
