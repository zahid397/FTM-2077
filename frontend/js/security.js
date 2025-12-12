const API = "https://ftm-2077.onrender.com";

async function unlockSystem() {
    const key = document.getElementById("godKey").value;

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: key })
        });

        const data = await res.json();

        if (data.status === "SUCCESS") {
            document.getElementById("login-screen").style.display = "none";
            document.getElementById("system-ui").style.display = "block";
            bootFace();
        } else {
            alert("Invalid Key");
        }

    } catch (e) {
        alert("Backend unreachable");
    }
}
