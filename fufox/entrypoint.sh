#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
sleep 0.1
done

echo "PostgreSQL started"
sleep 2
# pay attention to the --no-input
#https://stackoverflow.com/a/41950907/9378427
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py shell -c "from users.models import CustomUser; CustomUser.objects.create_superuser('er', 'admin@example.com', 'djangoproject1')"

exec "$@"
