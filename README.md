mkdir ProjectName
cd ProjectName
python3 venv venv
venv/bin/activate
pip3 install Django django-admin
django-admin startproject ProjectName .
django-admin startapp AppName
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata --format=json --app=TestCase TestCase/country.json
python3 manage.py runserver
