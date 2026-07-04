<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C853,100:00BCD4&height=220&section=header&text=Office%20Power%20Monitor&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35"/>

# ⚡ Office Power Monitor

### Smart IoT-Based Office Energy Monitoring & Device Management System

<p align="center">
<img src="https://readme-typing-svg.demolab.com?font=Poppins&weight=600&size=24&pause=1000&color=00C853&center=true&vCenter=true&width=750&lines=Smart+Office+Energy+Monitoring;FastAPI+%7C+Arduino+%7C+Telegram+Bot;Real-Time+Power+Analytics;IoT-Based+Device+Control"/>
</p>

<p align="center">

<img src="https://img.shields.io/github/stars/sajjadul404/Office-Power-Monitor?style=for-the-badge"/>

<img src="https://img.shields.io/github/forks/sajjadul404/Office-Power-Monitor?style=for-the-badge"/>

<img src="https://img.shields.io/github/issues/sajjadul404/Office-Power-Monitor?style=for-the-badge"/>

<img src="https://img.shields.io/github/license/sajjadul404/Office-Power-Monitor?style=for-the-badge"/>

</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"/>

<img src="https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white"/>

<img src="https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white"/>

<img src="https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white"/>

<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black"/>

<img src="https://img.shields.io/badge/WebSocket-black?style=flat-square"/>

<img src="https://img.shields.io/badge/Telegram_Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white"/>

</p>

</div>

---

# 📖 About

**Office Power Monitor** is a Smart IoT-Based Office Energy Monitoring System designed to monitor, analyze, and control office electrical devices in real time.

The project integrates **IoT hardware**, a **FastAPI backend**, a **Web Dashboard**, and a **Telegram Bot** to provide intelligent power monitoring and efficient energy management.

---

# ✨ Key Features

- ⚡ Live Power Monitoring
- 🔌 Smart Device Control
- 📊 Interactive Dashboard
- 📈 Energy Analytics
- 🤖 Telegram Bot Support
- 🌐 REST API
- 🔄 WebSocket Live Updates
- 📡 IoT Device Integration
- 🚨 Power Notifications
- 📱 Responsive Interface

---

# 🏛️ System Architecture

```text
                    +----------------------+
                    |    IoT Sensors       |
                    |  Arduino / ESP32     |
                    +----------+-----------+
                               │
                               │
                         Sensor Data
                               │
                               ▼
                  +-------------------------+
                  |     FastAPI Backend     |
                  +-----------+-------------+
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
      Dashboard UI                  Telegram Bot
               │                             │
               └──────────────┬──────────────┘
                              ▼
                     Office Administrators
```

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| IoT | Arduino / ESP32 |
| API | REST API |
| Communication | WebSocket |
| Bot | Telegram Bot |
| Version Control | Git & GitHub |

---

# 📁 Project Structure

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

### Clone Repository

```bash
git clone https://github.com/sajjadul404/Office-Power-Monitor.git

cd Office-Power-Monitor
```

---

### Backend

```bash
cd office-monitor/backend

python -m venv .venv

source .venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

### Telegram Bot

```bash
cd office-monitor/bot

pip install -r requirements.txt

python bot.py
```

---

# 📊 Components

- Backend API
- Dashboard
- Telegram Bot
- IoT Communication
- Energy Analytics
- Device Controller
- Notification Service

---

# 🎯 Objectives

- Reduce unnecessary electricity consumption
- Monitor devices in real time
- Improve office energy efficiency
- Enable remote power control
- Deliver live energy analytics

---

# 📸 Preview

### Dashboard

> Replace this with your dashboard screenshot.

```text
preview/dashboard.png
```

### System Diagram

```text
diagrams/system-diagram.svg
```

---

# 📈 Future Enhancements

- 📱 Mobile App
- ☁ Cloud Deployment
- 🤖 AI Energy Prediction
- 📊 Monthly Reports
- 🌍 Multi Office Support
- 🔔 Smart Automation
- 📡 MQTT Integration

---

# 🤝 Contributing

Contributions are welcome!

```bash
Fork Repository

Create Feature Branch

Commit Changes

Push Branch

Open Pull Request
```

---

# 📄 License

This project is intended for educational and research purposes.

---

<div align="center">

### ⭐ Don't forget to Star this repository!

<img src="https://github-readme-stats.vercel.app/api?username=sajjadul404&show_icons=true&theme=tokyonight"/>

<br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=sajjadul404&theme=tokyonight"/>

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C853,100:00BCD4&height=120&section=footer"/>

Made with ❤️ by **Sajjadul Islam**

</div>