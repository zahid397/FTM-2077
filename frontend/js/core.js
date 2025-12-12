const API = "https://ftm-2077.onrender.com/api"; // 🔥 তোমার backend

async function sendMission() {
  const cmd = document.getElementById("cmd").value;
  const output = document.getElementById("output");
  const player = document.getElementById("voicePlayer");

  output.textContent = "Processing...";

  try {
    const res = await fetch(`${API}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command: cmd,
        persona: "JARVIS"
      })
    });

    const data = await res.json();
    output.textContent = JSON.stringify(data, null, 2);

    // 🔊 PLAY VOICE IF EXISTS
    if (data.audio) {
      player.src = "https://ftm-2077.onrender.com" + data.audio;
      player.style.display = "block";
      player.play().catch(() => {
        console.log("User interaction required for audio");
      });
    }

  } catch (err) {
    output.textContent = "Backend unreachable ❌";
  }
}
