#!/bin/bash
PROJECT="django-test"
BRANCH="deployment-script-test"
REPOSITORY="https://github.com/TeaTracer/$PROJECT.git"

if [ "$#" -ne 1 ] ; then
    exit 1
fi

USER=$1

sudo apt-get install -y git && git clone -b $BRANCH $REPOSITORY && su - $USER -c $PROJECT/create_environment.sh
