// mspaint game logic
const mscanvas = document.getElementById('mspaint');
const ctx2 = mscanvas.getContext('2d');
const contentDiv = mscanvas.parentElement;
const toolbar = document.getElementById('paint-toolbar');
const colorInput = document.getElementById('paint-color');
const pencilBtn = document.getElementById('tool-pencil');
const eraserBtn = document.getElementById('tool-eraser');
const clearBtn = document.getElementById('tool-clear');

let currentTool = 'pencil';
let currentColor = colorInput.value;
let isDrawing = false;

function resizeCanvasToContent() {
    mscanvas.width = contentDiv.clientWidth- 40;
    mscanvas.height = contentDiv.clientHeight - toolbar.offsetHeight;
    mscanvas.style.marginTop = toolbar.offsetHeight + "px";
    ctx2.fillStyle = "#fff";
    ctx2.fillRect(0, 0, mscanvas.width, mscanvas.height);
}
resizeCanvasToContent();
window.addEventListener('resize', resizeCanvasToContent);

colorInput.addEventListener('input', e => {
    currentColor = e.target.value;
});

function setActiveTool(tool) {
    currentTool = tool;
    pencilBtn.classList.toggle('active-tool', tool === 'pencil');
    eraserBtn.classList.toggle('active-tool', tool === 'eraser');
}
setActiveTool(currentTool);
pencilBtn.addEventListener('click', () => setActiveTool('pencil'));
eraserBtn.addEventListener('click', () => setActiveTool('eraser'));
clearBtn.addEventListener('click', () => {
    ctx2.clearRect(0, 0, mscanvas.width, mscanvas.height);
    ctx2.fillStyle = "#fff";
    ctx2.fillRect(0, 0, mscanvas.width, mscanvas.height);
});

mscanvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    ctx2.beginPath();
    ctx2.moveTo(e.offsetX, e.offsetY);
});
mscanvas.addEventListener('mousemove', function(e) {
    if (!isDrawing) return;
    if (currentTool === 'pencil') {
        ctx2.strokeStyle = currentColor;
        ctx2.lineWidth = 2;
    } else if (currentTool === 'eraser') {
        ctx2.strokeStyle = "#fff";
        ctx2.lineWidth = 10;
    }
    ctx2.lineTo(e.offsetX, e.offsetY);
    ctx2.stroke();
});
mscanvas.addEventListener('mouseup', function(e) {
    isDrawing = false;
    ctx2.closePath();
});
mscanvas.addEventListener('mouseleave', function(e) {
    isDrawing = false;
    ctx2.closePath();
});
mscanvas.addEventListener('click', handleClick);

// Set initial active tool
setActiveTool(currentTool);