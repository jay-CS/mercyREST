#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/jay-CS/mercyREST.git'

PROJECT_BASE_PATH='/usr/local/apps/mercyREST'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python3-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip3 install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip3 install wheel
$PROJECT_BASE_PATH/env/bin/pip3 install uwsgi==2.0.18

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python3 manage.py migrate
$PROJECT_BASE_PATH/env/bin/python3 manage.py collectstatic --noinput

# Configure supervisor
cp $PROJECT_BASE_PATH/deploy/supervisor_mercyApp.conf /etc/supervisor/conf.d/mercyApp.conf
supervisorctl reread
supervisorctl update
supervisorctl restart mercyREST

# Configure nginx
cp $PROJECT_BASE_PATH/deploy/nginx_mercyApp.conf /etc/nginx/sites-available/mercyApp.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/mercyApp.conf /etc/nginx/sites-enabled/mercyApp.conf
systemctl restart nginx.service

echo "DONE! :)"
