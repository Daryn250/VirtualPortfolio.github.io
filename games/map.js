const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');

// Load the image
const img = new Image();
img.src = './mcmappng/mapimage.png';

// Define points of interest
const points = [
    { x: 1023, y: 43, radius: 20, text: "Suspension Bridge", ofs:160,
        desc: "The North Bridge is a suspension bridge designed to span the lake on the north side of the city. It is a key transportation route and would be a major landmark in the city.",
        img: "./mcmappng/bridge.png" },
    { x: 1342, y: 540, radius: 20, text: "Skyscraper", ofs:110,
        desc: "This skyscraper is the highest building in the city, standing at 210 blocks tall. It is a neo-futuristic design with blinding lights glowing all along the sides.",
        img: "./mcmappng/skyscraper.png" },
    { x: 1100, y: 530, radius: 20, text: "Highway Intersection", ofs:180,
        desc: "This highway intersection is situated on Main Street, which connects parts of the old city and parts of the new city together. It has a beautiful view with many different trees lining it's sides.",
        img: "./mcmappng/intersection.png" },
    { x: 378, y: 1100, radius: 20, text: "High Voltage Pylons", ofs:180,
        desc: "These high voltage pylons, surrounding the west front of the city lead from the power plant of the city to other parts of the country. Electricity is a main export of the city's economy.",
        img: "./mcmappng/pylon.png" },
    { x: 597, y: 393, radius: 20, text: "Future Power Plant", ofs:160,
        desc: "This is a design for a future power plant, it will be a coal burning plant with a two docks for cargo ships carrying coal. It also will include a large central office building and many other buildings, including a parking lot for employees.",
        img: "./mcmappng/powerplant.png" },
    { x: 1115, y: 265, radius: 20, text: "City Hall", ofs:70,
        desc: "This is the city hall, a smaller government building on the north end of Main Street. It is made of a polished white marble with a large golden dome adorning the top. It is a beautiful building with plans of expansion in the future.",
        img: "./mcmappng/cityhall.png" },
    { x: 1438, y: 551, radius: 20, text: "Blackstone Cathedral", ofs:180,
        desc: "The Blackstone Cathedral is one of the largest buildings in the city, standing on the east side. It features an impressive length of over 300 blocks. It is a gothic style cathedral with an enourmous center spire with a clocktower.",
        img: "./mcmappng/blackstonecathedral.png" },
    { x: 1139, y: 476, radius: 20, text: "New City", ofs:180,
        desc: "The West part of the city is the newer part of the city, featuring buildings made up to 6 months ago. It's the second part I built, after a short hiatus from building. I started work on this part of the city late 2024.",
        img: "./mcmappng/newcity.png" },
    { x: 1292, y: 641, radius: 20, text: "Old City", ofs:70,
        desc: "The old city is the original part of the city, featuring buildings made up to 3 years ago. It's the first part of the city I built, and features many different styles of buildings. It's a very detailed and thought out area, although small.",
        img: "./mcmappng/oldcity.png" },
    { x: 900, y: 1084, radius: 20, text: "Grand Prarie", ofs:90,
        desc: "The Grand Prarie is one of the few places not constructed by me. It's a city built by my brother and features an 1800s city style, complete with large wheat fields and barns.",
        img: "./mcmappng/grandprarie.png" }
    
    
];

let scale = 1;
let offsetX = 0;
let offsetY = 0;

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(offsetX, offsetY);
    ctx.scale(scale, scale);
    ctx.drawImage(img, 0, 0);
    ctx.restore();

    // Draw points of interest with constant size
    points.forEach(point => {
        ctx.save();
        ctx.translate(offsetX + point.x * scale, offsetY + point.y * scale);
        ctx.beginPath();
        // Diamond shape
        ctx.moveTo(0, -point.radius);
        ctx.lineTo(point.radius, 0);
        ctx.lineTo(0, point.radius);
        ctx.lineTo(-point.radius, 0);
        ctx.closePath();
        ctx.fillStyle = "rgb(173,92,122)";
        ctx.strokeStyle = "black";  // Add black border
        ctx.lineWidth = 2;         // Set border width
        ctx.fill();
        ctx.stroke();              // Draw the border
        ctx.restore();
    });
}

img.onload = function() {
    // Set canvas dimensions to match image
    canvas.width = img.width;
    canvas.height = img.height;
    
    // Set canvas display size in CSS (half of actual size for retina displays)
    canvas.style.width = img.width/2 + 'px';
    canvas.style.height = img.height/2 + 'px';
    
    draw();
};

