#!/bin/bash
# sync ssh key file to remote servers automatically
# Author: cuberub@gmail.com
# Date: 2013
list=""
while read line
do
  export list="$list $line"
done
for machine in ${list}
do
  echo "=====sync to server:$machine===="
  echo ~/.ssh/id_rsa $machine:~/.ssh/
  scp ~/.ssh/id_rsa $machine:~/.ssh/
  echo ~/.ssh/id_rsa.pub $machine:~/.ssh/
  scp ~/.ssh/id_rsa.pub $machine:~/.ssh/
done
