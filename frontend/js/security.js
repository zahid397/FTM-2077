const API_BASE = "https://ftm-2077.onrender.com";

async function unlockSystem() {
    const key = document.getElementById("godKey").value;

    if (!key) {
        alert("Enter key");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: key })
        });

        if (!res.ok) throw new Error("Login failed");

        const data = await res.json();

        if (data.status === "SUCCESS") {
            document.getElementById("login-screen").style.display = "none";
            document.getElementById("system-ui").style.display = "block";

            if (typeof bootFace === "function") bootFace();
        } else {
            alert("❌ Invalid Key");
        }

    } catch (e) {
        alert("❌ Backend unreachable");
    }
}
