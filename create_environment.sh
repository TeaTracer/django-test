#!/bin/bash
PROJECT="django-test"
LOG="$PROJECT/app-deploy.log"
BRANCH="dev" # master or dev
REPOSITORY="https://github.com/TeaTracer/$PROJECT.git"

teelog() {
    echo $(date -u) "|" $1 | tee -a $LOG
}

teelog "Start deploying."

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

sudo apt-get install -y htop vim nginx curl tmux rsync ansible python3-pip

teelog "Installing PostgreSQL."
sudo apt-get install -y postgresql-9.2 pgadmin3
echo "postgres:postgres" | sudo chpasswd

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
pip3 install -r $PROJECT/requirenments.txt
deactivate

teelog "Finish deploying."
