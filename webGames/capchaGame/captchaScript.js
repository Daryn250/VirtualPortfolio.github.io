document.querySelectorAll('.captcha-img').forEach(img => {
    img.addEventListener('click', function() {
        this.classList.toggle('selected');
        updateButtonState();
    });
});

function updateButtonState() {
    const anySelected = document.querySelector('.captcha-img.selected') !== null;
    const btn = document.querySelector('.captcha-btn');
    if (btn) {
        btn.textContent = anySelected ? 'Submit' : 'Skip';
    }
}

function cropImageToRatio(imageUrl, targetWidth, targetHeight, callback) {
    const img = new Image();
    img.src = imageUrl

    img.onload = function() {
        const originalWidth = img.width;
        const originalHeight = img.height;
        const originalRatio = originalWidth / originalHeight;
        const targetRatio = targetWidth / targetHeight;

        let sx, sy, sw, sh;

        if (originalRatio > targetRatio) {
            // Image is too wide, crop sides
            sh = originalHeight;
            sw = sh * targetRatio;
            sx = (originalWidth - sw) / 2;
            sy = 0;
        } else {
            // Image is too tall, crop top/bottom
            sw = originalWidth;
            sh = sw / targetRatio;
            sx = 0;
            sy = (originalHeight - sh) / 2;
        }

        const canvas = document.createElement('canvas');
        canvas.width = targetWidth;
        canvas.height = targetHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, sx, sy, sw, sh, 0, 0, targetWidth, targetHeight);

        callback(canvas.toDataURL());
    };

    img.onerror = function() {
        console.error("Failed to load image for cropping:", imageUrl);
        callback(imageUrl); // fallback: return original
    };

    img.src = imageUrl;
}
function loadMultiImageCaptcha(imageUrls, gridWidth, gridHeight, cellSize = 80, labels = [], ref=[]) {
    const grid = document.querySelector('.captcha-grid');
    const container = document.querySelector('.captcha-container');

    // Animate out old images
    const oldImgs = grid.querySelectorAll('.captcha-img');
    oldImgs.forEach(img => img.classList.add('anim-out'));

    setTimeout(() => {
        grid.innerHTML = '';
        grid.style.width = (gridWidth * cellSize) + "px";
        grid.style.height = (gridHeight * cellSize) + "px";
        grid.style.gridTemplateColumns = `repeat(${gridWidth}, ${cellSize}px)`;

        setTimeout(() => {
            let totalCells = gridWidth * gridHeight;
            for (let i = 0; i < totalCells; i++) {
                const row = Math.floor(i / gridWidth);
                const col = i % gridWidth;
                const div = document.createElement('div');
                div.className = 'captcha-img anim-in';
                div.style.width = div.style.height = cellSize + "px";

                // Use the corresponding image, or fallback to the last one if not enough images
                const imgUrl = imageUrls[i] || imageUrls[imageUrls.length - 1];
                div.style.backgroundImage = `url('${imgUrl}')`;
                div.style.backgroundRepeat = 'no-repeat';
                div.style.backgroundSize = 'cover';
                div.style.backgroundPosition = 'center';

                // Add the checkmark icon
                const icon = document.createElement('img');
                icon.src = 'checkmark.png';
                icon.alt = 'selected';
                icon.className = 'selected-icon';
                div.appendChild(icon);

                div.addEventListener('click', function() {
                    this.classList.toggle('selected');
                    updateButtonState();
                    if (ref!=[]) {
                        window.open(ref[i])
                    }
                });

                // --- Hover logic for displaying label ---
                div.addEventListener('mouseover', function() {
                    const label = labels[i] || imgUrl.split('/').pop();
                    document.getElementById("captchaPrompting").textContent = label;
                });
                div.addEventListener('mouseout', function() {
                    // Restore the original prompt text
                    document.getElementById("captchaPrompting").textContent = captchas[currentChallenge].text;
                });

                grid.appendChild(div);
                setTimeout(() => div.classList.remove('anim-in'), 400);
            }
        }, 20);
    }, 400);
}