img.onerror = function() {
    ctx.fillStyle = "red";
    ctx.font = "60px Arial";
    ctx.fillText("Image failed to load.", 100, 100);
};

// Mousemove listener
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect(), // abs. size of element
        scaleX = canvas.width / rect.width,    // relationship bitmap vs. element for x
        scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for y

    return {
        x: (evt.clientX - rect.left) * scaleX,   // scale mouse coordinates after they have
        y: (evt.clientY - rect.top) * scaleY     // been adjusted to be relative to element
    }
}

// Zoom with mouse wheel
canvas.addEventListener('wheel', function(event) {
    event.preventDefault();
    const mouse = getMousePos(canvas, event);

    const x = (mouse.x - offsetX) / scale;
    const y = (mouse.y - offsetY) / scale;

    const zoom = event.deltaY < 0 ? 1.05 : 0.95;
    let newScale = scale * zoom;

    // Limit zoom to initial size
    newScale = Math.max(newScale, 1);

    offsetX = mouse.x - x * newScale;
    offsetY = mouse.y - y * newScale;

    // Calculate maximum and minimum offsets to keep the image within bounds
    const maxOffsetX = 0;
    const maxOffsetY = 0;
    const minOffsetX = canvas.width - img.width * newScale;
    const minOffsetY = canvas.height - img.height * newScale;

    // Apply bounds to offsets
    offsetX = Math.max(minOffsetX, Math.min(maxOffsetX, offsetX));
    offsetY = Math.max(minOffsetY, Math.min(maxOffsetY, offsetY));

    scale = newScale;

    draw();
}, { passive: false });

let isPanning = false;
let startPan = { x: 0, y: 0 };
let startOffset = { x: 0, y: 0 };

// Mouse down: start panning
canvas.addEventListener('mousedown', function(event) {
    isPanning = true;
    startPan = getMousePos(canvas, event);
    startOffset = { x: offsetX, y: offsetY };
});

// Mouse up: stop panning
window.addEventListener('mouseup', function() {
    isPanning = false;
});

// Mouse move: pan if dragging
canvas.addEventListener('mousemove', function(event) {
    if (isPanning) {
        const mouse = getMousePos(canvas, event);
        offsetX = startOffset.x + (mouse.x - startPan.x);
        offsetY = startOffset.y + (mouse.y - startPan.y);

        // Keep the image within bounds
        const minOffsetX = canvas.width - img.width * scale;
        const minOffsetY = canvas.height - img.height * scale;
        offsetX = Math.max(minOffsetX, Math.min(0, offsetX));
        offsetY = Math.max(minOffsetY, Math.min(0, offsetY));

        draw();
    }
});

// Mousemove listener
canvas.addEventListener('mousemove', function(event) {
    const mouse = getMousePos(canvas, event);
    // Convert mouse coordinates to image space
    const imageX = (mouse.x - offsetX) / scale;
    const imageY = (mouse.y - offsetY) / scale;

    // Check if the mouse is over any point
    let hoveredPoint = null;
    points.forEach(point => {
        const dx = imageX - point.x;
        const dy = imageY - point.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        // Scale the hit detection radius inversely with the zoom
        if (distance < point.radius / scale) {
            hoveredPoint = point;
        }
    });

    // Redraw the canvas
    draw();

    // If hovering over a point, display its text
    if (hoveredPoint) {
        var mousePos = getMousePos(canvas, event);
        ctx.save();
        ctx.resetTransform();
        ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
        ctx.fillRect(mousePos.x - hoveredPoint.ofs, mousePos.y - 50, (hoveredPoint.ofs*2), 40);
        ctx.font = "30px mojangles";
        ctx.textAlign = "center";
        ctx.fillStyle = "white";
        ctx.fillText(hoveredPoint.text, mousePos.x, mousePos.y-20);
        ctx.restore();
    }
});
    window.addEventListener('click', function(event) {
        const mouse = getMousePos(canvas, event);
        const imageX = (mouse.x - offsetX) / scale;
        const imageY = (mouse.y - offsetY) / scale;
        // Check if the mouse is over any point
        points.forEach(point => {
            const dx = imageX - point.x;
            const dy = imageY - point.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            // Scale the hit detection radius inversely with the zoom
            if (distance < point.radius / scale) {
                document.getElementById("locTitle").innerText = point.text;
                document.getElementById("locDesc").innerText = point.desc;
                document.getElementById("location-image").src = point.img;
                document.getElementById("location-image").alt = point.text;
            }
        });
    }, { passive: false });