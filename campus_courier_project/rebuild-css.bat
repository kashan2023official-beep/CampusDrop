@echo off
tools\tailwindcss.exe -c tailwind.config.js -i tailwind.input.css -o static/css/tailwind.css --minify
echo Tailwind CSS rebuilt. Restart the server and hard-refresh the browser.
