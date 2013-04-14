import urllib2
import re
<<<<<<< HEAD
import sys
import pickle
import time

=======
import difflib
import time
>>>>>>> fixed webpage query timeout issue
# global val
#appkey = 'chvarnqqng32t34y236qw582'
appkey = 'cjvgsbragwdyncddda3ujmw8'
start = '02-01-2013'
end = '04-13-2013'
pickleData = None

try:
	pickleData = pickle.load( open( "save.p", "rb" ) )
except:
	print "no pickle data!"
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
		time.sleep(1.5)
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
<<<<<<< HEAD
	# req = 'http://api.appinions.com/influencer/score/influencers/history?topicid=58524714-852d-4569-ad5a-c70f1f5b414b&influencerid=5deff3e4-1210-46d8-ade0-22fad673cfee&offset=0&limit=100&appkey=chvarnqqng32t34y236qw582'
	the_page = ""

=======

	req = 'http://api.appinions.com/influencer/score/influencers/history?topicid=1a6e48b2-ca1e-4316-9804-a70cdbb1c013&influencerid=5bf28adf-3c9e-4e3a-a86d-ce2bbf77dd1b&offset=0&limit=100&appkey=chvarnqqng32t34y236qw582'
	'''
	s = difflib.SequenceMatcher(a=inf_history_str, b=req).get_matching_blocks()
	print s
	print inf_history_str[207:], '   ', req[207:]
	print len(inf_history_str)
	print len(req)
	'''
>>>>>>> fixed webpage query timeout issue
	try:
		time.sleep(1.5)
		print inf_history_str
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
	# print history
	inf_history_dic = {}
	for tuple in history:
		inf_history_dic[tuple[0]] = [tuple[1:]]
	return inf_history_dic

<<<<<<< HEAD
topic_dic = pickleData

if type(pickleData) == None:
	topic_id_dic = topic_id_import('topic_id_list.txt')
	'''
	# main methods test
	inf_id_lst = get_inf_id(topic_id_dic['Google'], start, end)
	samp_inf_history = get_inf_history(topic_id_dic['Google'], 'bc670322-fcd5-45c3-a9f0-7edffb47af9f')
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
		topic_dic[topic] = influncer_dic
	print 'num requests:' + str(num_requests)
=======
topic_id_dic = topic_id_import('topic_id_list.txt')
# print topic_id_dic
'''
# main methods test
inf_id_lst = get_inf_id(topic_id_dic['Google'], start, end)
samp_inf_history = get_inf_history(topic_id_dic['Google'], 'bc670322-fcd5-45c3-a9f0-7edffb47af9f')
print samp_inf_history# ['2013-04-01']
'''
topic_dic = {}
for topic, topic_id in topic_id_dic.iteritems():
	inf_lst = get_inf_id(topic_id, start, end)
	# print inf_lst
	print "current topic:", topic
	print "current topic id: ", topic_id
	influncer_dic = {}
	for influencer in inf_lst:
		# print "current influencer id: ", influencer
		influncer_dic[influencer] = get_inf_history(topic_id, influencer)
	topic_dic[topic] = influncer_dic
>>>>>>> fixed webpage query timeout issue
# test main
#print topic_dic['Amazon']
#pickle this data
if pickleData == None:
	pickle.dump( topic_dic, open( "save.p", "wb" ) )

#get all the days
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
print printDates

dates = sorted(dates)
printDates = sorted(printDates)

stocks = ["amzn", "appl", "fb", "goog", "intc", "msft"]

avgData = {}
for index, topic in enumerate(topic_dic):
	features = {}#a single topic: Amazon
	featuresNum = {}
	print topic_dic[topic]
	for inf in topic_dic[topic]:
		for day in dates:
			features[day] = [0,0,0]
			featuresNum[day] = [0,0,0]
			for iterElt in [0,1,2]:
				if iterElt not in features[day] : features[day][iterElt] = 0
				#print topic_dic[topic][inf][day][0][iterElt]
				try:
					features[day][iterElt] += float(topic_dic[topic][inf][day][0][iterElt])
					featuresNum[day][iterElt] += 1
				except:
					continue
	#for day in dates:
		#for iterElt in [0,1,2]:
			#print len(topic_dic[topic])
			#features[day][iterElt] = features[day][iterElt]*1.0/len(topic_dic[topic])
			#print features[day][iterElt]
	avgData[stocks[index]] = features

# create the average for each day
#print them for each day
for elt in avgData:
	line1 = ","
	line2 = ","
	line3 = ","
	line4 = ","
	eltVals = avgData[elt]
	for iter, day in enumerate(dates):
		line1 += printDates[iter] + ","
		line2 += str(eltVals[day][0]) + ","
		line3 += str(eltVals[day][1]) + ","
		line4 += str(eltVals[day][2]) + ","
	printFile = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n"
	print elt + "/" + elt +".csvtest"
	f = open(elt +".csvtest", 'w')
	f.write(printFile)

for stock in stocks:
	urlrequeststr = "http://ichart.finance.yahoo.com/table.csv?s=" + stock + "&a=01&b=13&c=2013&d=03&e=19&f=2013&g=d&ignore=.csv"
	print urlrequeststr
	req = urllib2.Request(urlrequeststr)
	response = urllib2.urlopen(req)
	response = response.read()
	f = open("table.csv", 'w')
	f.write(response)
	f.close()
	sys.exit(-1)
#get the stock for each guy (and print)
#run the prediction algorithm



