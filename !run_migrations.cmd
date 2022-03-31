call .\venv\Scripts\activate.bat
python manage.py makemigrations
python manage.py showmigrations
pause
python manage.py migrate
pause	

