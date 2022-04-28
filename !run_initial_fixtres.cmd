call .\venv\Scripts\activate.bat
python manage.py check
python manage.py migrate

python manage.py loaddata fixtures/semester.json
python manage.py loaddata fixtures/gradescale.json
python manage.py loaddata fixtures/grade.json
python manage.py loaddata fixtures/teacher.json

pause	

