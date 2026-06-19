#!/bin/bash

# Iniciar el proceso de sass --watch en segundo plano
sass --watch assets/sass/main.scss:staticfiles/css/main.css &

# Guardar el PID del proceso sass
SASS_PID=$!

# Iniciar el servidor de desarrollo de Django
python manage.py runserver

# Cuando el servidor de Django se detenga, también detener sass
kill $SASS_PID
