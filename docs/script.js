// ---------- Настройка режимов ----------
const modes = {
    "Pomodoro": { work: 5*1, break: 5*1 },
    "Свой": { work: 30*60, break: 10*60 },
    "40/15": { work: 40*60, break: 15*60 },
    "52/17": { work: 52*60, break: 17*60 },
    "90/20": { work: 90*60, break: 20*60 },
};

let timer = modes["Pomodoro"].work; // стартовый таймер
let isWork = true; // true — работа, false — отдых
let interval;

// ---------- Элементы ----------
const timeDisplay = document.querySelector(".time");
const workBtn = document.querySelector(".control-btn:nth-child(1)");
const breakBtn = document.querySelector(".control-btn:nth-child(2)");
const tabs = document.querySelectorAll(".tab");

// ---------- Обновление дисплея и кнопок ----------
function updateDisplay() {
    const minutes = Math.floor(timer / 60);
    const seconds = timer % 60;
    timeDisplay.textContent = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;

    document.querySelector(".timer").style.background = isWork
        ? "radial-gradient(circle, rgba(255,0,0,0.4), rgba(255,0,0,0) 70%)"
        : "radial-gradient(circle, rgba(0,128,0,0.4), rgba(0,128,0,0) 70%)";

    if (isWork) {
        workBtn.classList.add("active");
        breakBtn.classList.remove("active");
    } else {
        workBtn.classList.remove("active");
        breakBtn.classList.add("active");
    }
}

// ---------- Отправка уведомления на Flask ----------
function sendTelegramNotification(message) {
    fetch("https://c875eb190f6a.ngrok-free.app/notify", {  // публичный ngrok URL
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    }).catch(err => console.error("Ошибка уведомления:", err));
}

// ---------- Запуск таймера ----------
function startTimer() {
    clearInterval(interval);
    interval = setInterval(() => {
        if (timer > 0) {
            timer--;
            updateDisplay();
        } else {
            clearInterval(interval);

            const activeTab = document.querySelector(".tab.active")?.textContent || "Pomodoro";

            if (isWork) {
                // 1️⃣ Уведомление о завершении работы
                sendTelegramNotification("Рабочий таймер завершён! Время отдыха 🧘");

                // 2️⃣ Переключаем на отдых и запускаем таймер
                isWork = false;
                timer = modes[activeTab].break;
                updateDisplay();
                startTimer(); // запуск таймера отдыха
            } else {
                // 3️⃣ Уведомление о завершении отдыха
                sendTelegramNotification("Отдых завершён! Возвращаемся к работе 🚀");

                // 4️⃣ Переключаем на работу, но таймер не запускаем автоматически
                isWork = true;
                timer = modes[activeTab].work;
                updateDisplay();
            }
        }
    }, 1000);
}

// ---------- Обработчики вкладок ----------
tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        const selectedMode = tab.textContent;
        timer = modes[selectedMode].work;
        isWork = true;
        clearInterval(interval);
        updateDisplay();
    });
});

// ---------- Обработчики кнопок ----------
workBtn.addEventListener("click", startTimer);
breakBtn.addEventListener("click", () => {
    const activeTab = document.querySelector(".tab.active")?.textContent || "Pomodoro";
    timer = modes[activeTab].break;
    isWork = false;
    updateDisplay();
    startTimer();
});

// ---------- Инициализация ----------
updateDisplay();
