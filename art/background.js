const canvas = document.getElementById("backgroundCanvas")
const ctx = canvas.getContext("2d")

var scrollOffset = 0
function drawImages() {
    ctx.filter = "brightness(90%)"
    ctx.drawImage(layer3, 0, (scrollOffset*0.5)-80, canvas.width, canvas.width)
    ctx.filter = "brightness(100%)"
    ctx.drawImage(layer2, 0, scrollOffset*0.6, canvas.width, canvas.width)
    ctx.drawImage(layer1, 0, scrollOffset*0.7, canvas.width, canvas.width)
    ctx.fillStyle = '#396844'
    const lastImageY = scrollOffset * 0.7;
    ctx.fillRect(0, lastImageY + canvas.width, canvas.width, 900);
    ctx.save()
    ctx.filter = "brightness(0%) opacity(20%)"
    var shadowLength = 1.5
    ctx.translate(0, lastImageY+canvas.width*(2))
    ctx.scale(1,-1)
    ctx.drawImage(layer1, 0, 0, canvas.width,canvas.width*(1))
    ctx.restore()
}

window.addEventListener('scroll', () => {
    scrollOffset = (-scrollY)+500
    ctx.clearRect(0,0,canvas.width, canvas.height)
    drawImages()
})
function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * 4 * dpr; // 5x the viewport height
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = (window.innerHeight*4) + 'px';
    ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform before drawing
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();




ctx.imageSmoothingEnabled = false
// draw images on load
var layer1 = new Image()
var layer2 = new Image()
var layer3 = new Image()
layer1.src = './bg/main.png'
layer2.src = './bg/l1.png'
layer3.src = './bg/l2.png'
layer3.onload = () => {
    drawImages()
}



