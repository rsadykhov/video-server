#!/bin/bash
apt-get install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip3 install django==4.1
pip3 install pandas==2.0
pip3 install gunicorn==21.2
apt-get install -y nginx
apt-get install supervisor -y