function loadAnimatedCaptcha(gridWidth, gridHeight) {
    const grid = document.querySelector('.captcha-grid');
    grid.innerHTML = '';
    grid.style.width = (gridWidth * 80) + "px";
    grid.style.height = (gridHeight * 80) + "px";
    grid.style.gridTemplateColumns = `repeat(${gridWidth}, 80px)`;
    const cellSize = 80;
    for (let row = 0; row < gridHeight; row++) {
        for (let col = 0; col < gridWidth; col++) {
            // Create wrapper div
            const wrapper = document.createElement('div');
            wrapper.className = 'captcha-img';
            wrapper.dataset.row = row;
            wrapper.dataset.col = col;
            wrapper.style.width = "80px";
            wrapper.style.height = "80px";
            wrapper.style.display = "flex";
            wrapper.style.alignItems = "center";
            wrapper.style.justifyContent = "center";
            wrapper.style.position = "relative";

            // Create canvas
            const cellCanvas = document.createElement('canvas');
            cellCanvas.width = cellCanvas.height = cellSize;
            cellCanvas.style.width = "100%";
            cellCanvas.style.height = "100%";
            cellCanvas.style.display = "block";
            wrapper.appendChild(cellCanvas);

            // Add checkmark icon
            const icon = document.createElement('img');
            icon.src = 'checkmark.png';
            icon.alt = 'selected';
            icon.className = 'selected-icon';
            wrapper.appendChild(icon);

            // Selection logic
            wrapper.addEventListener('click', function() {
                this.classList.toggle('selected');
                updateButtonState();
            });

            grid.appendChild(wrapper);
        }
    }
    animateCaptchaGrid(gridWidth, gridHeight, cellSize);
}

function loadSingleImageCaptcha(imageUrl, gridWidth, gridHeight, cellSize) {
    const grid = document.querySelector('.captcha-grid');
    const container = document.querySelector('.captcha-container');

    // Animate out old images
    const oldImgs = grid.querySelectorAll('.captcha-img');
    oldImgs.forEach(img => img.classList.add('anim-out'));

    // Wait for fade-out to finish
    setTimeout(() => {
        grid.innerHTML = '';

        // Change grid size AFTER fade-out
        grid.style.width = (gridWidth * cellSize) + "px";
        grid.style.height = (gridHeight * cellSize) + "px";
        grid.style.gridTemplateColumns = `repeat(${gridWidth}, ${cellSize}px)`;

        // Let the container animate to the new size
        // Wait a frame to ensure the browser registers the size change
        setTimeout(() => {
            cropImageToRatio(imageUrl, gridWidth*100, gridHeight*100, function(croppedDataUrl) {
                for (let row = 0; row < gridHeight; row++) {
                    for (let col = 0; col < gridWidth; col++) {
                        const div = document.createElement('div');
                        div.className = 'captcha-img anim-in';
                        div.style.width = div.style.height = cellSize + "px";
                        div.style.backgroundImage = `url('${croppedDataUrl}')`;
                        div.style.backgroundRepeat = 'no-repeat';
                        div.style.backgroundSize = `${gridWidth * 100}% ${gridHeight * 100}%`;

                        const x = gridWidth === 1 ? 50 : (col / (gridWidth - 1)) * 100;
                        const y = gridHeight === 1 ? 50 : (row / (gridHeight - 1)) * 100;
                        div.style.backgroundPosition = `${x}% ${y}%`;

                        const icon = document.createElement('img');
                        icon.src = 'checkmark.png'; // Use your icon path
                        icon.alt = 'selected';
                        icon.className = 'selected-icon';
                        div.appendChild(icon);

                        div.addEventListener('click', function() {
                            this.classList.toggle('selected');
                            updateButtonState();
                        });
                        grid.appendChild(div);

                        setTimeout(() => div.classList.remove('anim-in'), 400);
                    }
                }
            });
        }, 20); // 20ms is enough for most browsers to register the size change
    }, 400); // Match the CSS transition duration for fade-out
}

