// Main pomodoro timer
let mainTimer;
let mainSeconds = 0;
let mainMinutes = 25;
let pushedFocus = 25;
let pushedRest = 5;
let mainIsTimerRunning = false;
let mainIsFocus = true

const alarm = new Audio('/static/hello/sound/alarm.wav'); // Play when timer complete
const rest = new Audio('/static/hello/sound/rest.wav'); // Play when time for rest

function startMainTimer() {
    if (!mainIsTimerRunning) {
        mainTimer = setInterval(updateMainTimer, 1000); // Realtime is 1000
        mainIsTimerRunning = true;
    }
}

function updateMainTimer() {
    mainSeconds--;

    if (mainSeconds < 0) {
        mainSeconds = 59;

        mainMinutes--;

        if (mainMinutes < 0) {
            timerComplete();
            return;
        }
    }

    updateMainTimerDisplay();
}

function updateMainTimerDisplay() {
    const formattedMainMinutes = padTime(mainMinutes);
    const formattedMainSeconds = padTime(mainSeconds);
    document.getElementById('minutes').innerText = formattedMainMinutes;
    document.getElementById('seconds').innerText = formattedMainSeconds;

    if (mainIsFocus) {
        updateArc(focusArc, (mainMinutes*6 + mainSeconds/10)+pushedRest*6);
        document.getElementById('title').innerText = "Focus: " + formattedMainMinutes + ":" + formattedMainSeconds
    } else {
        updateArc(restArc, (mainMinutes*6 + mainSeconds/10));
        document.getElementById('title').innerText = "Rest: " + formattedMainMinutes + ":" + formattedMainSeconds
    }
}

function timerComplete() {
    if (mainIsFocus == false) { // Completes timer after rest
        alarm.play();
        resetTimer();
        startMainTimer(); // Loops timer once complete
            } else { // Switches timer to rest
        rest.play();
        mainMinutes = pushedRest;
        mainSeconds = 0;
        mainIsFocus = false;
        updateArc(focusArc, 0)
    }
}

function pauseTimer() {
    clearInterval(mainTimer);
    mainIsTimerRunning = false;
    document.getElementById('title').innerText = "FocusMii"
}

function resetTimer() {
    clearInterval(mainTimer);
    mainIsTimerRunning = false;
    mainIsFocus = true;
    mainSeconds = 0;
    mainMinutes = pushedFocus;
    updateArc(restArc, pushedRest*6)
    updateMainTimerDisplay();
    document.getElementById('title').innerText = "FocusMii"
}

function padTime(time) {
    return (time < 10) ? `0${time}` : time;
}

// For timer profiles
const timers = {};

function pushITimer(timerId) { // Pushes a given timer profile to the main timer for use
    pushedFocus = parseInt(document.getElementById(`initialFocus${timerId}`).innerText) || 0;
    pushedRest = parseInt(document.getElementById(`initialRest${timerId}`).innerText) || 0;
    resetTimer();
}

// For analog timer
document.addEventListener("DOMContentLoaded", function() { // Making sure the page is loaded before trying to fetch arc information
    const restArc = document.getElementById("restArc");
    const focusArc = document.getElementById("focusArc");
    updateArc(restArc, 30);
    updateArc(focusArc, 180);
});

const cx = 470;
const cy = 460;
const radius = 378;

function updateArc(arc, degree) {
    const adjustedRadius = radius
    while (degree >= 360) {
        degree = degree - 360
    }
    const angle = (Math.PI / 180) * degree; // Convert degrees to radians
    //console.log(degree)
  
    // End point of the arc
    const endX = cx + adjustedRadius * Math.sin(angle);
    const endY = cy - adjustedRadius * Math.cos(angle); // Negative for SVG Y-axis
  
    const largeArcFlag = degree > 180 ? 1 : 0;
  
    // Define the path for the slice
    const pathData = `
      M ${cx} ${cy} 
      L ${cx} ${cy - adjustedRadius} 
      A ${adjustedRadius} ${adjustedRadius} 0 ${largeArcFlag} 1 ${endX} ${endY}
      Z
    `;
    arc.setAttribute("d", pathData);
}