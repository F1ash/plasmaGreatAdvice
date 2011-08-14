#!/bin/bash

/usr/bin/printf "$(echo -e `curl -s http://fucking-great-advice.ru/api/random | awk -F \" {'print $8'}` | sed 's/\&nbsp;/ /g' | sed 's/\&#151;/ - /g')" > /dev/shm/$1
