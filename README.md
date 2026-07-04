<div align="center">

# ⚡ Office Power Monitor

### Smart IoT-Based Office Energy Monitoring & Device Management System

<p align="center">
Monitor • Analyze • Control • Save Energy
</p>

<p align="center">
<img src="https://readme-typing-svg.herokuapp.com?font=Poppins&size=24&pause=1000&color=00C853&center=true&vCenter=true&width=700&lines=Smart+Office+Energy+Monitoring;IoT+Based+Power+Management;FastAPI+%7C+Arduino+%7C+Telegram+Bot;Real-time+Device+Monitoring" />
</p>

<p align="center">
<img src="https://img.shields.io/github/stars/sajjadul404/Office-Power-Monitor?style=for-the-badge">
<img src="https://img.shields.io/github/forks/sajjadul404/Office-Power-Monitor?style=for-the-badge">
<img src="https://img.shields.io/github/license/sajjadul404/Office-Power-Monitor?style=for-the-badge">
<img src="https://img.shields.io/github/repo-size/sajjadul404/Office-Power-Monitor?style=for-the-badge">
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white"/>
<img src="https://img.shields.io/badge/WebSocket-010101?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Telegram_Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white"/>
</p>

</div>

---

# 📖 About

**Office Power Monitor** is a Smart IoT-Based Office Energy Monitoring and Device Control System designed to reduce electricity consumption through real-time monitoring, analytics, and remote device management.

The project combines **IoT Hardware**, **FastAPI Backend**, **Interactive Dashboard**, and **Telegram Bot** into one centralized platform for efficient office power management.

---

# ✨ Features

- ⚡ Real-Time Power Monitoring
- 🔌 Smart Device Control
- 📊 Live Dashboard
- 📈 Energy Analytics
- 🤖 Telegram Bot Integration
- 📡 IoT Sensor Communication
- 🌐 REST API
- 🔄 WebSocket Live Updates
- 🚨 Instant Notifications
- 📱 Responsive Interface

---

# 🏗 System Architecture

```text
        +------------------+
        |   IoT Devices    |
        | Arduino / ESP32  |
        +--------+---------+
                 |
                 |
          Sensor Data
                 |
                 ▼
       +------------------+
       | FastAPI Backend  |
       +------------------+
          |          |
          |          |
          ▼          ▼
 Dashboard        Telegram Bot
          |
          ▼
     Office Users
```

---

# 🛠 Tech Stack

| Layer | Technologies |
|--------|--------------|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| IoT | Arduino / ESP32 |
| Communication | REST API, WebSocket |
| Notification | Telegram Bot |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
Office-Power-Monitor
│
├── office-monitor
│   ├── backend
│   ├── bot
│   ├── dashboard
│   ├── diagrams
│   └── preview
│
├── dashboard-preview.html
├── system-diagram.svg
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/sajjadul404/Office-Power-Monitor.git

cd Office-Power-Monitor
```

---

## Backend

```bash
cd office-monitor/backend

python -m venv .venv

source .venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Telegram Bot

```bash
cd office-monitor/bot

pip install -r requirements.txt

python bot.py
```

---

# 📊 Modules

- Backend API
- Dashboard
- Telegram Bot
- Device Controller
- Energy Monitoring
- Power Analytics
- Notification Service
- IoT Communication

---

# 🎯 Objectives

✔ Reduce electricity waste

✔ Monitor office devices in real-time

✔ Automate power management

✔ Improve energy efficiency

✔ Remote monitoring & control

---

# 📸 Screenshots

### Dashboard

> Add dashboard screenshots here.

```
preview/dashboard.png
```

### System Diagram

```
diagrams/system-diagram.svg
```

---

# 📈 Future Improvements

- AI-based Power Prediction
- Smart Scheduling
- Monthly Reports
- Mobile Application
- Cloud Deployment
- MQTT Integration
- Multi-Office Support

---

# 🤝 Contributing

Contributions are welcome!

```bash
Fork Repository

Create New Branch

Commit Changes

Push Branch

Create Pull Request
```

---

# 📜 License

This project is developed for educational and research purposes.

---

<div align="center">

### ⭐ Star this repository if you found it useful!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C853,100:00BCD4&height=120&section=footer"/>

Made with ❤️ by **Sajjadul Islam**

</div>