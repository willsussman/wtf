#!/bin/sh

./raw.sh &

python3 ../collect/server.py --port 1122 &