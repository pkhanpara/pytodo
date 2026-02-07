#!/bin/bash
set -eup pipefail
trap 's=$?; echo "$0: Error on line $LINENO: $BASH_COMMAND"; exit ${s}' ERR
IFS=$'\n\t'

echo "starting backend"
uvicorn main:app --host 0.0.0.0 --reload & 

echo "starting frontend"
cd ./pytodo-frontend
npm run start &

wait
