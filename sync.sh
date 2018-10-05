#!/bin/bash

# Example:
# ./sync dev
# ./sync dev /home/vagrant/special_folder/

# dev - host in ~/.ssh/config with user, port and andress
# use vagrant ssh-config dev >> ~/.ssh/config to get it

case "$#" in
    "0")
        exit 1
    ;;
    "1")
        FOLDER="/home/vagrant"
    ;;
    "2")
        FOLDER="$2"
    ;;
    *)
    exit 1
    ;;
esac

FROM=$(pwd)
TO="$1:$FOLDER"

rsync -avz --no-perms --no-owner --no-group --exclude=".vagrant/" --exclude=".git/" $FROM $TO

