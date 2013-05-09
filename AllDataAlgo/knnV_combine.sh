#!/bin/sh

python knnV_parse.py msft
python knnV_parse.py appl
python knnV_parse.py fb
python knnV_parse.py intc
cat msft/msft.train appl/appl.train fb/fb.train intc/intc.train >merge_file/merge.train
cat msft/msft.test appl/appl.test fb/fb.test intc/intc.test >merge_file/merge.test


