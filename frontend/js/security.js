const API = "https://ftm-2077.onrender.com";

async function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();
    if (!key) {
        alert("Enter key");
        return;
    }

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: key
            })
        });

        if (!res.ok) {
            throw new Error("HTTP error");
        }

        const data = await res.json();

        console.log("LOGIN RESPONSE:", data); // 👈 DEBUG

        if (data.status === "SUCCESS") {
            document.getElementById("login-screen").style.display = "none";
            document.getElementById("system-ui").style.display = "block";
            bootFace();
        } else {
            alert("Invalid Key");
        }

    } catch (err) {
        console.error(err);
        alert("Backend unreachable");
    }
}
