// ১. URL গুলো ভেরিয়েবল এ রাখা ভালো
const BASE_URL = "https://ftm-2077.onrender.com"; 
const API_URL = `${BASE_URL}/api`;

async function sendMission() {
  const cmdInput = document.getElementById("cmd");
  const output = document.getElementById("output");
  const player = document.getElementById("voicePlayer");

  const cmd = cmdInput.value.trim();

  // ২. যদি ইনপুট খালি থাকে
  if (!cmd) {
    alert("Please enter a command!");
    return;
  }

  output.textContent = "Processing... ⏳";
  output.style.color = "blue";
  
  // আগের অডিও থাকলে বন্ধ করা
  player.pause();
  player.currentTime = 0;
  player.style.display = "none";

  try {
    // ৩. রিকোয়েস্ট পাঠানো
    const res = await fetch(`${API_URL}/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        command: cmd,
        persona: "JARVIS" // অথবা অন্য কোনো নাম
      })
    });

    if (!res.ok) throw new Error(`Server Error: ${res.status}`);

    const data = await res.json();
    
    // ৪. আউটপুট দেখানো
    output.textContent = JSON.stringify(data, null, 2);
    output.style.color = "green";

    // 🔊 ৫. অডিও প্লে করা (Audio Logic Fix)
    if (data.audio) {
      // যদি অডিও পাথ (Path) হিসেবে আসে, তাহলে বেস URL যোগ করতে হবে
      // আর যদি ফুল URL (http...) আসে, তাহলে সরাসরি বসবে।
      const audioSrc = data.audio.startsWith("http") 
        ? data.audio 
        : `${BASE_URL}${data.audio}`;

      player.src = audioSrc;
      player.style.display = "block";

      // ব্রাউজার পলিসি হ্যান্ডেল করার জন্য try-catch
      try {
        await player.play();
      } catch (playError) {
        console.warn("Autoplay blocked. User interaction needed.");
      }
    } else {
        console.log("No audio received from backend.");
    }

  } catch (err) {
    console.error(err);
    output.textContent = "Backend unreachable or Error ❌";
    output.style.color = "red";
  }
}
