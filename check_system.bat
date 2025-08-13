@echo off
echo ===============================================
echo  Smart for Green - System Status Check
echo ===============================================

echo Checking Docker containers...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter name=kind_wu
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter name=go2rtc

echo.
echo Checking Python processes...
tasklist /fi "imagename eq python.exe" /fo table 2>nul | findstr /i python
tasklist /fi "imagename eq uvicorn.exe" /fo table 2>nul | findstr /i uvicorn
tasklist /fi "imagename eq celery.exe" /fo table 2>nul | findstr /i celery

echo.
echo Checking ports...
netstat -an | findstr :8000
netstat -an | findstr :6379
netstat -an | findstr :1984

echo.
echo System URLs:
echo  - Django App: http://localhost:8000
echo  - Go2RTC Web: http://localhost:1984
echo  - Redis: localhost:6379
echo.
pause
