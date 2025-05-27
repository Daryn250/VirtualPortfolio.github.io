document.addEventListener('DOMContentLoaded', function() {
            async function getCodeFromFile(filePath, elementId) {
                try {
                    const response = await fetch(filePath);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.text();
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.textContent = data;
                    } else {
                        console.error(`Element with id ${elementId} not found`);
                    }
                } catch (error) {
                    console.error('Error loading file:', error);
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.textContent = `Error loading ${filePath}: ${error.message}`;
                    }
                }
            }

            const fetchlist = [
                { file: '../home.html', element: 'sourceCode' },
                { file: './conways.py', element: 'conways' },
                { file: './ml.py', element: 'ml' },
                { file: './final_cube.py', element: '3dcube' },
                { file: './a_star.py', element: 'astar' },
                { file: './slots.py', element: 'slots' },
                { file: './wave_function_collapse_2.py', element: 'wfc' },
                { file: './bossfight.py', element: 'bossfight' },
                { file: './wordle.py', element: 'wordle' },
            ];
            // Loop through the list and fetch each file
            fetchlist.forEach(item => {
                getCodeFromFile(item.file, item.element);
            });


            // Parallax scrolling effect
            
            function onScroll() {
                var scrolled = window.pageYOffset;
                
                // Different speeds for different layers with limited decimal places
                document.getElementById('layer1').style.transform = 
                    `translateY(${(scrolled * -0.5).toFixed(3)}px)`;
                document.getElementById('layer2').style.transform = 
                    `translateY(${(scrolled * -0.3).toFixed(3)}px)`;
                document.getElementById('layer3').style.transform = 
                    `translateY(${(scrolled * -0.1).toFixed(3)}px)`;
                
                // Remove navbar position handling
            }
            window.addEventListener('scroll', onScroll);
            onScroll(); // Initial call to set positions on page load
            // Preload images
            const preloadImages = () => {
                const imageUrls = [
                    './background/layer1(1).png',
                    './background/layer1(2).png',
                    './background/layer1(3).png',
                    './background/layer2(1).png',
                    './background/layer2(2).png',
                    './background/layer2(3).png',
                    './background/layer3(1).png',
                    './background/layer3(2).png',
                    './background/layer3(3).png'
                ];
                
                imageUrls.forEach(url => {
                    const img = new Image();
                    img.src = url;
                });
            };

            // Call preload before starting animation
            preloadImages();
            
            var frames = 0;
            var l1frame = 1;
            var l2frame = 1;
            var l3frame = 1;

            // Modify the animation function
            function animateParallax() {
                frames += 1;
                
                // Use longer intervals to reduce frequency of frame changes
                if (frames % 45 === 0) {  // Increased from 30 to 45
                    l1frame = (l1frame % 3) + 1;
                    l2frame = (l2frame % 3) + 1;
                    
                    // Use CSS classes instead of direct style manipulation
                    const layer1 = document.getElementById('layer1');
                    const layer2 = document.getElementById('layer2');
                    
                    // Queue the frame updates
                    window.requestAnimationFrame(() => {
                        layer1.style.backgroundImage = `url('./background/layer1(${l1frame}).png')`;
                        // Small delay between updates to prevent simultaneous changes
                        setTimeout(() => {
                            layer2.style.backgroundImage = `url('./background/layer2(${l2frame}).png')`;
                        }, 16);  // One frame delay at 60fps
                    });
                }
                
                if (frames % 150 === 0) {  // Increased from 130 to 150
                    l3frame = (l3frame % 3) + 1;
                    const layer3 = document.getElementById('layer3');
                    
                    window.requestAnimationFrame(() => {
                        layer3.style.backgroundImage = `url('./background/layer3(${l3frame}).png')`;
                    });
                }
                
                window.requestAnimationFrame(animateParallax);
            }

            // Initialize with first frame
            let preloadComplete = false;
            function initAnimation() {
                const imageUrls = [
                    './background/layer1(1).png',
                    './background/layer1(2).png',
                    './background/layer1(3).png',
                    './background/layer2(1).png',
                    './background/layer2(2).png',
                    './background/layer2(3).png',
                    './background/layer3(1).png',
                    './background/layer3(2).png',
                    './background/layer3(3).png'
                ];
                
                // Create and store Image objects
                const preloadedImages = {};
                
                // Promise to load all images
                Promise.all(imageUrls.map(url => {
                    return new Promise((resolve, reject) => {
                        const img = new Image();
                        img.onload = () => {
                            preloadedImages[url] = img;
                            resolve();
                        };
                        img.onerror = reject;
                        img.src = url;
                    });
                }))
                .then(() => {
                    console.log('All images loaded successfully');
                    animateParallax();
                })
                .catch(error => console.error('Image loading failed:', error));
                
                function animateParallax() {
                    frames += 1;
                    
                    if (frames % 45 === 0) {
                        l1frame = (l1frame % 3) + 1;
                        l2frame = (l2frame % 3) + 1;
                        
                        const layer1 = document.getElementById('layer1');
                        const layer2 = document.getElementById('layer2');
                        
                        // Use RAF for better timing
                        requestAnimationFrame(() => {
                            // Update background images in sequence
                            layer1.style.backgroundImage = `url('./background/layer1(${l1frame}).png')`;
                            
                            // Stagger updates to prevent simultaneous changes
                            setTimeout(() => {
                                layer2.style.backgroundImage = `url('./background/layer2(${l2frame}).png')`;
                            }, 50);
                        });
                    }
                    
                    if (frames % 150 === 0) {
                        l3frame = (l3frame % 3) + 1;
                        const layer3 = document.getElementById('layer3');
                        
                        requestAnimationFrame(() => {
                            layer3.style.backgroundImage = `url('./background/layer3(${l3frame}).png')`;
                        });
                    }
                    
                    requestAnimationFrame(animateParallax);
                }
            }

            // Start the animation only after preloading
            initAnimation();

            
        });