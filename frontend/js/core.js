const API = "https://ftm-2077.onrender.com";

async function sendMission() {
    const text = document.getElementById("missionInput").value.trim();
    if (!text) return;

    document.getElementById("missionOutput").innerText = "Processing...";

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
            throw new Error("Server error");
        }

        const data = await res.json();
        document.getElementById("missionOutput").innerText =
            JSON.stringify(data, null, 2);

        // 🔊 Audio auto-play (if exists)
        if (data.audio) {
            const audio = new Audio(`${API}${data.audio}`);
            audio.play();
        }

    } catch (err) {
        document.getElementById("missionOutput").innerText =
            "ERROR: Backend unreachable";
        console.error(err);
    }
}
