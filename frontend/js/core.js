// 🔗 BACKEND ROUTE (Render Production URL)
const API = "https://ftm-2077.onrender.com/api";

async function sendMission() {
    let text = document.getElementById("missionInput").value;
    if (!text.trim()) return;

    document.getElementById("missionOutput").innerText = "Processing...";

    try {
        const res = await fetch(`${API}/process_mission`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: text })
        });

        const data = await res.json();
        document.getElementById("missionOutput").innerText =
            JSON.stringify(data, null, 2);

    } catch (err) {
        document.getElementById("missionOutput").innerText =
            "ERROR: Unable to reach backend.";
    }
}
