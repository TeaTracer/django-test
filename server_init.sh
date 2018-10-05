#!/bin/bash
PROJECT="django-test"
BRANCH="dev"
REPOSITORY="https://github.com/TeaTracer/$PROJECT.git"

case "$#" in
    "0")
        GET_PROJECT_FROM='--local'
    ;;
    "1")
        GET_PROJECT_FROM=$1
    ;;
    *)
    exit 1
    ;;
esac

case "$GET_PROJECT_FROM" in
    "-r" | "--remote")
        sudo apt-get install -y git && git clone -b $BRANCH $REPOSITORY && cd $PROJECT && ./create_environment.sh
        ;;
    "-l" | "--local")
        ./create_environment.sh
        ;;
esac

