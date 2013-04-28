import urllib2
import re
import sys
import pickle
import time
import csv
import datetime
import random
from subprocess import *
from collections import defaultdict

# global val
appkey = 'chvarnqqng32t34y236qw582'
# appkey = 'cjvgsbragwdyncddda3ujmw8'
start = '02-22-2013'
end = '04-22-2013'
pickleData = None
C = 1

def stock_data_parse(filename):
	global start
	global end
	volume_book = {}
	start_date = datetime.datetime.strptime(start,'%m-%d-%Y').date()
	end_date = datetime.datetime.strptime(end,'%m-%d-%Y').date()
	with open(filename,'rb') as f_in:
		reader = csv.reader(f_in)
		for row in reader:
			#print row[0]
			if(row[0] != 'Date'):
				_date = datetime.datetime.strptime(row[0],'%Y-%m-%d').date()
				#print _date, start_date, end_date
				#print _date >= start_date
				if(_date >= start_date and _date <= end_date):
					volume_book[_date] = int(row[5])
	target_val = {}
	trading_days = []
	# start_date = min(volume_book.keys())
	for today in volume_book.keys():
		if(today != start_date):
			yesterday = max(dt for dt in volume_book.keys() if dt < today)
		# calculate target value
		str_today = today.strftime('%Y-%m-%d')
		if(volume_book[today] >= volume_book[yesterday]):
			target_val[str_today] = '+1'
		else:
			target_val[str_today] = '-1'
		if(today != start_date):
			trading_days.append(str_today)
	return (target_val, sorted(trading_days))

def get_volume_movement(topic_id_dic):
	svm_target = {}
	# topic_id_dic = topic_id_import('topic_id_list.txt')
	for stock in topic_id_dic.keys():
		urlrequeststr = "http://ichart.finance.yahoo.com/table.csv?s=" + stock + "&a=01&b=13&c=2013&d=03&e=19&f=2013&g=d&ignore=.csv"
		print urlrequeststr
		req = urllib2.Request(urlrequeststr)
		response = urllib2.urlopen(req)
		response = response.read()
		stock_filename = "yahoo_stock_data/"+stock+".csv"
		f = open(stock_filename, 'w')
		f.write(response)
		f.close()
		svm_target[stock], trading_days= stock_data_parse(stock_filename)
	print svm_target['msft']['2013-04-01']
	print trading_days
	return svm_target, trading_days
#print pickleData
# get topic id from file
def topic_id_import(filename):
	topic_in = open(filename, 'r')
	topic_id_dic = {}
	for line in topic_in:
		topic_id_dic[line.split(':')[0]] = line.split(':')[1].strip()
	# print topic_id_dic
	return topic_id_dic

# get list of influencer id from topic using influencer filter
def get_inf_id(topic_id, start, end):
	start_date = start
	end_date = end
	inf_filter_str =('http://api.appinions.com/influencer/influencersearch/{0}/.json?offset=0&limit=100'+\
					 '&publisher=twitter&start_date={1}&end_date={2}&appkey={3}').format(topic_id, start_date, end_date, appkey)
	# req = 'http://api.appinions.com/influencer/influencersearch/58524714-852d-4569-ad5a-c70f1f5b414b/.json?offset=0&limit=100&publisher=twitter&start_date=02-01-2013&end_date=04-12-2013&appkey=chvarnqqng32t34y236qw582'
	# print inf_filter_str
	# print req
	the_page = ""
	try:
		inf_filter_req = urllib2.Request(inf_filter_str)
		response = urllib2.urlopen(inf_filter_req)
		the_page = response.read()
		#sleep(500)
		# print the_page
	except:
		print "Error from Influencer API"
		print "topic id: ", topic_id
		#sys.exit(-1)
	id_lst = [pair[1] for pair in re.findall(r'("id":)"([\w-]+)"', the_page)]
	# print id_lst
	return id_lst

# get influencer score history for a topic using influencer score history method
def get_inf_history(topic_id, inf_id):
	inf_history_str =('http://api.appinions.com/influencer/score/influencers/history?topicid={0}&influencerid={1}'+\
					  '&offset=0&limit=100&appkey={2}').format(topic_id, inf_id, appkey).strip()
	# req = 'http://api.appinions.com/influencer/score/influencers/history?topicid=58524714-852d-4569-ad5a-c70f1f5b414b&influencerid=5deff3e4-1210-46d8-ade0-22fad673cfee&offset=0&limit=100&appkey=chvarnqqng32t34y236qw582'
	the_page = ""

	try:
		# print inf_history_str
		inf_history_req = urllib2.Request(inf_history_str)
		response = urllib2.urlopen(inf_history_req)
		the_page = response.read()
		#sleep(500)
		# print the_page
	
	except:
		print "Error from Influencer API"
		print "topic id: ", topic_id
		print "influencer id:", inf_id
		#sys.exit(-1)


	history = re.findall(r'"date":"([\d-]+)","sentiment":([\d.]+),"score":([\d.]+),"volume":([\d.]+)', the_page)
	# print "history: ", history
	inf_history_dic = {}
	for tuple in history:
		inf_history_dic[tuple[0]] = list(tuple[1:])
	# print "dic val: ", inf_history_dic.values()
	return inf_history_dic

