// 1. Настройка режимов и начальных переменных
const modes = {
    "Pomodoro": { work: 5, break: 3 },   // для теста короткие таймеры
    "Свой": { work: 4, break: 2 },
    "40/15": { work: 6, break: 3 },
    "52/17": { work: 5, break: 2 },
    "90/20": { work: 7, break: 3 },
};

let time = 5; // стартовое время таймера
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

// 4. Функция для отправки уведомлений через Flask сервер
function sendTelegramNotification(text) {
    fetch("http://127.0.0.1:5000/notify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
    }).catch(err => console.error("Ошибка уведомления:", err));
}

// 5. Функция запуска таймера
function startTimer() {
    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (time > 0) {
            updateDisplay();
            time--;
        } else {
            const activeTab = document.querySelector('.tab.active')?.textContent || "Pomodoro";

            if (isWork) {
                isWork = false;
                time = modes[activeTab].break;
                sendTelegramNotification("Рабочий таймер завершён! Время отдыха 🧘");
            } else {
                isWork = true;
                time = modes[activeTab].work;
                sendTelegramNotification("Отдых закончился! Возвращаемся к работе 🚀");
            }

            updateDisplay();
            switchButtons();
        }
    }, 1000);
}

// 6. Обработчики вкладок
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

// 7. Обработчики кнопок
startBtn.addEventListener('click', startTimer);

// 8. Инициализация дисплея
updateDisplay();
switchButtons();
