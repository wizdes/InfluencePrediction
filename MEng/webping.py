import urllib2
import re

# global val
appkey = 'chvarnqqng32t34y236qw582'
start = '02-01-2013'
end = '04-13-2013'

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
	try:
		inf_filter_req = urllib2.Request(inf_filter_str)
		response = urllib2.urlopen(inf_filter_req)
		the_page = response.read()
		# print the_page
	except:
		print "Error from Influencer API"
		print "topic id: ", topic_id
	id_lst = [pair[1] for pair in re.findall(r'("id":)"([\w-]+)"', the_page)]
	# print id_lst
	return id_lst

# get influencer score history for a topic using influencer score history method
def get_inf_history(topic_id, inf_id):
	inf_history_str =('http://api.appinions.com/influencer/score/influencers/history?topicid={0}&influencerid={1}'+\
					  '&offset=0&limit=100&appkey={2}').format(topic_id, inf_id, appkey).strip()
	# req = 'http://api.appinions.com/influencer/score/influencers/history?topicid=58524714-852d-4569-ad5a-c70f1f5b414b&influencerid=5deff3e4-1210-46d8-ade0-22fad673cfee&offset=0&limit=100&appkey=chvarnqqng32t34y236qw582'
	try:
		print inf_history_str
		inf_history_req = urllib2.Request(inf_history_str)
		response = urllib2.urlopen(inf_history_req)
		the_page = response.read()
		# print the_page
	
	except:
		print "Error from Influencer API"
		print "topic id: ", topic_id
		print "influencer id:", inf_id


	history = re.findall(r'"date":"([\d-]+)","sentiment":([\d.]+),"score":([\d.]+),"volume":([\d.]+)', the_page)
	inf_history_dic = {}
	for tuple in history:
		inf_history_dic[tuple[0]] = [tuple[1:]]
	return inf_history_dic

topic_id_dic = topic_id_import('topic_id_list.txt')
'''
# main methods test
inf_id_lst = get_inf_id(topic_id_dic['Google'], start, end)
samp_inf_history = get_inf_history(topic_id_dic['Google'], 'bc670322-fcd5-45c3-a9f0-7edffb47af9f')
print samp_inf_history# ['2013-04-01']
'''
topic_dic = {}
for topic, topic_id in topic_id_dic.iteritems():
	inf_lst = get_inf_id(topic_id, start, end)
	print "current topic:", topic
	print "current topic id: ", topic_id
	influncer_dic = {}
	for influencer in inf_lst:
		print "current influencer id: ", influencer
		influncer_dic[influencer] = get_inf_history(topic_id, influencer)
	topic_dic[topic] = influncer_dic
# test main
print topic_dic['Amazon']['bc670322-fcd5-45c3-a9f0-7edffb47af9f']['2013-04-01']



