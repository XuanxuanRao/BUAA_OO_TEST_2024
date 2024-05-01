@echo off
:loop
echo "\n" | .\main.exe
timeout /t 5 >nul
goto loop