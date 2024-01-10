cd video_server
python3 manage.py makemigrations users
python3 manage.py migrate users
python3 manage.py makemigrations videos
python3 manage.py migrate videos
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser