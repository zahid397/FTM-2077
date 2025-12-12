async function unlockSystem() {
    const key = document.getElementById("godKey").value;

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
            bootFace();
        } else {
            alert("ACCESS DENIED");
        }
    } catch (e) {
        alert("Backend unreachable");
        console.error(e);
    }
}
