#!/bin/bash
set -eup pipefail
trap 's=$?; echo "$0: Error on line $LINENO: $BASH_COMMAND"; exit ${s}' ERR
IFS=$'\n\t'

uvicorn main:app --reload & 

cd ./pytodo-frontend
npm run start &

wait