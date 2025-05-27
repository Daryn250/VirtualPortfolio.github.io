const canvas = document.getElementById('snowCanvas');
const ctx = canvas.getContext('2d');

var snowflakes = [];
const maxSnowflakes = 2000; // Adjust for performance

function createSnowflake() {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: Math.random() * 0.5 - 0.25, // Random horizontal speed
        vy: Math.random() * 1 + 0.5, // Random vertical speed
        size: Math.random() * 3 + 1, // Random radius between 1 and 4
        speed: Math.random() * 1 + 0.5 // Random speed between 0.5 and 1.5
    };
}
function drawSnowflake() {
    snowflakes.forEach(element => {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)'; // Semi-transparent white
        ctx.fillRect(element.x, element.y, element.size, element.size);
    });
}
function updateSnowflake() {
    snowflakes.forEach(element => {
        element.x += element.vx;
        element.y += element.vy;
        
        // Reset snowflake if it goes off screen
        if (element.y > canvas.height) {
            if (snowEnabled) {
            Object.assign(element, createSnowflake());
            }
        }
    });
}
var lightningOnscreen = false;
var lightningFramesLeft = 0;

function drawLightning() {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.lineWidth = 2;
    ctx.beginPath();

    let x = Math.random() * canvas.width;
    let y = 0;
    ctx.moveTo(x, y);

    for (let i = 0; i < 5; i++) {
        x += (Math.random() - 0.5) * 100;
        y += Math.random() * 50 + 20;
        ctx.lineTo(x, y);
    }

    ctx.lineTo(x, canvas.height);
    ctx.stroke();
}

var steps = 0;
function animateSnow() {
    steps++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (nighttime) {
        document.getElementById('body').classList.add('isNight')
    } else {
        document.getElementById('body').classList.remove('isNight')
    }
    if (snowEnabled) {
    
    // Create new snowflakes if below max limit
        if (snowflakes.length < maxSnowflakes) {
            snowflakes.push(createSnowflake());
        }
        if (windEnabled) {
            snowflakes.forEach(element => {
                element.x += (Math.sin(steps / 100) * 0.5)+0.1; // Horizontal wind effect
            });
        }
    }
    if (snowLightning) {
        if (lightningOnscreen && lightningFramesLeft > 0) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'; // Flash effect
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            lightningFramesLeft--;
            if (lightningFramesLeft === 0) {
                lightningOnscreen = false;
            }
        }
        if (!lightningOnscreen && Math.random() < 0.001) { // 1% chance of lightning each frame
            drawLightning();
            lightningOnscreen = true;
            lightningFramesLeft = 5; // Show for 5 frames
        } else if (lightningOnscreen && lightningFramesLeft > 0) {
            drawLightning();
        }
    }

    updateSnowflake();
    drawSnowflake();
      
    requestAnimationFrame(animateSnow);
}
function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * 7 * dpr; // 5x the viewport height
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = (window.innerHeight * 7) + 'px';
    ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform before drawing
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();


animateSnow();
