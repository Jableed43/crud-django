#!/usr/bin/env bash
# exit on error
set -o errexit

#Los requirements son creados pip freeze > requeriments.txt
#Instala las dependencias necesarias que se encuentran en build.sh

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate