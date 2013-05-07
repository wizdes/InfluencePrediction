#!/bin/sh

cp yahoo_stock_data/aapl.csv appl/
mv appl/aapl.csv appl/table.csv

cp yahoo_stock_data/fb.csv fb/
mv fb/fb.csv fb/table.csv

cp yahoo_stock_data/goog.csv goog/
mv goog/goog.csv goog/table.csv

cp yahoo_stock_data/intc.csv intc/
mv intc/intc.csv intc/table.csv

cp yahoo_stock_data/msft.csv msft/
mv msft/msft.csv msft/table.csv

cp csv_test/Facebook.csvtest fb/
mv fb/Facebook.csvtest fb/fb.csv
cp csv_test/Apple.csvtest appl/
mv appl/Apple.csvtest appl/appl.csv
cp csv_test/Google.csvtest goog/
mv goog/Google.csvtest goog/goog.csv
cp csv_test/Intel.csvtest intc/
mv intc/Intel.csvtest intc/intc.csv
cp csv_test/Microsoft.csvtest msft/
mv msft/Microsoft.csvtest msft/msft.csv
