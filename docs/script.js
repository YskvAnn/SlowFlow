// 1. Настройка режимов и начальных переменных
const modes = {
    "Pomodoro": { work: 25*60, break: 5*60 },
    "Свой": { work: 30*60, break: 10*60 },
    "40/15": { work: 40*60, break: 15*60 },
    "52/17": { work: 52*60, break: 17*60 },
    "90/20": { work: 90*60, break: 20*60 },
};

let time = 3 * 1; // стартовое время таймера
let timerInterval;
let isWork = true; // true — рабочий таймер, false — отдых

const timeDisplay = document.querySelector('.time');
const startBtn = document.querySelector('.control-btn.active');

// 2. Функция обновления дисплея
function updateDisplay() {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    timeDisplay.textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

    if (isWork) {
        document.querySelector('.timer').style.background =
            "radial-gradient(circle, rgba(255,0,0,0.4), rgba(255,0,0,0) 70%)";
    } else {
        document.querySelector('.timer').style.background =
            "radial-gradient(circle, rgba(0,128,0,0.4), rgba(0,128,0,0) 70%)";
    }
}

// 3. Переключение подсветки кнопок
function switchButtons() {
    const workBtn = document.querySelector('.control-btn:nth-child(1)');
    const breakBtn = document.querySelector('.control-btn:nth-child(2)');

    if (isWork) {
        workBtn.classList.add('active');
        breakBtn.classList.remove('active');
    } else {
        breakBtn.classList.add('active');
        workBtn.classList.remove('active');
    }
}

// 4. Функция запуска таймера
function startTimer() {
    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (time > 0) {
            updateDisplay();
            time--;
        } else {
            // Когда дошли до 0 — переключаем режим
            const activeTab = document.querySelector('.tab.active')?.textContent || "Pomodoro";

            if (isWork) {
                isWork = false;
                time = modes[activeTab].break;
            } else {
                isWork = true;
                time = modes[activeTab].work;
            }

            updateDisplay();
            switchButtons(); // переключаем подсветку кнопок
        }
    }, 1000);
}

// 5. Обработчики вкладок
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const selectedMode = tab.textContent;
        time = modes[selectedMode].work;
        isWork = true;
        clearInterval(timerInterval);
        updateDisplay();
        switchButtons();
    });
});

// 6. Обработчики кнопок
startBtn.addEventListener('click', startTimer);

// 7. Инициализация дисплея
updateDisplay();
switchButtons();
