#!/usr/bin/env bash

echo "***********************************************"
echo "-----------------|   install  |----------------"
echo "***********************************************"

echo "***********************************************"
echo "--------------| apt update e upgrade |---------"
echo "***********************************************"

apt-get -y update && apt-get -y upgrade

echo "***********************************************"
echo "---install dependencies (including django)  ---"
echo "***********************************************"

pip3 install --upgrade pip
python3 -m venv laregina
source laregina/bin/activate
pip3 install -r requirements.txt

echo "***********************************************"
echo "--- Running the app  ---"
echo "***********************************************"

python3 manage.py makemigrations
python3 manage.py migrate