function loadCaptcha(captcha) {
    if (captcha.type === undefined) {
        alert("type for " + captcha + " not selected")
    } else {
        document.getElementById("captchaPrompting").textContent = captcha.text;
        document.getElementById("submit").textContent = 'Skip'
    }
    if (captcha.type === 'multi' && Array.isArray(captcha.url)) {
        loadMultiImageCaptcha(captcha.url, captcha.x, captcha.y, captcha.size || 80, captcha.labels || [], captcha.ref || []);
    }
    else if (captcha.type === 'single' && typeof captcha.url === 'string') {
        if (captcha.size === undefined) {
            loadSingleImageCaptcha(captcha.url, captcha.x, captcha.y, 80)
        } else {
            loadSingleImageCaptcha(captcha.url, captcha.x, captcha.y, captcha.size)
        }
    }
    else if (captcha.type === 'canvas') {
        loadAnimatedCaptcha(captcha.x, captcha.y)
    }
    const helperImg = document.getElementById('captcha-helper-img');
    if (captcha.helper!=undefined) {
        // Show the helper image
        helperImg.src = captcha.helper
        helperImg.style.display = 'block';
    } else {
        helperImg.style.display = 'none';
    }
}


function areSquaresSelected(selectedTuples, gridWidth, neutralTuples = []) {
    const squares = document.querySelectorAll('.captcha-img');
    // Build Sets for fast lookup
    const correctSet = new Set(selectedTuples.map(([row, col]) => row * gridWidth + col));
    const neutralSet = new Set(neutralTuples.map(([row, col]) => row * gridWidth + col));

    for (let i = 0; i < squares.length; i++) {
        const isSelected = squares[i].classList.contains('selected');
        const shouldBeSelected = correctSet.has(i);
        const isNeutral = neutralSet.has(i);

        // If not neutral, must match correct selection
        if (!isNeutral && isSelected !== shouldBeSelected) {
            return false;
        }
        // If neutral, any state is allowed
    }
    return true;
}

function printSelectedInList(gridWidth, gridHeight) {
    const squares = document.querySelectorAll('.captcha-img');
    const selected = [];
    for (let i = 0; i < squares.length; i++) {
        if (squares[i].classList.contains('selected')) {
            const row = Math.floor(i / gridWidth);
            const col = i % gridWidth;
            selected.push([row, col]);
        }
    }
    console.log(selected);
    // If you want a string for copy-pasting:
    console.log(selected.map(pair => `[${pair[0]},${pair[1]}]`).join(','));
}

function highlightCorrect() {
    // Get the current challenge's correct squares and grid width
    var current = captchas[currentChallenge];
    var correct = current.correct;
    var gridWidth = current.x;
    const squares = document.querySelectorAll('.captcha-img');

    correct.forEach(([row, col]) => {
        const idx = row * gridWidth + col;
        if (squares[idx]) {
            squares[idx].style.filter = "invert()"
        }
    });
}

function setChallengeTo(num) {
    currentChallenge = num
    var next = captchas[num];
    loadCaptcha(next);
    document.getElementById("captchaPrompting").textContent = next.text;
    document.getElementById("submit").textContent = 'Skip'
}

