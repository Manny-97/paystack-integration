release: python manage.py makemigrations
release: python manage.py migrate
web gunicorn paystackpay.wsgi:application --log-file -