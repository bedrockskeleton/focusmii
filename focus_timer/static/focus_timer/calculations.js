let currentProblem = 0; // Tracks the problem that the user is on
let updateTimer;
let score = 0; // Initialize a variable to track the user's score
let timer = 0; // Timer counts up from 0
let started = false; // Tracks whether or not the game is started
// Grabbing general elements from the DOM
const title = document.getElementsByTagName("title")[0];
const main = document.getElementsByClassName("main")[0];
const container = document.getElementById("right");
const intro = document.getElementById("intro");
const encouragement = document.getElementById("encouragement");
const startButton = document.getElementById("startButton");
const endButton = document.getElementById("endButton");
const arrows = document.getElementsByClassName("arrow");
const timerDisplay = document.getElementById("time");
const scoreDisplay = document.getElementById("score");
// Difficulty selector
const difficulties = ["Normal", "1-Back", "2-Back", "3-Back", "4-Back"];
let numBack = 0; // Number of problems "back" the user has to remember
const label = document.getElementById("difficultyLabel");
const leftArrow = document.getElementById("arrowLeft");
const rightArrow = document.getElementById("arrowRight");
// Problem count selector
const counts = [25, 50, 100] // Defines the amounts that the users can choose from
let countIndex = 0
problems = generateProblems(counts[0])
const countLabel = document.getElementById("countLabel");
const countLeftArrow = document.getElementById("countArrowLeft");
const countRightArrow = document.getElementById("countArrowRight");

console.log(problems)

function update() {
    timer ++;
    //console.log("Current Time:", timer/100); // Log time to console
}

async function start() {
    score = 0;
    container.innerHTML = '';
    console.log("Starting with", numBack, "-back");
    
    // Show/Hide necessary DOM elements
    main.className = "mainShrunk"
    intro.style.display = "none";
    startButton.style.display = "none";
    endButton.style.display = "flex";
    scoreDisplay.parentNode.style.display = "flex";
    scoreDisplay.innerText = `Score: ${score}/${problems.length}`;
    for (let arrow of arrows) {
        arrow.style.display = "none";
    }

    started = true;
    currentProblem = 0;
    for (let i = 0; i <= numBack; i++) { // Show the starting problems (next() function takes over after this)
        //console.log(problems[i]);
        insertProblem(i);
    };
    formatProblems()
    updateTimer = setInterval(update, 10); // Record time
}

function generateProblems(amount) {
    let n1 = 0;
    let n2 = 0;
    let result = 0;
    let userAnswer = -1;
    let problemList = [];
    for (let i = 0; i < amount; i++) {
        result = Math.floor(Math.random() * 10);
        n1 = Math.floor(Math.random() * 10);
        n2 = result - n1;
        // Creating an html element for the problem
        let node = document.createElement("div");
        node.id = `p${i}`;
        node.className = "problem";
        //console.log(n2)
        if (n2 < 0) {
            node.innerHTML = `<p class="id">${i+1}</p><p class="num">${n1}</p><p class="op">-</p><p class="num">${Math.abs(n2)}</p><p class="op">=</p><p class="result">${result}</p>`
        } else {
            node.innerHTML = `<p class="id">${i+1}</p><p class="num">${n1}</p><p class="op">+</p><p class="num">${Math.abs(n2)}</p><p class="op">=</p><p class="result">${result}</p>`
        };
        problemList.push([node,n1,n2,result,userAnswer]);
    };
    return problemList;
};

function insertProblem(index) {
    //("Inserting problem", index)
    const newNode = problems[index][0];
    newNode.classList.add("animate-in"); // Apply animation
    container.insertAdjacentElement("afterbegin", newNode);
}

function formatProblems() {
    var currentProblems = container.childNodes;
    var adjustedCurrent = currentProblems.length - (currentProblem + 1) // Calculates the index of the currentProblem within currentProblems
    //console.log("ajustedCurrent =", currentProblems.length, "- (", currentProblem, "+ 1 ) =", adjustedCurrent)
    if (started) {
        showHide('show', currentProblems[adjustedCurrent - numBack]) // Show problem at the top
        for (let i = adjustedCurrent - numBack + 1; i <= adjustedCurrent; i++) {
            showHide('hide', currentProblems[i])
        }
        for (let i = adjustedCurrent + 1; i < currentProblems.length; i++) {
            showHide('full', currentProblems[i])
        }

        try {
            const answerCell = currentProblems.item(adjustedCurrent).childNodes[5];
            answerCell.innerHTML = `<input type="number" name="answer" min="0" max="9" id="answer">`;

            const input = document.getElementById("answer");
            input.focus();
            input.addEventListener("input", function () {
                if (input.value !== "") {
                    next();
                } else if (input.value == "-" || input.value == ".") {
                    next(true)
                }
            });
            input.addEventListener("keydown", function (e) {
                if (e === "Enter") {
                    input.value = -1;
                }
            });
        } catch (TypeError) {
            showHide('full', currentProblems[0])
        }
    } else {
        for (let problem of currentProblems) {
            showHide('show', problem)
        }        
    }
}