def API_data_retrieve():
	global pickleData
	try:
		pickleData = pickle.load( open( "save.p", "rb" ) )
		print "Reading saved data ---"
	except:
		print "no pickle data!"

	# test = get_inf_history('1a6e48b2-ca1e-4316-9804-a70cdbb1c013', '2b5a0749-c957-4a56-acc9-0173dd674bb9')

	topic_dic = pickleData
	#print "here"
	#print pickleData == None
	if pickleData == None:
		topic_dic = {}
		topic_id_dic = topic_id_import('topic_id_list.txt')
		'''
		# main methods test
		inf_id_lst = get_inf_id(topic_id_dic['goog'], start, end)
		samp_inf_history = get_inf_history(topic_id_dic['goog'], 'bc670322-fcd5-45c3-a9f0-7edffb47af9f')
		print samp_inf_history# ['2013-04-01']
		'''

		num_requests = 0
		for topic, topic_id in topic_id_dic.iteritems():
			inf_lst = get_inf_id(topic_id, start, end)
			print "current topic:", topic
			print "current topic id: ", topic_id
			influncer_dic = {}
			for influencer in inf_lst:
				print "current influencer id: ", influencer
				time.sleep(0.7)
				influncer_dic[influencer] = get_inf_history(topic_id, influencer)
				num_requests += 1
				print num_requests
			topic_dic[topic] = influncer_dic
		print 'num requests:' + str(num_requests)
	#pickle this data
	if pickleData == None:
		pickle.dump( topic_dic, open( "save.p", "wb" ) )
	return topic_dic

# get all the days in influencer data
def get_dates(topic_dic):
	dates = []
	#print topic_dic
	firstElt = topic_dic.values()[0].values()[0]
	#print firstElt
	for elt in firstElt.keys():
		dates.append(elt)
	#print dates
	printDates = []
	for elt in dates:
		printDates.append(elt.replace("-", "/"))

	dates = sorted(dates)
	printDates = sorted(printDates)
	print printDates
	return (dates, printDates)

# For each stock, get average sentiment, score and volume each day as features
def get_avg_data(topic_dic, dates):
	avgData = {}
	for index, topic in enumerate(topic_dic):
		print "in avg data, current topic: ", topic
		features = {}#a single topic: Amazon
		featuresNum = {}
		bin_score_feature ={}
		bin_score_num_feature = {}
		# print topic_dic[topic]
		for inf in topic_dic[topic]:
			for day in dates:
				features[day] = [0,0,0]
				featuresNum[day] = [0,0,0]
				bin_score_feature[day] = {}
				bin_score_num_feature[day] = {}
				# initialize bin dictionary for each day
				for i in range(11):
					bin_score_feature[day][i] = [0,0,0]
					bin_score_num_feature[day][i] = [0,0,0]
				# get binned data based on influencer score for each day
				try:
					bin_num = min(10,int(float(topic_dic[topic][inf][day][1])/10))
					# print "passed"
				except:
					# print "failed topic: ", topic
					continue
				# get sum and count of data for each day
				for iterElt in [0,1,2]:
					if iterElt not in features[day] : features[day][iterElt] = 0
					#print topic_dic[topic][inf][day][0][iterElt]
					try:
						#print "test:  value = ", topic_dic[topic][inf][day][0]# [iterElt]
						features[day][iterElt] += float(topic_dic[topic][inf][day][iterElt])
						featuresNum[day][iterElt] += 1
						bin_score_feature[day][bin_num][iterElt] += float(topic_dic[topic][inf][day][iterElt])
						bin_score_num_feature[day][bin_num][iterElt] += 1
					except:
						# print "failed in avg: ", topic
						continue
		for day in dates:
			# print "Number of influencer for topic ", topic, "is ", len(topic_dic[topic])
			for iterElt in [0,1,2]:
				if(featuresNum[day][iterElt] != 0):
					features[day][iterElt] = float(features[day][iterElt])/featuresNum[day][iterElt]
				else:
					features[day][iterElt] = 0
				# print "avg is ", features[day][iterElt]
			for i in range(11):
				for iterElt in [0,1,2]:
					if(bin_score_num_feature[day][i][iterElt] != 0):
						bin_score_feature[day][i][iterElt] = float(bin_score_feature[day][i][iterElt])/bin_score_num_feature[day][i][iterElt]
					else:
						bin_score_feature[day][i][iterElt] = 0
		avgData[topic] = [features, bin_score_feature]
	return avgData


