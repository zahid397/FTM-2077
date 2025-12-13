// ================================
// CONFIG
// ================================
const API = "https://ftm-2077.onrender.com";

// ================================
// AUDIO SETUP (GLOBAL)
// ================================
const voicePlayer = document.getElementById("voicePlayer");
let audioUnlocked = false;

voicePlayer.preload = "auto";
voicePlayer.setAttribute("playsinline", "true"); // iOS fix

// 🔓 Mobile audio unlock
function unlockAudio() {
    if (audioUnlocked) return;
    audioUnlocked = true;

    const silentWav =
        "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=";

    voicePlayer.src = silentWav;
    voicePlayer.load();

    voicePlayer.play()
        .then(() => {
            voicePlayer.pause();
            voicePlayer.currentTime = 0;
            console.log("🔊 Audio unlocked");
        })
        .catch(() => {});
}

// one-time user interaction
document.addEventListener("click", unlockAudio, { once: true });
document.addEventListener("touchstart", unlockAudio, { once: true });

// ================================
// TYPING EFFECT
// ================================
function typeText(target, text, speed = 18) {
    return new Promise(resolve => {
        let i = 0;

        function type() {
            if (i < text.length) {
                target.textContent += text.charAt(i);
                i++;
                target.parentElement.scrollTop =
                    target.parentElement.scrollHeight;
                setTimeout(type, speed);
            } else {
                resolve();
            }
        }

        type();
    });
}

// ================================
// PLAY VOICE
// ================================
function playVoice() {
    if (!voicePlayer.src) return;
    voicePlayer.currentTime = 0;
    voicePlayer.play().catch(() => {
        alert("Tap screen once to enable audio");
    });
}

// ================================
// SEND MISSION (MAIN)
// ================================
async function sendMission() {
    const input = document.getElementById("missionInput");
    const output = document.getElementById("missionOutput");
    const scrollBox = document.getElementById("scrollBox");

    const text = input.value.trim();
    if (!text) return;

    // show user command
    output.textContent += `\n\n> ${text}\n`;
    input.value = "";
    scrollBox.scrollTop = scrollBox.scrollHeight;

    try {
        const res = await fetch(`${API}/api/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                command: text,
                persona: "JARVIS"
            })
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();

        // ----------------
        // SHOW TEXT (NO JSON)
        // ----------------
        if (data.text) {
            await typeText(output, data.text, 18);
        } else {
            await typeText(output, "[No response text]", 18);
        }

        scrollBox.scrollTop = scrollBox.scrollHeight;

        // ----------------
        // LOAD VOICE (OPTIONAL)
        // ----------------
        if (data.audio) {
            const audioUrl = data.audio.startsWith("http")
                ? data.audio
                : `${API}${data.audio}`;

            voicePlayer.pause();
            voicePlayer.currentTime = 0;
            voicePlayer.src = audioUrl;
            voicePlayer.load();
        }

    } catch (err) {
        console.error(err);
        output.textContent += "\n❌ SYSTEM ERROR\n";
    }
}

// ================================
// ENTER KEY SUPPORT
// ================================
document.getElementById("missionInput")?.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMission();
    }
});
