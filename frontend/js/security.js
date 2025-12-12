const BACKEND = "https://ftm-2077.onrender.com"; // তোমার backend URL

async function unlockSystem() {
    const key = document.getElementById("godKey").value;

    if (!key.trim()) {
        alert("Enter access key");
        return;
    }

    try {
        const res = await fetch(`${BACKEND}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: key })
        });

        const data = await res.json();

        if (data.status === "SUCCESS") {
            document.getElementById("login-screen").style.display = "none";
            document.getElementById("system-ui").style.display = "block";

            bootFace(); // AI face init
        } else {
            alert("ACCESS DENIED");
        }

    } catch (err) {
        alert("Backend unreachable");
    }
}
