$env:HTTP_PROXY = 'http://127.0.0.1:7890'
$env:HTTPS_PROXY = 'http://127.0.0.1:7890'
& 'C:\Users\dbao0\market_monitor\venv\Scripts\python.exe' 'C:\Users\dbao0\market_monitor\monitor.py'
pause
