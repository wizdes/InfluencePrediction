InfluencePrediction
===================

This is used for influence prediction

All the raw data is in the directory with the stock's name on it:
msft/
fb/
goog/
intc/
amzn/
appl/
intc/

best_parse.py - This parses the data for all the different stock and puts it all together into merge_file/
	Every time you run it, it generates a new set of training and test data (this is randomized, so you get different results all the time.)

combine.py - I also wrote a shell script that runs best_parse.py on all the different stocks. Read this script to see how to call best_parse.py.

After the data is in merge_file/, run:
./svm_learn merge_file/merge.train svm.model to learn the data; then run:
./svm_classify  merge_file/merge.test svm.model

best_parse.py has a "read_volume_data" function that reads the stock data and gets the volume data. I think you can extract your features in this function; it also has a "create_data" function that creates the SVM data; this works by putting each line into "enter_str" and then appending it to the data_array array. The data_array is then written out to the merge_file/ to either the test or train file.

====================

Updated (03/11/2013):

- Combined the features of stock volume and influence prediction, the new parsing file is combined_parse.py
- Can run shell script merge_all.sh to generate merge_all.train and merge_all.test for svm in merge_file folder
- tested result with svm_light, the accuracy for linear kernel is 54.26% and accuracy for radial kernel is 45%



