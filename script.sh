#!/bin/sh
LOG="/var/log/app-deploy.log"
PROJECT="django-test"
BRANCH="dev" # master or dev
REPOSITORY="https://github.com/TeaTracer/django-test.git"

teelog() {
    echo $(date -u) "|" $1 | tee -a $LOG
}

teelog "Start deploying."
teelog "Installing APT repositories."

# PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install -y wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# RabbitMQ
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee -a /etc/apt/sources.list.d/rabbitmq.list
wget --quiet -O - https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get autoremove -y
sudo apt-get install -y htop vim git tmux rsync ansible python3-pip

# PostgreSQL
teelog "Installing PostgreSQL."
sudo apt-get install -y postgresql-9.2 pgadmin3
echo "postgres:postgres" | sudo chpasswd

# RabbitMQ
teelog "Installing RabbitMQ."
sudo apt-get install -y rabbitmq-server

# Git
teelog "Downloading git project."
git clone -b $BRANCH $REPOSITORY

# pip requirenments
teelog "Installing requirenments."
(cd $PROJECT && sudo pip3 install -r requirenments.txt)