var captchas = [
    {url:"images/img1-2.png",text:"pedestrians",x:3,y:3,correct:[[1,0],[1,1],[1,2],[2,0],[2,1],[2,2],],neutral:[], type:'single'},
    {url:"images/img1-2.png",text:"no pedestrians",x:5,y:3,correct:[[0,0],[0,1],[0,2],[0,3],[0,4],[1,4]],neutral:[], type:'single'},
    {url:"images/img3.jpg",text:"no telephone poles",x:3,y:4,correct:[[0,0],[0,2],[1,0],[1,2],[2,0],[2,2],[3,0],[3,2]],neutral:[], type:'single'},
    {url:"images/img4.jpg",text:"poison ivy",x:4,y:4,correct:[],neutral:[], type:'single'},
    {url:"images/img5.jpg",text:"the owl",x:5,y:5,correct:[[1,1],[2,1],[3,1]],neutral:[[1,2],[2,0],[2,2],[3,0],[4,0],[4,1]], type:'single'},
    {url:"images/img6.jpg",text:"the color yellow",x:5,y:5,correct:[[2,2],[3,2],[4,0]],neutral:[[2,1],[3,1]], type:'single'},
    {url:"images/img7.jpg",text:"solution less than 0",x:3,y:2,correct:[[0,0]],neutral:[], type:'single'},
    {url:"images/img8.jpg",text:"someone with the name Ian",x:6,y:5,correct:[[1,1],[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2]],neutral:[], type:'single'},
    {url:"images/img9.png",text:"car that has right of way",x:4,y:4,correct:[[1,3]],neutral:[], type:'single'},
    {url:"images/img10.jpg",text:"cool rocks",x:4,y:3,correct:[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3]],neutral:[], type:'single'},
    {url:"images/img11.jpg",text:"Waldo",x:6,y:6,correct:[[3,4]],neutral:[], type:'single'},
    {url:[
        "images/img3.jpg", "images/bat.jpg", "images/img9.png",
        "images/baseballbat.jpg", "images/img5.jpg", "images/kitten.jpg",
        "images/fountain.jpg", "images/statue.jpg", "images/img4.jpg",
    ],text:"previously seen captchas",x:3,y:3,correct:[[0,0],[0,2],[1,1],[2,2]], type:'multi'},
    {url:[
        "images/baseballbat.jpg", "images/bat.jpg",
    ],text:"bat",x:2,y:1,correct:[[0,1]], type:'multi'},
    {url:"images/theseus.jpg", text:"Ship of Theseus" ,x:3,y:3,correct:[],neutral:[[0,0],[0,1],[1,1],[1,2],[2,0],[2,1],[2,2]],type:'single'},
    {url:"images/bugincode.png", text:"Syntax Errors" ,x:6,y:6,correct:[[1,2]],type:'single'},
    {text:"pong win screen",x:3,y:3,type:'canvas', game:'pong',neutral:[], helper:"images/pongWinScreen.png"},
    {url:[
        "images/color1.png","images/color1.png","images/color1.png","images/color1.png",
        "images/color1.png","images/color1.png","images/color1.png","images/color2.png",
        "images/color1.png","images/color1.png","images/color1.png","images/color1.png",
    ],text:"the odd color out",x:4,y:3,correct:[[1,3]],neutral:[], type:'multi'},
    {url:[
        "images/color3.png","images/color3.png","images/color3.png","images/color3.png",
        "images/color3.png","images/color3.png","images/color3.png","images/color3.png",
        "images/color3.png","images/color3.png","images/color3.png","images/color3.png",
    ],text:"the odd color out",x:4,y:3,correct:[],neutral:[], type:'multi', helper:"images/color3.png"},
    {url:[
        "images/guy1.png","images/guy2.png","images/guy3.png",
        "images/guy4.png","images/guy5.png","images/guy6.png",
    ],text:"guy who tailgated me on the freeway last night",x:3,y:2,correct:[[0,1]],neutral:[], type:'multi'},
    {url:[
        "images/guy1.png","images/guy2.png","images/guy3.png",
        "images/guy4.png","images/guy5.png","images/guy6.png",
    ],text:"guy who didnt tailgate me on the freeway last night",x:3,y:2,correct:[[0,0],[0,2],[1,0],[1,1],[1,2]],neutral:[], type:'multi'},
    {url:"images/trafficlight.jpg",text:"large traffic lights",x:7,y:7,correct:[[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[2,4],[3,0],[3,1],[3,2],[3,3],[3,4],[4,2],[4,3],[4,4]],neutral:[[0,2],[0,3],[0,4],[1,0],[2,0],[2,5],[3,0],[3,5],[4,5]],size:40,type:'single'},
    {url:"images/tyforplaying.jpg",text:"congratulations!",x:3,y:2,correct:[],neutral:[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]],type:'single'},
    {url:[
        "images/img1-2.png","images/img3.jpg","images/img4.jpg","images/img5.jpg",
        "images/img6.jpg","images/img7.jpg","images/img8.jpg","images/img9.png",
        "images/img10.jpg","images/img11.jpg","images/kitten.jpg","images/statue.jpg",
        "images/theseus.jpg","images/trafficlight.jpg","images/bat.jpg","images/baseballbat.jpg",
        "images/fountain.jpg","images/color1.png","images/color2.png","images/color3.png",
    ],ref:[
        "https://x.com/timessquarenyc","https://en.wikipedia.org/wiki/File:Palo_SES_Tegna_260513.jpg","https://www.researchgate.net/profile/Eddy-Moors/publication/254765422/figure/fig18/AS:669534444851212@1536640859424/ew-of-the-undergrowth-below-the-birch-and-pine-trees-near-the-scaffolding-tower-at-the.jpg",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiU-Orw0NqNAxXTFlkFHQiZJ80Qn5YKegQILBAB&url=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fautumn-greece&usg=AOvVaw1-ZE1r2QIBu3wuMM1Tonmu&opi=89978449", null, null, "https://www.freepik.com/free-photo/happy-family-spending-holidays-home_13307667.htm",
        "https://www.khon2.com/local-news/malfunctioning-traffic-signal-treat-it-as-a-four-way-stop/", "https://www.eiscolabs.com/collections/all/products/esngkit0007", "“Ski Slopes,” scene from Where’s Waldo? Illustration by Martin Handford", "https://www.pexels.com/photo/close-up-photography-of-brown-and-white-kitten-1870376/", "https://www.wallpaperflare.com/bronze-statues-alba-iulia-figure-metal-woman-artwork-design-wallpaper-woxwb",
        "https://en.wikipedia.org/wiki/File:Constantine_Volanakis_Argo.jpg","https://en.m.wikipedia.org/wiki/File:Traffic_lights.jpg", "https://commons.wikimedia.org/wiki/File:Little_Brown_Bat%3F_(flying_during_the_day_-_flushed%3F)_(33741700644).jpg", "https://en.m.wikipedia.org/wiki/File:Baseball_bat.svg",
        "https://commons.wikimedia.org/wiki/File:Ruth_Asawa%27s_San_Francisco_fountain_2.JPG", null, null, null

    ],labels:[
        "Times Square", "Utility Pole", "Birch Forest Brush", "Camoflauged Owl",
        "Road Sign", "Math Equations", "Happy Family", "4 Way Stop",
        "Rocks", "Where's Waldo", "Kitten", "Statue",
        "Ship of Theseus", "Traffic Lights", "Bat", "Baseball Bat",
        "Fountain", "Green", "Green Again", "Orange"
    ],text:"",x:4,y:5,correct:[],neutral:[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3],[4,0],[4,1],[4,2],[4,3]],type:'multi'},

]

