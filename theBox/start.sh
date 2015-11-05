#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

sleep 10
killall pppd
sleep 5 && /usr/sbin/pppd debug call /root/dlink/bin/linux_dial
sleep 10
cd ${DIR} 
/usr/bin/git pull
cd -
sleep 5
${DIR}/alive.py &
${DIR}/server.py &
