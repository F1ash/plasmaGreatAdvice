#!/bin/bash

echo -e `curl -s http://fucking-great-advice.ru/api/random | awk -F \" {'print $8'}` | sed 's/\&nbsp;/ /g' > /dev/shm/$1
