#!/bin/bash
source venv/bin/activate
cd video_server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver