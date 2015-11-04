#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR} 
/usr/bin/git pull
cd -
sleep 5
${DIR}/alive.py &
${DIR}/server.py &
