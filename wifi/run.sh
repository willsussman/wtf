#!/bin/sh

python3 raw.py &

python3 ../collect/server.py --port 1122 &