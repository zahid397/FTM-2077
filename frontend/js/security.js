async function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();
    if (!key) return alert("OMEGA-777");

    try {
        // LOGIN
        const res = await fetch(`${window.BACKEND}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: key })
        });

        const data = await res.json();

        if (data.status !== "SUCCESS") {
            alert("ACCESS DENIED");
            return;
        }

        // GOD MODE
        await fetch(`${window.BACKEND}/api/godmode?key=${encodeURIComponent(key)}`, {
            method: "POST"
        });

        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";

        bootFace();

    } catch (e) {
        console.error(e);
        alert("Backend unreachable");
    }
}
