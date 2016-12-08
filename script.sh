#!/bin/sh
LOG="/var/log/app-deploy.log"
PROJECT="django-test"
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
# sudo apt-get upgrade -y
# sudo apt-get autoremove -y

sudo apt-get install -y htop vim git tmux rsync ansible python3-pip

teelog "Installing PostgreSQL."
sudo apt-get install -y postgresql-9.2 pgadmin3
echo "postgres:postgres" | sudo chpasswd

teelog "Installing RabbitMQ."
sudo apt-get install -y rabbitmq-server

teelog "Downloading git project."
git clone -b $BRANCH $REPOSITORY

teelog "Installing requirenments."
(cd $PROJECT && sudo pip3 install -r requirenments.txt)

teelog "Finish deploying."
