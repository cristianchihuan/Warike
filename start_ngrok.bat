@echo off
echo Starting ngrok for Peruvian Warike Flask app...
echo This will expose your local server at http://localhost:5000 to the internet
echo.
ngrok http 5000
pause 