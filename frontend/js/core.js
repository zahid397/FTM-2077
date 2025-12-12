// ===== BACKEND BASE URL =====
window.BACKEND = "https://ftm-2077.onrender.com";

// ===== CORE EXECUTE =====
async function sendMission() {
    const text = document.getElementById("missionInput").value.trim();
    if (!text) return;

    document.getElementById("missionOutput").innerText = "Processing...";

    try {
        const res = await fetch(`${window.BACKEND}/api/execute`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        const data = await res.json();
        document.getElementById("missionOutput").innerText =
            JSON.stringify(data, null, 2);

        // 🔊 Auto play audio if exists
        if (data.audio) {
            new Audio(window.BACKEND + data.audio).play();
        }

    } catch (e) {
        console.error(e);
        alert("Backend unreachable");
    }
}
