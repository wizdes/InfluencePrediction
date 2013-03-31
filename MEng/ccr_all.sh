#!/bin/bash

python ccr.py intc
python ccr.py appl
python ccr.py msft
python ccr.py amzn
python ccr.py fb
python ccr.py goog
python getAvg.py
rm ccr_data.txt
touch ccr_data.txt
