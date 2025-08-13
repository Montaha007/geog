@echo off
echo ===============================================
echo  Smart for Green - Fire Detection System
echo  Stopping all services...
echo ===============================================

echo [1/3] Stopping Docker containers...
echo Stopping Redis container (kind_wu)...
docker stop kind_wu

echo Stopping Go2RTC container (go2rtc)...
docker stop go2rtc

echo [2/3] Stopping Python processes...
taskkill /f /im python.exe /t 2>nul
taskkill /f /im celery.exe /t 2>nul
taskkill /f /im uvicorn.exe /t 2>nul

echo [3/3] Closing command windows...
taskkill /f /im cmd.exe /fi "WindowTitle eq Django ASGI*" 2>nul
taskkill /f /im cmd.exe /fi "WindowTitle eq Camera Service*" 2>nul
taskkill /f /im cmd.exe /fi "WindowTitle eq Fire Detection*" 2>nul
taskkill /f /im cmd.exe /fi "WindowTitle eq Notifications*" 2>nul

echo.
echo ===============================================
echo  All services stopped successfully!
echo ===============================================
pause
