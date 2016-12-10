#!/bin/bash

# Example:
# ./sync dev
# ./sync dev /home/vagrant/special_folder/

# dev - host in ~/.ssh/config with user, port and andress
# use vagrant ssh-config dev >> ~/.ssh/config to get it

if [ "$#" -eq 0 ] ; then
    exit 1
fi

if [ "$#" -eq 1 ] ; then
    FOLDER="/home/vagrant"
fi

if [ "$#" -eq 2 ] ; then
    FOLDER="$2"
fi
FROM=$(pwd)
TO="$1:$FOLDER"

rsync -avz --no-perms --no-owner --no-group --exclude=".vagrant/" --exclude=".git/" $FROM $TO

