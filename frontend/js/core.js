const API = "https://ftm-2077.onrender.com/api";

let audioUnlocked = false;
let audioPlayer = null;

function initAudioUnlock() {
    if (!audioPlayer) {
        audioPlayer = document.createElement("audio");
        audioPlayer.style.display = "none";
        document.body.appendChild(audioPlayer);
    }

    // user interaction unlock
    audioPlayer.play().then(() => {
        audioUnlocked = true;
    }).catch(() => {
        audioUnlocked = false;
    });
}

async function sendMission() {
    initAudioUnlock();

    const text = document.getElementById("missionInput").value.trim();
    if (!text) return;

    document.getElementById("missionOutput").innerText = "Processing...";

    try {
        const res = await fetch(`${API}/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        const data = await res.json();
        document.getElementById("missionOutput").innerText =
            JSON.stringify(data, null, 2);

        // 🔊 PLAY AUDIO
        if (data.audio && audioUnlocked) {
            audioPlayer.src = `${API.replace("/api", "")}${data.audio}`;
            audioPlayer.load();
            audioPlayer.play().catch(() => {
                alert("Tap EXECUTE again to enable voice 🔊");
            });
        }

    } catch (err) {
        document.getElementById("missionOutput").innerText =
            "ERROR: Backend unreachable.";
    }
}
