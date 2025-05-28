const bgCanvas = document.getElementById('backgroundCanvas');
const bgCtx = bgCanvas.getContext('2d');
let diamonds = []; // Store all diamond info

function resizeBgCanvas() {
    const dpr = window.devicePixelRatio || 1;
    bgCanvas.width = window.innerWidth * dpr;
    bgCanvas.height = window.innerHeight * dpr;
    bgCanvas.style.width = window.innerWidth + 'px';
    bgCanvas.style.height = window.innerHeight + 'px';
    bgCtx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform before drawing
    drawIsoPattern();
}
resizeBgCanvas();
window.addEventListener('resize', resizeBgCanvas);

function drawIsoPattern() {
    diamonds = []; // Reset the list each time you redraw
    const dpr = window.devicePixelRatio || 1;
    const width = bgCanvas.width;
    const height = bgCanvas.height*2;
    const tileWidth = 80 * dpr;
    const tileHeight = 40 * dpr;

    bgCtx.clearRect(0, 0, width, height);
    bgCtx.strokeStyle = "rgba(255,255,255,0.15)";
    bgCtx.lineWidth = 2 * dpr;

    for (let y = 0; y < height + tileHeight; y += tileHeight) {
        for (let x = 0; x < width + tileWidth; x += tileWidth) {
            drawDiamond(x, y, tileWidth, tileHeight);
            // Add each diamond's info to the list
            diamonds.push({
                x: x,
                y: y,
                width: tileWidth,
                height: tileHeight,
                // Add more properties as needed, e.g. value: null
            });
        }
    }
}

function drawDiamond(cx, cy, w, h) {
    bgCtx.beginPath();
    bgCtx.moveTo(cx, cy + h / 2);         // left
    bgCtx.lineTo(cx + w / 2, cy);         // top
    bgCtx.lineTo(cx + w, cy + h / 2);     // right
    bgCtx.lineTo(cx + w / 2, cy + h);     // bottom
    bgCtx.closePath();
    bgCtx.stroke();
}

window.addEventListener('scroll', () => {
    const scrollY = window.scrollY || window.pageYOffset;
    bgCtx.setTransform(1, 0, 0, 1, 0, -(scrollY*0.2));
    bgCtx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);
    drawIsoPattern();
});