function showHide(action, node) {
    try {
        let contents = node.childNodes;
        if (action == 'show') {
            const id = contents[0].innerHTML - 1;
            contents[1].innerHTML = problems[id][1];
            if (problems[id][2] < 0) {
                contents[2].innerHTML = "-"
            } else {
                contents[2].innerHTML = "+"
            }
            contents[3].innerHTML = Math.abs(problems[id][2]);
            contents[4].innerHTML = "=";
            contents[5].innerHTML = "?";
        } else if (action == 'hide') {
            contents[1].innerHTML = "?";
            contents[2].innerHTML = "?";
            contents[3].innerHTML = "?";
            contents[5].innerHTML = "?";
        } else if (action == 'full') {
            const id = contents[0].innerHTML - 1;
            contents[1].innerHTML = problems[id][1];
            if (problems[id][2] < 0) {
                contents[2].innerHTML = "-"
            } else {
                contents[2].innerHTML = "+"
            }
            contents[3].innerHTML = Math.abs(problems[id][2]);
            contents[4].innerHTML = "=";
            contents[5].innerHTML = problems[id][4]

            if (problems[id][3] == problems[id][4]) { // Checks if the correct answer is equal to the one the user submitted
                node.className = "correct"
            } else {
                node.className = "incorrect"
            }
        }
    } catch (TypeError) {
        console.log("Unable to show/hide node.")
    }     
}

function next(skip = false) {
    const input = document.getElementById("answer");
    const userAnswer = parseInt(input.value);
    const correctAnswer = problems[currentProblem][3];
    problems[currentProblem][4] = userAnswer // Record the user's answer for comparison later
    //console.log(problems[currentProblem])

    if (skip) {
        problems[currentProblem][4] = " ";
    } else if (userAnswer === correctAnswer) {
        score ++;
        console.log(score);
        scoreDisplay.innerText = `Score: ${score}/${problems.length}`;
    } // Could tag an else statement at the end of this if I ever want to run anything for a wrong answer
    userAnswer.valueOf = ""; // Reset the answer input just in case (I had problems with this before)

    currentProblem++;
    let done = true;
    for (let problem of problems) { // Checks if all questions have been answered by user
        //console.log("!", problem[4])
        if (problem[4] == -1) { // If there are no -1's in the userAnswer slot of a problem, done will remain true
            done = false;
            break;
        }
    }
    //console.log("Done?", done)

    // Only inserts the next visible problem if it exists
    if (currentProblem + numBack < problems.length) {
        insertProblem(currentProblem + numBack);
    }
    formatProblems();

    // End the game when all problems are marked done
    if (done) {
        for (let problem of container.childNodes) {
            showHide('full', problem)
        }
        clearInterval(updateTimer);
        console.log("Score:", score, "/", problems.length);
        console.log("Time:", timer / 100);
        if (score / problems.length >= 0.85) {
            encouragement.style.display = "block"
        }
        timerDisplay.innerText = `Time: ${timer / 100}s`;
        timerDisplay.parentNode.style.display = "flex";
        started = false;
    }
}

// Difficulty logic
function updateDifficultyLabel() {
    label.textContent = difficulties[numBack];
    container.innerHTML = '';
    for (let i = 0; i <= numBack-1; i++) {
        //console.log(problems[i]);
        insertProblem(i);
    };
    formatProblems()
    //console.log(numBack);
}
leftArrow.addEventListener("click", () => {
    numBack = (numBack - 1 + difficulties.length) % difficulties.length;
    updateDifficultyLabel();
});
rightArrow.addEventListener("click", () => {
    numBack = (numBack + 1) % difficulties.length;
    updateDifficultyLabel();
});
updateDifficultyLabel();

// Count Logic (Mostly cut and paste from difficulty logic)
function updateCountLabel() {
    title.textContent = `Calculations x${counts[countIndex]}`;
    countLabel.textContent = "x" + counts[countIndex];
    problems = generateProblems(counts[countIndex]);
    formatProblems();
}

countLeftArrow.addEventListener("click", () => {
    countIndex = (countIndex - 1 + counts.length) % counts.length;
    updateCountLabel();
});

countRightArrow.addEventListener("click", () => {
    countIndex = (countIndex + 1) % counts.length;
    updateCountLabel();
});

updateCountLabel();