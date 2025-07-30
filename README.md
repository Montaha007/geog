# 🌾 Smart Farm Watcher

**Smart Farm Watcher** is a web-based platform designed to help farmers monitor and manage their lands through an intuitive and interactive map interface. It allows each user to create and visualize geospatial data (polygons and markers) and view live camera streams—all while ensuring user-specific data isolation.

---

## 🌍 Key Features

### 🗺️ Interactive Map Interface

* Built with **Leaflet** and **leaflet.draw**
* Users can draw and save **polygons** and **markers**
* Each user sees only **their own saved locations**
* Locations are accessible via the **"Your Saved Locations"** menu

### 📹 Camera Management

* Add cameras by providing a **custom name** , an **RTSP link** and **CAM ID**
* **Live stream preview** is available instantly after saving
* Real-time streaming powered by **[go2rtc](https://github.com/AlexxIT/go2rtc)** for **low-latency video**

### ⚡ Asynchronous Backend

* Built with **Django** (async-enabled)
* Designed for **real-time data flow** and **live camera integration**

---

## ⚙️ Tech Stack

* **Backend**: Django 5.2.1 (Python 3.12.6, Async Support)
* **Frontend**: HTML, CSS, JavaScript
* **Streaming**: [go2rtc](https://github.com/AlexxIT/go2rtc)
* **Libraries & Tools**:

  * [Leaflet](https://leafletjs.com/)
  * [Leaflet.draw](https://github.com/Leaflet/Leaflet.draw)
  * [GDAL](https://gdal.org/)
  * [FFmpeg](https://ffmpeg.org/) *(optional for processing)*

---

## 🚀 Roadmap

* ✅ **YOLO AI Fire Detection** — Real-time fire detection on camera feeds
* ✅ **Smart Notification System** — Alerts when risks or fires are detected

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.12.6
* Django 5.2.1
* GDAL
* go2rtc
* FFmpeg *(if additional processing is needed)*

### 📦 Install System Dependencies (Ubuntu Example)

```bash
sudo apt update
sudo apt install gdal-bin ffmpeg python3-dev python3-pip
```

### 📁 Clone the Repository

```bash
git clone https://github.com/your-username/smart-farm-watcher.git
cd smart-farm-watcher
```

### 🐍 Install Python Packages

```bash
pip install -r requirements.txt
```

### ⚙️ Setup the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 👤 Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### ▶️ Run the Development Server

#### Option 1: Standard (Synchronous)

```bash
python manage.py runserver
```

#### Option 2: Async (ASGI-compatible)

```bash
uvicorn mysite.asgi:application --reload
```

---

## 💡 Notes

* Video streams are **instantly available** using go2rtc — no initialization delay.
* Saved map features and camera positions are fully isolated per user.
* The platform is in **active development** with more real-time features coming soon.

---

## 🧠 Purpose-Driven Innovation

**Smart Farm Watcher** brings together geospatial tools, real-time video, and AI to help modern farmers monitor, protect, and optimize their fields like never before.

