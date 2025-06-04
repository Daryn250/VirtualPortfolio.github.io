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

function loadCaptchaImage(imageUrl, gridWidth, gridHeight) {
    const grid = document.querySelector('.captcha-grid');
    const container = document.querySelector('.captcha-container');

    // Animate out old images
    const oldImgs = grid.querySelectorAll('.captcha-img');
    oldImgs.forEach(img => img.classList.add('anim-out'));

    // Wait for fade-out to finish
    setTimeout(() => {
        grid.innerHTML = '';

        // Change grid size AFTER fade-out
        grid.style.width = (gridWidth * 80) + "px";
        grid.style.height = (gridHeight * 80) + "px";
        grid.style.gridTemplateColumns = `repeat(${gridWidth}, 80px)`;

        // Let the container animate to the new size
        // Wait a frame to ensure the browser registers the size change
        setTimeout(() => {
            cropImageToRatio(imageUrl, gridWidth*100, gridHeight*100, function(croppedDataUrl) {
                for (let row = 0; row < gridHeight; row++) {
                    for (let col = 0; col < gridWidth; col++) {
                        const div = document.createElement('div');
                        div.className = 'captcha-img anim-in';
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
                //highlightCorrect();
            });
        }, 20); // 20ms is enough for most browsers to register the size change
    }, 400); // Match the CSS transition duration for fade-out
}

function areSquaresSelected(selectedTuples, gridWidth) {
    const squares = document.querySelectorAll('.captcha-img');
    // Build a Set of correct indices for fast lookup
    const correctSet = new Set(selectedTuples.map(([row, col]) => row * gridWidth + col));

    for (let i = 0; i < squares.length; i++) {
        const isSelected = squares[i].classList.contains('selected');
        const shouldBeSelected = correctSet.has(i);
        if (isSelected !== shouldBeSelected) {
            return false;
        }
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
    loadCaptchaImage(next.url, next.x, next.y);
    document.getElementById("captchaPrompting").textContent = next.text;
    document.getElementById("submit").textContent = 'skip'
}

var captchas = [
    {url:"Cropped_Image.png",text:"people",x:3,y:3,correct:[[1,0],[1,1],[1,2],[2,0],[2,1],[2,2],]},
    {url:"Cropped_Image.png",text:"no people",x:5,y:3,correct:[[0,0],[0,1],[0,2],[0,3],[0,4],[1,4]]},
    {url:"img3.jpg",text:"no telephone poles",x:3,y:4,correct:[[0,0],[0,2],[1,0],[1,2],[2,0],[2,2],[3,0],[3,2]]},
    {url:"img4.jpg",text:"poison ivy",x:4,y:4,correct:[]},
    {url:"img5.jpg",text:"the owl",x:5,y:5,correct:[[1,1],[2,1],[3,1]]},
    {url:"img6.jpg",text:"the color yellow",x:5,y:5,correct:[[2,2],[3,2],[4,0]]},
    {url:"img7.jpg",text:"solution less than 0",x:3,y:2,correct:[[0,0]]},
    {url:"img8.jpg",text:"someone with the name Ian",x:6,y:5,correct:[[1,1],[1,2],[2,1],[2,2],[3,1],[3,2],[4,1],[4,2]]},
    {url:"img9.png",text:"car that has right of way",x:4,y:4,correct:[[1,3]]},
    {url:"img10.jpg",text:"cool rocks",x:4,y:3,correct:[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3]]},
    {url:"img11.jpg",text:"Waldo",x:6,y:6,correct:[[3,4]]},

]

var currentChallenge = 0

// Initial load
window.addEventListener('DOMContentLoaded', function() {
    var current = captchas[currentChallenge];
    loadCaptchaImage(current.url, current.x, current.y);
    document.getElementById("captchaPrompting").textContent = current.text;
});

document.getElementById("submit").addEventListener('click', function () {
    var current = captchas[currentChallenge];

    if (areSquaresSelected(current.correct, current.x)) {
        currentChallenge += 1;
        if (currentChallenge < captchas.length) {
            var next = captchas[currentChallenge];
            loadCaptchaImage(next.url, next.x, next.y);
            document.getElementById("captchaPrompting").textContent = next.text;
            document.getElementById("submit").textContent = 'Skip'
        } else {
            // Optionally handle end of captchas
            alert("All captchas complete!");
        }
    } else {
        if (currentChallenge>0) {
        currentChallenge -=1
        var next = captchas[currentChallenge];
        loadCaptchaImage(next.url, next.x, next.y);
        document.getElementById("captchaPrompting").textContent = next.text;
        } else {
            
        }
    }
});
