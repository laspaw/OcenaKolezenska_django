call .\venv\Scripts\activate.bat
python manage.py check
python manage.py migrate

rem python manage.py loaddata fixtures/semester.json
python manage.py loaddata fixtures/gradescale.json
python manage.py loaddata fixtures/grade.json
pause	

