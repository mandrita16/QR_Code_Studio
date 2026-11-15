
// ========================================
// QR STUDIO — 3D INTERACTION ENGINE
// ========================================

const cube = document.getElementById("qrCube");

const pauseBtn = document.getElementById("pauseBtn");
const pauseIcon = document.getElementById("pauseIcon");
const pauseText = document.getElementById("pauseText");

const rotateLeft = document.getElementById("rotateLeft");
const rotateRight = document.getElementById("rotateRight");
const resetCube = document.getElementById("resetCube");

let paused = false;
let manualRotation = false;
let rotationY = 0;
let rotationX = -12;


// PAUSE / RESUME AUTO ROTATION

pauseBtn.addEventListener("click", () => {

    paused = !paused;

    cube.classList.toggle("paused", paused);

    pauseIcon.textContent = paused ? "▶" : "Ⅱ";
    pauseText.textContent = paused ? "RESUME" : "PAUSE";

});


// MANUAL ROTATION

function applyManualRotation() {

    manualRotation = true;
    paused = true;

    cube.classList.add("paused");
    cube.classList.add("manual");

    pauseIcon.textContent = "▶";
    pauseText.textContent = "RESUME";

    cube.style.transform =
        `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`;

}


rotateLeft.addEventListener("click", () => {

    rotationY -= 45;
    applyManualRotation();

});


rotateRight.addEventListener("click", () => {

    rotationY += 45;
    applyManualRotation();

});


// RESET

resetCube.addEventListener("click", () => {

    rotationY = 0;
    rotationX = -12;

    manualRotation = false;
    paused = false;

    cube.classList.remove("paused");
    cube.classList.remove("manual");

    cube.style.transform = "";

    pauseIcon.textContent = "Ⅱ";
    pauseText.textContent = "PAUSE";

});


// COLOR PRESETS

const fillPicker = document.getElementById("fill_color");
const backPicker = document.getElementById("back_color");

const presets = document.querySelectorAll(".preset");

presets.forEach(preset => {

    preset.addEventListener("click", () => {

        fillPicker.value = preset.dataset.fill;
        backPicker.value = preset.dataset.back;

        presets.forEach(p => p.classList.remove("active"));

        preset.classList.add("active");

    });

});


// CHARACTER COUNTER

const textarea = document.getElementById("data");
const charCount = document.getElementById("charCount");

function updateCounter() {

    charCount.textContent =
        `${textarea.value.length} / 2000`;

}

textarea.addEventListener("input", updateCounter);

updateCounter();


// TOUCH / MOUSE DRAG ROTATION

let dragging = false;
let startX = 0;
let startY = 0;

const scene = document.querySelector(".scene");

scene.addEventListener("pointerdown", (event) => {

    if (event.target.closest("button")) return;

    dragging = true;

    startX = event.clientX;
    startY = event.clientY;

    scene.setPointerCapture(event.pointerId);

});

scene.addEventListener("pointermove", (event) => {

    if (!dragging) return;

    const deltaX = event.clientX - startX;
    const deltaY = event.clientY - startY;

    rotationY += deltaX * 0.6;
    rotationX -= deltaY * 0.5;

    rotationX = Math.max(-75, Math.min(75, rotationX));

    startX = event.clientX;
    startY = event.clientY;

    applyManualRotation();

});

scene.addEventListener("pointerup", () => {

    dragging = false;

});

scene.addEventListener("pointercancel", () => {

    dragging = false;

});

