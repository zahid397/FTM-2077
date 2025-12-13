// ===================================
// 1. CONFIGURATION
// ===================================
// তোর Render Backend-এর লিংক
const API_URL = "https://ftm-2077.onrender.com/api/execute"; 
const DEFAULT_PERSONA = "JARVIS";

// ===================================
// 2. DOM ELEMENTS
// ===================================
const inputEl = document.getElementById("missionInput");
const outputEl = document.getElementById("missionOutput");

// ===================================
// 3. TYPING EFFECT (MATRIX STYLE)
// ===================================
let isTyping = false;

function typeWriter(text, element, speed = 20) {
    if (isTyping) return; // Prevent overlapping
    isTyping = true;
    element.innerHTML = ""; // Clear previous text
    
    let i = 0;
    function type() {
        if (i < text.length) {
            // Handle newlines
            if (text.substring(i, i + 1) === '\n') {
                element.innerHTML += "<br>";
            } else {
                element.innerHTML += text.charAt(i);
            }
            i++;
            setTimeout(type, speed);
        } else {
            isTyping = false; // Finished typing
        }
    }
    type();
}

// ===================================
// 4. VOICE ENGINE (BROWSER NATIVE)
// ===================================
function speak(text) {
    if (!window.speechSynthesis) return;
    
    // Stop any currently playing audio
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Try to find a cool voice (Google UK Male / Microsoft Hazel)
    const voices = window.speechSynthesis.getVoices();
    const jarvisVoice = voices.find(v => v.name.includes("UK") || v.name.includes("Male")) || voices[0];
    
    if (jarvisVoice) utterance.voice = jarvisVoice;
    
    utterance.pitch = 0.9; // Deep voice
    utterance.rate = 1.1;  // Fast pace
    
    window.speechSynthesis.speak(utterance);
}

// ===================================
// 5. MAIN MISSION LOGIC
// ===================================
async function runMission() {
    const cmd = inputEl.value.trim();
    if (!cmd) return;

    // UI Feedback
    inputEl.value = ""; 
    outputEl.innerHTML = `<span style="color: cyan; animation: blink 1s infinite;">[CONNECTING TO NEURAL NET...]</span>`;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                command: cmd, 
                persona: DEFAULT_PERSONA 
            })
        });

        const data = await response.json();

        if (data.text) {
            // Success: Type text and Speak
            typeWriter(data.text, outputEl);
            speak(data.text);
        } else {
            outputEl.innerHTML = `<span style="color: red;">[ERROR]: EMPTY RESPONSE FROM CORE.</span>`;
        }

    } catch (error) {
        console.error("Connection Error:", error);
        outputEl.innerHTML = `<span style="color: red;">[SYSTEM FAILURE]: CANNOT REACH SERVER.<br>Make sure Backend is running.</span>`;
    }
}

// ===================================
// 6. EVENT LISTENERS
// ===================================
// Allow "Enter" key to submit
inputEl.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        runMission();
    }
});

// Load voices immediately
window.speechSynthesis.onvoiceschanged = () => {
    console.log("🎤 Voice Module Loaded");
};
