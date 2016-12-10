#!/bin/bash
PROJECT = "django-test"
BRANCH = "deployment-script-test"
REPOSITORY = "https://github.com/TeaTracer/$PROJECT.git"

sudo apt-get install -y git && git clone -b $BRANCH $REPOSITORY && $PROJECT/create_environment.sh
