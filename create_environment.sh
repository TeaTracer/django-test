#!/bin/bash
PROJECT="django-test"
LOG="app-deploy.log"
BRANCH="dev" # master or dev
REPOSITORY="https://github.com/TeaTracer/$PROJECT.git"
SESSION=$PROJECT

teelog() {
    echo $(date -u) "|" $1 | tee -a $LOG
}

teelog "Start deploying."

tmux -2 new-session -d -s $SESSION


teelog "Add PostgreSQL APT repository."
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install -y wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

teelog "Add RabbitMQ APT repository."
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee -a /etc/apt/sources.list.d/rabbitmq.list
wget --quiet -O - https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove -y

sudo apt-get install -y htop git vim nginx curl tmux rsync ansible python3-pip

teelog "Installing PostgreSQL."
sudo apt-get install -y postgresql-9.2 pgadmin3 libpq-dev
echo "postgres:postgres" | sudo chpasswd
sudo -u postgres createdb djdb
sudo -u postgres psql -c \
    "CREATE DATABASE djdb; \
     CREATE USER djdb_user WITH PASSWORD 'djdb_password';\
     ALTER ROLE djdb_user SET client_encoding TO 'utf8';\
     GRANT ALL PRIVILEGES ON DATABASE djdb TO djdb_user;"
tmux new-window -t $SESSION:1 -n 'Postgres'
tmux select-pane -t 0
tmux send-keys "sudo -u postgres psql djdb" C-m


teelog "Installing RabbitMQ."
sudo apt-get install -y rabbitmq-server

teelog "Make virtualenv."
sudo pip3 install virtualenv virtualenvwrapper
echo export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 >> ~/.bashrc
echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.bashrc
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source `which virtualenvwrapper.sh`
mkvirtualenv $PROJECT
deactivate

teelog "Installing requirenments."
workon $PROJECT
pip3 install -r ./requirenments.txt

teelog "Django setup"
python $PROJECT/manage.py makemigrations
python $PROJECT/manage.py migrate

teelog "Gunicorn setup"
tmux new-window -t $SESSION:2 -n 'Gunicorn'
tmux select-pane -t 0
tmux send-keys "workon $PROJECT" C-m
tmux send-keys "gunicorn --bind unix:/tmp/gunicorn.sock $PROJECT.wsgi:application " C-m

teelog "Nginx setup"
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
cat ./nginx.conf | sudo tee /etc/nginx/sites-available/default
sudo service nginx restart

teelog "Finish deploying."

tmux select-window -t $SESSION:2

# Attach to session
tmux -2 attach-session -t $SESSION

