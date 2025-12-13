async function sendMission() {
    const input = document.getElementById("missionInput");
    const output = document.getElementById("missionOutput");
    const scrollBox = document.getElementById("scrollBox");

    const text = input.value.trim();
    if (!text) return;

    output.textContent += `\n\n> ${text}\n`;
    input.value = "";
    scrollBox.scrollTop = scrollBox.scrollHeight;

    try {
        const res = await fetch("https://ftm-2077.onrender.com/api/execute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        const data = await res.json();

        // 🔥 ONLY SHOW TEXT (NO JSON)
        await typeText(output, data.text, 18);

        scrollBox.scrollTop = scrollBox.scrollHeight;

        // 🔊 AUTO LOAD VOICE
        if (data.audio) {
            voicePlayer.src = data.audio.startsWith("http")
                ? data.audio
                : `https://ftm-2077.onrender.com${data.audio}`;
        }

    } catch (err) {
        output.textContent += "\n❌ SYSTEM ERROR\n";
    }
}
