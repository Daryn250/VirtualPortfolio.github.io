const plantCanvas = document.getElementById('plants');
const plantCtx = plantCanvas.getContext('2d');


function resizeWindow() {
    plantCanvas.width = 200;
    plantCanvas.height = 200;
    plantCtx.imageSmoothingEnabled = false; // Add this line
    plantCtx.drawImage(backgroundImage, 0, 0, 200, 200);
}

window.addEventListener('resize', resizeWindow)



backgroundImage = new Image();
backgroundImage.src = './stardewplant/background1.png';
backgroundImage.onload = () => {
    plantCanvas.width = 200;
    plantCanvas.height = 200;
    plantCtx.imageSmoothingEnabled = false; // Add this line
    plantCtx.drawImage(backgroundImage, 0, 0, 200, 200);
};
resizeWindow();

flowerpot = new Image();
flowerpot.src = './stardewplant/plantpot1.png';
currentGrowth = 1;
flowerpot.onload = () => {
    plantCtx.clearRect(0, 0, plantCanvas.width, plantCanvas.height);
    plantCtx.drawImage(backgroundImage, 0, 0, 200, 200); // Draw the background
    plantCtx.drawImage(flowerpot, 0, 0, 200, 200); // Draw the flowerpot at the center
}
waterButton = new Image();
waterButton.src = './stardewplant/waterButton.png';
waterButton.onload = () => {
    plantCtx.drawImage(waterButton, 110, 10, 50, 50); // Draw the water button at the top left corner
};
function drawWaterButton() {
    plantCtx.drawImage(waterButton, 110, 10, 50, 50); // Draw the water button at the top left corner
}

function drawPlant(growthStage) {
    plantCtx.clearRect(0, 0, plantCanvas.width, plantCanvas.height);
    plantCtx.drawImage(backgroundImage, 0, 0, 200, 200); // Draw the background
    plantCtx.drawImage(flowerpot, 0, 0, 200, 200); // Draw the flowerpot at the center

    const plantImage = new Image();
    plantImage.src = `./stardewplant/plantpot${growthStage}.png`;
    plantImage.onload = () => {
        plantCtx.drawImage(plantImage, 0, 0, 200, 200); // Draw the plant at the center
    };
}
function waterPlant() {
    if (currentGrowth < 4) {
        currentGrowth++;
        drawPlant(currentGrowth);
        drawWaterButton(); // Redraw the water button after watering
    }
}
window.addEventListener('click', (event) => {
    const rect = plantCanvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if the click is within the water button area
    if (x >= 110 && x <= 160 && y >= 10 && y <= 60) {
        waterPlant();
    }
});
// Initial draw of the plant
drawPlant(currentGrowth);
