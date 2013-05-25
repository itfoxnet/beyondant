#!/bin/bash
# check remote server status automatically
# Author: cuberub@gmail.com
# Date: 2013

list=""
while read line
do
  export list="$list $line"
done
for machine in ${list}
do
  echo "=====server:$machine===="
  ssh $machine "free -g; echo ; vmstat; echo; top -b -n 1 | head -n 5;"
done
