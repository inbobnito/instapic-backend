heroku ps:scale web=1
web:
    python manage.py db init
    python manage.py db migrate -m "initial"
    python manage.py db upgrade
    python manage.py run 0.0.0.0:5000
