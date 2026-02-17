// EXPOSE FUNCTIONS TO PYTHON
eel.expose(updateTerminal);
eel.expose(updateStatus);
eel.expose(updateStats);
eel.expose(updateWeather);

// ELEMENT REFERENCES
const elements = {
    cpuBar: document.getElementById('cpu-bar'),
    cpuVal: document.getElementById('cpu-val'),
    ramBar: document.getElementById('ram-bar'),
    ramVal: document.getElementById('ram-val'),
    battBar: document.getElementById('batt-bar'),
    battVal: document.getElementById('batt-val'),
    output: document.getElementById('output'),
    status: document.getElementById('status'),
    clock: document.getElementById('clock-text'),
    date: document.getElementById('date-text'),
    weatherTemp: document.getElementById('weather-temp'),
    weatherIcon: document.getElementById('weather-icon'),
    weatherLoc: document.getElementById('weather-loc')
};

// SYSTEM BOOT SEQUENCE
window.onload = function () {
    simulateBoot();
};

function simulateBoot() {
    const bootMsgs = [
        "INITIALIZING CORE...",
        "LOADING MODULES...",
        "ESTABLISHING SECURE LINK...",
        "SYSTEM ONLINE."
    ];
    let delay = 0;
    bootMsgs.forEach(msg => {
        setTimeout(() => updateTerminal(msg, "sys"), delay);
        delay += 800;
    });
    // Signal Python that UI is ready
    setTimeout(() => {
        if (eel.app_ready) eel.app_ready();
    }, 1000);
}

// UPDATE STATS (CALLED FROM PYTHON)
function updateStats(cpu, ram, battery) {
    if (elements.cpuBar) {
        elements.cpuBar.style.width = cpu + '%';
        elements.cpuVal.innerText = cpu + '%';
    }
    if (elements.ramBar) {
        elements.ramBar.style.width = ram + '%';
        elements.ramVal.innerText = ram + '%';
    }
    if (elements.battBar) {
        elements.battBar.style.width = battery + '%';
        elements.battVal.innerText = battery + '%';
    }
}

// TERMINAL OUTPUT
function typeWriter(element, text, i = 0) {
    if (i < text.length) {
        element.innerHTML += text.charAt(i);
        // Scroll to bottom
        elements.output.scrollTop = elements.output.scrollHeight;
        setTimeout(() => typeWriter(element, text, i + 1), 15);
    }
}

function updateTerminal(text, sender) {
    const newMsg = document.createElement("div");

    if (sender === "avi" || sender === "sys") {
        newMsg.className = "msg-sys";
        newMsg.innerHTML = `<span style="opacity:0.5;">></span> `;
        elements.output.appendChild(newMsg);
        typeWriter(newMsg, text);
    } else {
        newMsg.className = "msg-user";
        newMsg.innerText = text;
        elements.output.appendChild(newMsg);
        elements.output.scrollTop = elements.output.scrollHeight;
    }
}

// UPDATE STATUS
function updateStatus(status) {
    elements.status.innerText = status.toUpperCase();
    if (status.includes("Listening")) {
        elements.status.style.color = "#00FF00"; // Green
        elements.status.style.textShadow = "0 0 10px #00FF00";
    } else {
        elements.status.style.color = "#00FFFF"; // Cyan
        elements.status.style.textShadow = "none";
    }
}

// START LISTENING
function startListening() {
    updateStatus("Listening...");
    eel.start_avi();
}

// CLOCK & DATE
setInterval(() => {
    const now = new Date();
    elements.clock.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    elements.date.innerText = now.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' }).toUpperCase();
}, 1000);

// WEATHER (Placeholder or called from Python)
function updateWeather(temp, condition, city) {
    if (elements.weatherTemp) elements.weatherTemp.innerText = temp + "°C";
    if (elements.weatherLoc && city) elements.weatherLoc.innerText = city.toUpperCase();

    // Simple icon mapping
    let icon = "☁️";
    if (condition) {
        let c = condition.toLowerCase();
        if (c.includes("sun") || c.includes("clear")) icon = "☀️";
        else if (c.includes("rain")) icon = "bumble🌧️";
        else if (c.includes("fog")) icon = "🌫️";
        else if (c.includes("cloud")) icon = "☁️";
    }
    if (elements.weatherIcon) elements.weatherIcon.innerText = icon;
}