Table of Contents
1) Overview
2) Directories
3) Data
4) How to Run the Data
5) Parsing the results
6) Notes

1) Overview
Our code is designed to work on the Linux operating system. Our source code is cross-platform; however, our SVM executables are compatible with only Linux. To get the executables for Windows or Mac OS X, please use http://svmlight.joachims.org/ to get the most up-to-date SVM executables.

2) Directories
There are two directories: 
AllDataAlgo
WithTwitter

'AllDataAlgo' contains all the source code and executables for the implementation that gathers all the data from the topic/influencer graph and the stock data. This requires all the specific data to be placed in the corresponding directories (detailed in 'Data').

'WithTwitter' contains all the source code and executables for the implementation that gathers data from a particular source; one can isolate the publisher and test with the data gathered from the API.


3) Data

'AllDataAlgo':
Namely, for the code to work in 'AllDataAlgo', it is necessary that all the data to be in the right directories. For an example, if we choose to learn more about Microsoft, the Microsoft data to be in msft/msft.csv (for the topic/influence graph) and msft/table.csv (for the stock data). The table.csv file is from Yahoo's Historical Stock Price API (http://finance.yahoo.com/q/hp?s=#### where #### is the placement for the stock ticker). 
The msft.csv can be retrieved by
- going to Appinions' Topic Exchange (http://platform.appinions.com/topiclist/mytopic/)
- selecting a topic (Microsoft)
- selecting Topic History (Excel)
- creating a new Excel spreadsheet with just the Historical data (Sheet1)
- Save it as a .csv and as msft.csv

Currently, there are 7 directories for the different topics:
msft/
fb/
goog/
intc/
amzn/
appl/
intc/

'WithTwitter'
Simply call 'python webping_bin.py'. This will get the data from the APIs and Yahoo's stock data. The specific companies are specified in 'topic_id_list.txt'. To use a different API key/different start/end date, simply modify the global variables in 'webping_bin.py'. 
The data is saved in save.p (pickled data); if save.p exists in the directory, then its data will be used instead. Simply remove the file to use the web data. The data is saved here so the there are fewer API calls (this is to fall inside the API limits for a developer).
To change the publisher, simply modify the global variable 'publisher' to the desired filtered publisher.

4) How to Run the Data

'AllDataAlgo':
First make sure all the data is in the proper place; please refer to the 'Data' section for more information.

Run "./combine.sh". This is a bash script that will call 'python best_parse.py' #### where #### is the stock name of a particular company and combine all the data together. This will put all the training and testing data in the directory './merge_file' to be used by the SVM.

The SVM can be run by calling:
./svm_learn -c 0.01 ./merge_file/merge_all.train
./svm_classify ./merge_file/merge_all.test svm_model

This will produce the prediction results (also outputted to svm_predictions). To use different kernels, simply attach a different flag to the 'svm_learn' command. For an example, to use the sigmoid tan function, call the svm_learn function as:
./svm_learn -c 0.01 -t 3 ./merge_file/merge_all.train

To calculate the cross co-relation matrix, run the bash script './crr_all.sh'.

To get the kNN data, run the bash script './knnV_parse.sh', then run:
python knn.py merge_file/merge.train merge_file/merge.test

'WithTwitter'
After getting all the data, call the bash script './copySpread.sh'. This will take the data and put it in the correct directories.

Run "./combine.sh". This is a bash script that will call 'python best_parse.py' #### where #### is the stock name of a particular company and combine all the data together. This will put all the training and testing data in the directory './merge_file' to be used by the SVM.

The SVM can be run by calling:
./svm_learn -c 0.01 ./merge_file/merge_all.train
./svm_classify ./merge_file/merge_all.test svm_model

This will produce the prediction results (also outputted to svm_predictions). To use different kernels, simply attach a different flag to the 'svm_learn' command. For an example, to use the sigmoid tan function, call the svm_learn function as:
./svm_learn -c 0.01 -t 3 ./merge_file/merge_all.train

To calculate the cross co-relation matrix, run the bash script './crr_all.sh'.

To get the kNN data, run the bash script './knnV_parse.sh', then run:
python knn.py merge_file/merge.train merge_file/merge.test


5) Parsing the results

All the results will be in standard output. For SVMs, more detailed results are displayed in svm_predictions file that is produced.

6) Notes


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



