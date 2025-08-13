@echo off
echo ===============================================
echo  Smart for Green - Fire Detection System
echo  Starting all services...
echo ===============================================

REM Change to project directory
cd /d "c:\Users\Mattoussi\OneDrive\Documents\smart for green\geo"

echo [1/6] Activating virtual environment...
call myvenv\Scripts\activate

echo [2/6] Starting Docker containers...
echo Starting Redis container (kind_wu)...
docker start kind_wu
timeout /t 2

echo Starting Go2RTC container (go2rtc)...
docker start go2rtc
timeout /t 3

echo [3/6] Starting Django ASGI server...
start "Django ASGI Server" cmd /k "title Django ASGI && myvenv\Scripts\activate && uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000"
timeout /t 5

echo [4/6] Starting Camera Stream Service...
start "Camera Stream Service" cmd /k "title Camera Service && myvenv\Scripts\activate && python -m camera_stream_service.main"
timeout /t 3

echo [5/6] Starting Fire Detection Celery Worker...
start "Fire Detection Worker" cmd /k "title Fire Detection && myvenv\Scripts\activate && celery -A fire_detection_service.fire_detector worker --loglevel=info --pool=solo"
timeout /t 3

echo [6/6] Starting Notification Service...
start "Notification Service" cmd /k "title Notifications && myvenv\Scripts\activate && python -m notification_service.notification"
timeout /t 2

echo.
echo ===============================================
echo  All services started successfully!
echo ===============================================
echo.
echo Services running:
echo  - Redis (Docker): localhost:6379
echo  - Go2RTC (Docker): localhost:1984
echo  - Django ASGI: localhost:8000
echo  - Camera Stream Service
echo  - Fire Detection Worker
echo  - Notification Service
echo.
echo Press any key to open system monitoring...
pause

REM Open system monitoring
echo Opening system monitoring...
start "" http://localhost:8000
start "" http://localhost:1984

echo System is ready!
pause
