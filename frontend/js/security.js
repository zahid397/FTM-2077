function unlockSystem() {
    const key = document.getElementById("godKey").value.trim();

    // HARD CODED GOD KEY (frontend gate only)
    if (key === "OMEGA-777") {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("system-ui").style.display = "block";

        if (typeof bootFace === "function") bootFace();
    } else {
        alert("❌ Invalid Access Key");
    }
}