# trading_days and inf_days should be in sorted order starting from earlier days
def svm_gen(target, trading_days, avg_data, inf_days):
	svm_out = []
	# make sure all trading days has the data in the day before
	if(trading_days[0] == inf_days[0]):
		trading_days = trading_days[1:]
	for trading_day in trading_days:
		date_today = trading_day
		date_yesterday = inf_days[inf_days.index(trading_day)-1]
		for topic in target:
			svm_line = target[topic][date_today]
			f_index = 1
			# make sure features in order
			for company in sorted(avg_data.keys()):
				# use absolute avg data (not delta) as feature values
				avg_features, bin_score_feature = avg_data[company]
				# today's avg features
				for index, val in enumerate(avg_features[date_today], start = f_index):
					if(val > 0):
						svm_line = svm_line + ' ' + str(index) + ':' + str(round(val,4))
				f_index = index + 1
				# yesterday's avg features
				for index, val in enumerate(avg_features[date_yesterday], start = f_index):
					if(val > 0):
						svm_line = svm_line + ' ' + str(index) + ':' + str(round(val,4))
				f_index = index + 1
				# binned features of today
				for bin in sorted(bin_score_feature[date_today].keys()):
					for index, val in enumerate(bin_score_feature[date_today][bin], start = f_index):
						if(val > 0):
							svm_line = svm_line + ' ' + str(index) + ':' + str(round(val,4))
					f_index = index + 1
				# binned features of yesterday
				for bin in sorted(bin_score_feature[date_yesterday].keys()):
					for index, val in enumerate(bin_score_feature[date_yesterday][bin], start = f_index):
						if(val > 0):
							svm_line = svm_line + ' ' + str(index) + ':' + str(round(val,4))
					f_index = index + 1
			svm_out.append(svm_line)
	return svm_out

def svm_run(svm_lst):
	global C
	random.shuffle(svm_lst)
	split = int(len(svm_lst) * 0.7)
	train_out_lst = svm_lst[:split]
	test_out_lst = svm_lst[split:]
	train_out = ""
	test_out = ""
	for each in train_out_lst:
		train_out += each
		train_out += '\n'
	for each in test_out_lst:
		test_out += each
		test_out += '\n'
	svm_train_out = open("twitter_train.svm",'w')
	svm_test_out = open("twitter_test.svm",'w')
	svm_train_out.write(train_out)
	svm_test_out.write(test_out)

	train_file = 'twitter_train.svm'
	test_file = 'twitter_test.svm'
	model_file = 'model'
	predict_file = 'predict'
	svm_learn = 'svm_light/svm_learn'
	svm_classify = 'svm_light/svm_classify'
	cmd = '%s -c %.4f %s %s' %(svm_learn,C, train_file, model_file)
	print('Training...')
	call(cmd,shell=True,cwd='/Users/ccrjohn/Dropbox/Spring 2013/CS 5999/API parse')

	cmd = '%s %s %s %s' %(svm_classify,test_file,model_file,predict_file)
	print('Testing...')
	call(cmd,shell=True,cwd='/Users/ccrjohn/Dropbox/Spring 2013/CS 5999/API parse')

# ------------------ main ------------------ #
topic_dic = API_data_retrieve()
topic_id_dic = topic_id_import('topic_id_list.txt')
# special treatment since amazon was broke at the time of query
del topic_dic['Amazon']
del topic_id_dic['amzn']
# get all the days
dates, printDates = get_dates(topic_dic)
# For each stock, get average sentiment, score and volume each day as features
avgData = get_avg_data(topic_dic, dates)
# get the binary movement of stock volume each day
svm_target, trading_days = get_volume_movement(topic_id_dic)
# generate svm formated data in list
svm_lst = svm_gen(svm_target, trading_days, avgData, dates)
# run svm and get accuracy
svm_run(svm_lst)



# create the average for each day
#print them for each day
for elt in avgData:
	line1 = ","
	line2 = ","
	line3 = ","
	line4 = ","
	eltVals = avgData[elt]
	# print "stock is ", elt
	try:
		for iter, day in enumerate(dates):
			line1 += printDates[iter] + ","
			line2 += str(eltVals[0][day][0]) + ","
			line3 += str(eltVals[0][day][1]) + ","
			line4 += str(eltVals[0][day][2]) + ","
		printFile = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n"
		print elt + "/" + elt +".csvtest"
		f = open("csv_test/"+elt +".csvtest", 'w')
		f.write(printFile)
	except:
		print "Failed stock: ", elt




