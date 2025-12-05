function bootFace() {
    const face = document.getElementById("ai-face");
    face.innerHTML = "";

    let blocks = "";
    for (let i = 0; i < 400; i++) blocks += `<div class='pixel'></div>`;
    face.innerHTML = blocks;
}
