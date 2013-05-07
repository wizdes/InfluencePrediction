#!/bin/sh

python best_parse.py amzn
python best_parse.py msft
python best_parse.py appl
python best_parse.py fb
python best_parse.py goog
python best_parse.py intc
cat amzn/amzn.train msft/msft.train appl/appl.train fb/fb.train goog/goog.train intc/intc.train >merge_file/merge.train
cat amzn/amzn.test msft/msft.test appl/appl.test fb/fb.test goog/goog.test intc/intc.test >merge_file/merge.test


