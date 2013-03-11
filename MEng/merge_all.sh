#!/bin/sh

python combined_parse.py amzn
python combined_parse.py msft
python combined_parse.py appl
python combined_parse.py fb
python combined_parse.py goog
python combined_parse.py intc
cat amzn/amzn.train msft/msft.train appl/appl.train fb/fb.train goog/goog.train intc/intc.train >merge_file/merge_all.train
cat amzn/amzn.test msft/msft.test appl/appl.test fb/fb.test goog/goog.test intc/intc.test >merge_file/merge_all.test


