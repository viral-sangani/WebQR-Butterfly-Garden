for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do set NetworkIP=%%a
echo Network IP: %NetworkIP%
echo %NetworkIP%:8000 > ../IP-ADDRESS-TO-OPEN-IN-BROWSER.txt
python ../manage.py runserver %NetworkIP%:8000
pause
