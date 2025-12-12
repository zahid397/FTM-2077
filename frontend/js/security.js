// ================================
// SECURITY CORE :: FTM-2077
// ================================

const API = "https://ftm-2077.onrender.com";

async function unlockSystem() {
    const keyInput = document.getElementById("godKey");
    if (!keyInput) return;

    const key = keyInput.value.trim();
    if (!key) {
        alert("Enter access key");
        return;
    }

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: key })
        });

        const data = await res.json();

        if (data.status === "SUCCESS") {
            // UI unlock
            document.getElementById("login-screen").style.display = "none";
            document.getElementById("system-ui").style.display = "block";

            // Visual boot
            if (typeof bootFace === "function") bootFace();
            if (typeof matrixIdleMode === "function") matrixIdleMode();

        } else {
            alert("❌ Invalid access key");
        }

    } catch (err) {
        alert("⚠️ Backend not reachable");
    }
}
