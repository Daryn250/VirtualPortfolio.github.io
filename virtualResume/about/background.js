const canvas = document.getElementById("backgroundCanvas")
        const ctx = canvas.getContext("2d")

        let color1 = document.getElementById('color1');
        let color2 = document.getElementById('color2');
        let slider = document.getElementById('myRange');
        let rectSize = parseInt(slider.value);
        let trailsEnabled = document.getElementById('trailsEnabled');
        let Speed = document.getElementById('myRange2');
        let speed = parseInt(Speed.value);

        trailsEnabled.addEventListener('change', function() {
            if (trailsEnabled.checked) {
            } else {
                for (let x = 0; x < all.length; x++) {
                    for (let y = 0; y < all[x].length; y++) {
                        all[x][y].current = 0;
                    }
                }
            }
        });

        Speed.addEventListener('input', function() {
            let newSpeed = Math.floor(parseInt(Speed.value));
            if (newSpeed !== speed) {
                speed = newSpeed;
            }
        });

        slider.addEventListener('input', function() {
            let newSize = Math.floor(25-parseInt(slider.value));
            if (newSize !== rectSize) {
                rectSize = newSize;
                resizeCanvas();
                
            }
        });

        color1.addEventListener('input', function() {
            let newColor = color1.value;
            colorList[0] = newColor;
        });
        color2.addEventListener('input', function() {
            let newColor = color2.value;
            colorList[1] = newColor;
        });

        const totalSize = {
            'x': Math.round(canvas.width/rectSize),
            'y': Math.round(canvas.height/rectSize)
        }
        var paused = false

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            // draw everything again
            ctx.fillStyle = '#3f757d';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            totalSize.x = Math.ceil(canvas.width/rectSize)
            totalSize.y = Math.ceil(canvas.height/rectSize)
            
            for (let x = 0; x<all.length; x++) {
                for (let y = 0; y<all[x].length; y++) {
                    let curr = all[x][y]
                    curr.width = rectSize
                    curr.height = rectSize
                    curr.x = (x*curr.width)
                    curr.y = (y*curr.height)
                    curr.fill = colorList[0]
                    curr.current = 0
                }
            }
            all = Rects(totalSize)
        }
        
        window.addEventListener("resize", resizeCanvas)
        
        canvas.addEventListener("mousemove", function(event) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            for (let x = 0; x < all.length; x++) {
                for (let y = 0; y < all[x].length; y++) {
                    const curr = all[x][y];
                    if (
                        mouseX >= curr.x &&
                        mouseX <= curr.x + curr.width &&
                        mouseY >= curr.y &&
                        mouseY <= curr.y + curr.height
                    ) {
                        
                        curr.alive = true
                        curr.fill = '#25454a'  
                    }
                }
            }
        });

        window.addEventListener("keypress", function(event) {
            if (event.key === " " || event.key === "Spacebar") {
                paused = !paused;
            }
        });

        function Rects(amt) {
            var rectMap = []
            for (let c = 0; c<amt.x; c++) {
                rectMap.push([])
                for (let v = 0; v<amt.y; v++) {
                    let sizex = rectSize
                    let sizey = rectSize
                    let rect = {
                        width:sizex,
                        height:sizey,
                        x:(c * sizex),
                        y:(v * sizey),
                        fill:'#5ca2ad',
                        current:0,
                        alive:false,
                    }
                    rectMap[c].push(rect)
                }
            }
            return rectMap
        }

        function drawRects(list) {
            for (let x = 0; x<all.length; x++) {
                for (let y = 0; y<all[x].length; y++) {
                    let curr = list[x][y]
                    ctx.fillStyle = curr.fill
                    ctx.fillRect(curr.x,curr.y,curr.width,curr.height)
                }
            }
        }

    const colorList = [
                '#5ca2ad',
                '#25454a'
            ];
    function interpolateHexColor(minHex, maxHex, t) {
        t = Math.max(0, Math.min(1, t)); // Clamp t between 0 and 1

        function hexToRgb(hex) {
            hex = hex.replace('#', '');
            return {
                r: parseInt(hex.slice(0, 2), 16),
                g: parseInt(hex.slice(2, 4), 16),
                b: parseInt(hex.slice(4, 6), 16),
            };
        }

        function rgbToHex(r, g, b) {
            return '#' + [r, g, b]
                .map(v => Math.round(v).toString(16).padStart(2, '0'))
                .join('');
        }

        const c1 = hexToRgb(minHex);
        const c2 = hexToRgb(maxHex);

        return rgbToHex(
            c1.r + (c2.r - c1.r) * t,
            c1.g + (c2.g - c1.g) * t,
            c1.b + (c2.b - c1.b) * t
        );
    }
            

        function updateRects(list) {
            
            let spreadTo = structuredClone(all); //duplicate list
            for (let x = 0; x < all.length; x++) {
                for (let y = 0; y < all[x].length; y++) {
                    let self = spreadTo[x][y];

                    let surrounding = 0
                    for (let i = -1; i<=1; i++) {
                        for (let a = -1; a<=1; a++) {
                            let nx = x + i;
                            let ny = y + a;

                            // Skip the center cell itself
                            if (i === 0 && a === 0) continue;
                            // Bounds check
                            if (nx >= 0 && nx < totalSize.x && ny >= 0 && ny < totalSize.y) {
                                let neighbor = all[nx][ny];
                                if (neighbor.alive == true) {
                                    surrounding++
                                }
                            }
                        }
                    }

                    const previouslyAlive = self.alive;

                // Update alive state based on neighbors count
                if (surrounding > 3 || (surrounding === 2 && self.alive === true)) {
                    if (trailsEnabled.checked) {
                        self.current = 1; // start fading from 1
                    } else {
                        self.current = 0; // no fade, just dead
                    }
                }

                // Compute new alive state
                const currentlyAlive = (previouslyAlive) 
                    ? (surrounding === 2 || surrounding === 3) 
                    : (surrounding === 3);

                self.alive = currentlyAlive;

                // Detect if cell just died (was alive but now dead)
                if (previouslyAlive && !currentlyAlive) {
                    if (trailsEnabled.checked) {
                        self.current = 1; // start fading from 1
                    } else {
                        self.current = 0; // no fade, just dead

                    }
                }

                // Always set fill color based on alive state and trails
                if (self.alive) {
                    self.fill = colorList[1]; // alive color
                } else if (self.current > 0) {
                    if (trailsEnabled.checked) {
                        self.fill = interpolateHexColor(colorList[1], colorList[0], self.current);
                    } else {
                        self.fill = colorList[0]; // dead color
                    }
                    self.fill = interpolateHexColor(colorList[0], colorList[1], self.current);
                    self.current = self.current / 2;
                    if (self.current < 0) self.current = 0;
                } else {
                    self.fill = colorList[0]; // dead color
                }
                    
            }
        }
        
        all = spreadTo
        
    }
            
    
        var frames = 0
        
        var all = Rects(totalSize)
        resizeCanvas()
        function updateBackground() {
            frames++
            drawRects(all) 
            if (!paused && frames % speed == 0) {
                updateRects(all)
            }
            requestAnimationFrame(updateBackground)
        }
        updateBackground()