var currentChallenge = 0

// Initial load
window.addEventListener('DOMContentLoaded', function() {
    var current = captchas[currentChallenge];
    loadCaptcha(current);
    document.getElementById("captchaPrompting").textContent = current.text;
});

document.getElementById("submit").addEventListener('click', function () {
    var current = captchas[currentChallenge];

    if (areSquaresSelected(current.correct, current.x, current.neutral)) {
        currentChallenge += 1;
        if (currentChallenge < captchas.length) {
            var next = captchas[currentChallenge];
            loadCaptcha(next);
            document.getElementById("captchaPrompting").textContent = next.text;
            document.getElementById("submit").textContent = 'Skip'
        } else {
            // Optionally handle end of captchas
        }
    } else {
        if (currentChallenge>0) {
        currentChallenge -=1
        var next = captchas[currentChallenge];
        loadCaptcha(next);
        document.getElementById("captchaPrompting").textContent = next.text;
        } else {

        }
    }
});
var game = null
function animateCaptchaGrid(gridWidth, gridHeight, cellSize) {
    game = captchas[currentChallenge].game
    const mainCanvas = document.getElementById('mainCaptchaCanvas');
    const mainCtx = mainCanvas.getContext('2d');
    if (game==='pong') {
        let t = 0;

        var paddle1 = {
            x:10,
            y:0,
            size:50,
        }
        var paddle2 = {
            x:220,
            y:70,
            size:50,
            vy:0
        }
        var ball = {
            x:120,
            y:120,
            vx:1,
            vy:1,
            size:5,
        }

        const grid = document.querySelector('.captcha-grid');
        grid.addEventListener('mousemove', (evt) => {
            const rect = grid.getBoundingClientRect();
            // Map mouse Y from grid to main canvas
            const y = (evt.clientY - rect.top) * (mainCanvas.height / grid.offsetHeight);
            paddle1.y = y - paddle1.size / 2; // Center the paddle on the mouse
        });


        function drawMainCanvas() {
            mainCtx.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
        
            ball.x += ball.vx;
            ball.y += ball.vy;
            if (ball.vx<0) {
                ball.vx-=0.01
            } else {
                ball.vx+=0.01
            }
            if (ball.vy<0) {
                ball.vy-=0.001
            } else {
                ball.vy+=0.001
            }
        
            // Ball bouncing off top/bottom
            if (ball.y < 0 || ball.y + ball.size > mainCanvas.height) {
                ball.vy = -ball.vy;
            }
        
            // Paddle 1 collision (left paddle, front is right side)
            if (
                ball.x <= paddle1.x + 10 && // Ball at or past paddle's right edge
                ball.x + ball.size >= paddle1.x && // Ball overlaps paddle's left edge
                ball.y + ball.size >= paddle1.y && // Ball bottom below paddle top
                ball.y <= paddle1.y + paddle1.size // Ball top above paddle bottom
            ) {
                // Only bounce if moving left to right (toward paddle2)
                if (ball.vx < 0) {
                    ball.vx = -ball.vx;
                    // Optional: add a little "english" based on where it hits the paddle
                    ball.vy += (ball.y + ball.size/2 - (paddle1.y + paddle1.size/2)) * 0.1;
                    // Move ball out of paddle to prevent sticking
                    ball.x = paddle1.x + 10;
                }
            }
        
            // Paddle 2 collision (right paddle, front is left side)
            if (
                ball.x + ball.size >= paddle2.x && // Ball at or past paddle's left edge
                ball.x <= paddle2.x + 10 && // Ball overlaps paddle's right edge
                ball.y + ball.size >= paddle2.y &&
                ball.y <= paddle2.y + paddle2.size
            ) {
                // Only bounce if moving right to left (toward paddle1)
                if (ball.vx > 0) {
                    ball.vx = -ball.vx;
                    // Optional: add a little "english"
                    // ball.vy += (ball.y + ball.size/2 - (paddle2.y + paddle2.size/2)) * 0.1;
                    // Move ball out of paddle to prevent sticking
                    ball.x = paddle2.x - ball.size;
                }
            }
        
            // Win/Lose logic
            if (ball.x > mainCanvas.width) {
                // player win
                
                game = 'pongWin';
            }
            if (ball.x < 0) {
                // player lose
                currentChallenge -= 1;
                loadCaptcha(captchas[currentChallenge]);
                game = null;
            }
        
            // Opponent paddle moving
            if (ball.y + ball.size / 2 > paddle2.y + paddle2.size / 2) {
                paddle2.vy += 0.2;
            }
            if (ball.y + ball.size / 2 < paddle2.y + paddle2.size / 2) {
                paddle2.vy -= 0.2;
            }
            paddle2.y+=paddle2.vy
            paddle2.vy /=1.1
        
            // Draw paddles and ball
            mainCtx.fillRect(paddle1.x, paddle1.y, 10, paddle1.size);
            mainCtx.fillRect(paddle2.x, paddle2.y, 10, paddle2.size);
            mainCtx.fillRect(ball.x, ball.y, ball.size, ball.size);
        }

        function updateGridCells() {
            const cells = document.querySelectorAll('.captcha-img');
            for (const cell of cells) {
                const canvas = cell.querySelector('canvas');
                if (canvas) {
                    const row = parseInt(cell.dataset.row);
                    const col = parseInt(cell.dataset.col);
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, cellSize, cellSize);
                    ctx.drawImage(
                        mainCanvas,
                        col * cellSize, row * cellSize, cellSize, cellSize, // src region
                        0, 0, cellSize, cellSize // dest region
                    );
                }
            }
        }

        function animate() {
            t += 1;
            if (game==='pong') {
                drawMainCanvas();
                updateGridCells();
                requestAnimationFrame(animate);
            }
            if (game === 'pongWin') {
                mainCtx.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
                mainCtx.font = "20px serif";
                mainCtx.textAlign = "center";
                mainCtx.textBaseline = "middle";
                mainCtx.fillText("You Win!", mainCanvas.width / 2, mainCanvas.height / 2);
                captchas[currentChallenge].correct = [[1,1]]
                captchas[currentChallenge].neutral = [[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]]
                updateGridCells();
            }
        }
        
            animate();
        
    }
}