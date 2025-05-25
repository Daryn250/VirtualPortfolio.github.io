document.getElementById('about-taskbar-btn')?.addEventListener('click', () => {
    const aboutWindow = document.getElementById('about-window');
    const aboutBtn = document.getElementById('about-taskbar-btn');
    if (aboutWindow?.classList.contains('hidden')) {
        aboutWindow.classList.remove('hidden');
        aboutBtn.classList.add('active');
    } else {
        aboutWindow.classList.add('hidden');
        aboutBtn.classList.remove('active');
    }
});

document.getElementById('mspaint-taskbar-btn')?.addEventListener('click', () => {
    const mspaintWindow = document.getElementById('mspaint-window');
    const mspaintBtn = document.getElementById('mspaint-taskbar-btn');
    if (mspaintWindow?.classList.contains('hidden')) {
        mspaintWindow.classList.remove('hidden');
        mspaintBtn.classList.add('active');
    } else {
        mspaintWindow.classList.add('hidden');
        mspaintBtn.classList.remove('active');
    }
});

document.getElementById('internet-taskbar-btn')?.addEventListener('click', () => {
    const internetWindow = document.getElementById('internet-window');
    const internetBtn = document.getElementById('internet-taskbar-btn');
    if (internetWindow?.classList.contains('hidden')) {
        internetWindow.classList.remove('hidden');
        internetBtn.classList.add('active');
    } else {
        internetWindow.classList.add('hidden');
        internetBtn.classList.remove('active');
    }
});

document.getElementById('close-about')?.addEventListener('click', () => {
    document.getElementById('about-window')?.classList.add('hidden');
    document.getElementById('about-taskbar-btn')?.classList.remove('active');
});

document.getElementById('close-internet')?.addEventListener('click', () => {
    document.getElementById('internet-window')?.classList.add('hidden');
    document.getElementById('internet-taskbar-btn')?.classList.remove('active');
});

document.getElementById('close-settings')?.addEventListener('click', () => {
    document.getElementById('settings-window')?.classList.add('hidden');
});

document.getElementById('close-mspaint')?.addEventListener('click', () => {
    document.getElementById('mspaint-window')?.classList.add('hidden');
    document.getElementById('mspaint-taskbar-btn')?.classList.remove('active');
});

document.getElementById('taskbar-icon')?.addEventListener('click', () => {
    document.getElementById('start-menu')?.classList.toggle('hidden');
});

document.querySelector('.start-menu-list li:nth-child(3)')?.addEventListener('click', () => {
    document.getElementById('settings-window')?.classList.toggle('hidden');
    document.getElementById('start-menu')?.classList.add('hidden');
});

document.getElementById('home-btn').addEventListener('click', () => {
    window.open('../home.html', '_self');
});


// Utility: Make window draggable
let topZ = 2000; // Start above any static z-index you use

function makeDraggable(windowEl, titleBarEl, zIndex) {
    let isDragging = false, offsetX = 0, offsetY = 0;
    titleBarEl.addEventListener('mousedown', (e) => {
        isDragging = true;
        const rect = windowEl.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        topZ += 1;
        windowEl.style.zIndex = topZ; // Bring to front
        document.body.style.userSelect = 'none';
    });
    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            let left = Math.max(0, Math.min(window.innerWidth - windowEl.offsetWidth, e.clientX - offsetX));
            let top = Math.max(0, Math.min(window.innerHeight - windowEl.offsetHeight, e.clientY - offsetY));
            windowEl.style.left = left + 'px';
            windowEl.style.top = top + 'px';
            windowEl.style.position = 'absolute';
        }
    });
    document.addEventListener('mouseup', () => {
        isDragging = false;
        document.body.style.userSelect = '';
    });
}

makeDraggable(
    document.getElementById('about-window'),
    document.getElementById('about-titlebar'),
    1001
);

makeDraggable(
    document.getElementById('settings-window'),
    document.getElementById('settings-titlebar'),
    1002
);

makeDraggable(
    document.getElementById('mspaint-window'),
    document.getElementById('mspaint-titlebar'),
    1003
);

makeDraggable(
    document.getElementById('internet-window'),
    document.getElementById('internet-titlebar'),
    1004
);


