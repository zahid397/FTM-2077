// 🔗 BACKEND BASE URL (RENDER)
const API_BASE = "https://ftm-2077.onrender.com";

// ==========================
// SEND MISSION
// ==========================
async function sendMission() {
    const text = document.getElementById("missionInput").value;
    if (!text.trim()) return;

    document.getElementById("missionOutput").innerText = "Processing...";

    try {
        const res = await fetch(`${API_BASE}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        document.getElementById("missionOutput").innerText =
            JSON.stringify(data, null, 2);

        // 🔊 Play voice if exists
        if (data.audio) {
            const audio = new Audio(`${API_BASE}${data.audio}`);
            audio.play();
        }

    } catch (err) {
        document.getElementById("missionOutput").innerText =
            "❌ Backend unreachable";
    }
}
