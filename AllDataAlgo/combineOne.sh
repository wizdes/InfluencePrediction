#!/bin/sh

python best_parseOne.py amzn
python best_parseOne.py msft
python best_parseOne.py appl
python best_parseOne.py fb
python best_parseOne.py goog
python best_parseOne.py intc
cat amzn/amzn.train msft/msft.train appl/appl.train fb/fb.train goog/goog.train intc/intc.train >merge_file/merge.train
cat amzn/amzn.test msft/msft.test appl/appl.test fb/fb.test goog/goog.test intc/intc.test >merge_file/merge.test


