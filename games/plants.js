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
drawFlowerpot();