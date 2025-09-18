// ---------- Настройка режимов ----------
const modes = {
    "Pomodoro": { work: 5*60, break: 5*60 },  // тестовые короткие таймеры
    "Свой": { work: 30*60, break: 10*60 },
    "40/15": { work: 40*60, break: 15*60 },
    "52/17": { work: 52*60, break: 17*60 },
    "90/20": { work: 90*60, break: 20*60 },
};

let timer = modes["Pomodoro"].work;
let isWork = true;
let interval;

// ---------- Элементы ----------
const timeDisplay = document.querySelector(".time");
const workBtn = document.querySelector(".control-btn:nth-child(1)");
const breakBtn = document.querySelector(".control-btn:nth-child(2)");
const tabs = document.querySelectorAll(".tab");

// ---------- Обновление дисплея ----------
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

// ---------- Отправка уведомления ----------
function sendTelegramNotification(message) {
    fetch("https://9aa26e6a295a.ngrok-free.app/notify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    }).catch(err => console.error("Ошибка уведомления:", err));
}


// ---------- Таймер ----------
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
                console.log("Рабочий таймер завершён!");
                sendTelegramNotification("Рабочий таймер завершён! Время отдыха 🧘");
                isWork = false;
                timer = modes[activeTab].break;
                updateDisplay();
                startTimer(); // запускаем таймер отдыха автоматически
            } else {
                console.log("Отдых завершён!");
                sendTelegramNotification("Отдых завершён! Возвращаемся к работе 🚀");
                isWork = true;
                timer = modes[activeTab].work;
                updateDisplay();
            }
        }
    }, 1000);
}

// ---------- Обработчики ----------
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
