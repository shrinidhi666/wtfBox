#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}
git pull
python ${DIR}/syncServer/aliveServer.py &
python ${DIR}/syncClient/client.py &

