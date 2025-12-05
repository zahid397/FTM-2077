function unlockSystem() {
    const key = document.getElementById("godKey").value;

    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";
        bootFace();
    } else {
        alert("Invalid Key");
    }
}
