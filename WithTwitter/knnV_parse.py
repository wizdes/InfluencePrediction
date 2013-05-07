import sys
import random

import csv
import datetime

smoothing = True

def read_file(filename):
	fp = open(filename)
	lines = fp.readlines()
	fp.close()
	return lines

def smoothed_matrix(matrix):
	for enum in [1,2,3]:
		list_feature = [0,0,0,0,0,0,0]
		sum_count = [0,0,0,0,0,0,0]
		for index, elt in enumerate(matrix[enum]):
			if index == 0: continue
			list_feature[index % 7] += float(matrix[enum][index])
			sum_count[index % 7] += 1
		total_sum = 0
		total_count = 0
		for elt in list_feature : total_sum += elt
		for elt in sum_count : total_count += elt
		all_average = total_sum * 1.0 / total_count
		for index, elt in enumerate(list_feature) : list_feature[index] = list_feature[index] * 1.0/ sum_count[index]
		avg_avg = all_average * 1.0 / 7.0
		for index, elt in enumerate(list_feature) : list_feature[index] = list_feature[index] * 1.0/ avg_avg
		for index, elt in enumerate(matrix[enum]):
			if index == 0: continue
			matrix[enum][index] = float(matrix[enum][index]) * 1.0 #/ list_feature[index % 7]
	return matrix

def read_influence_file(filename, apply_smoothing):
	lines = read_file(filename)
	matrix = []
	for line in lines:
		line = line.strip()
		matrix.append(line.split(","))
	num_entries = 61
	inf_dict = {}
	iter = 1
	yesterday_info = (0,0,0)

	if apply_smoothing:
		matrix = smoothed_matrix(matrix)

	while iter != num_entries:
		date = matrix[0][iter][5:10]
		date = date.replace("/", "")
		inf_dict[date] = (matrix[1][iter], matrix[2][iter], matrix[3][iter], float(matrix[1][iter]) - float(yesterday_info[0]), float(matrix[2][iter]) - float(yesterday_info[1]), float(matrix[3][iter]) - float(yesterday_info[2]))
		yesterday_info = (matrix[1][iter], matrix[2][iter], matrix[3][iter])
		iter += 1
	return inf_dict

# read csv file for stock volume features
def csv_read(dir):
	num_entries = 64
	file_path = dir + "/" + "table.csv"
	volume_book = {}
	with open(file_path,'rb') as f_in:
		reader = csv.reader(f_in)
		cnt = 1
		for row in reader:
			#print row[0]
			if(row[0] != 'Date'):
				_date = datetime.datetime.strptime(row[0],'%Y-%m-%d').date()
				#if(_date < datetime.date(2012,12,20)):
				if(cnt == num_entries):
					break
				volume_book[_date] = int(row[5])
				cnt += 1
	return volume_book

def read_volume_data(dir):
	lines = read_file(dir + "/" + "table.csv")
	volume_dict = {}
	week_based_avg = [0,0,0,0,0]
	week_based_count =[0,0,0,0,0]
	total_avg = 0
	total_count = 0
	for line in lines:
		elements = line.split(",")
		if elements[5] == "Volume": continue
		date = elements[0][5:]
		date = date.replace("-", "")
		#print date
		volume = (int) (elements[5])
		volume_dict[date] = volume
		total_avg += volume
		total_count += 1
		week_based_avg[int(date)%5] += int(volume)
		week_based_count[int(date)%5] += 1
	for index, elt in enumerate(week_based_count):
		week_based_avg[index] = week_based_avg[index] * 1.0/week_based_count[index]
	total_avg = total_avg * 1.0/total_count
	for key, value in volume_dict.items():
		volume_dict[key] = int(volume_dict[key]) * 1.0 * total_avg / week_based_avg[int(key)%5]
	return volume_dict

def create_data(v_dic, i_dic, volume_book):
	predict_dates = sorted(v_dic.keys())
	influence_data = sorted(i_dic.keys())
	yesterday_volume = 0
	yesterday_datum = ""
	saved_enter_str = ""

	data_array = []
	for datum in influence_data:
		if yesterday_datum in v_dic and datum in v_dic:
			result = 1
			if(v_dic[datum] - v_dic[yesterday_datum] < 0) : result = -1
			enter_str = str(result) + " 1:" + str(i_dic[yesterday_datum][0]) + " 2:" + str(i_dic[yesterday_datum][1]) + " 3:" + str(i_dic[yesterday_datum][2]) + " 4:" + str(i_dic[yesterday_datum][3]) + " 5:" + str(i_dic[yesterday_datum][4]) + " 6:" + str(i_dic[yesterday_datum][5]) 
			#enter_str = str(result) + " 1:" + str(i_dic[yesterday_datum][0]) + " 2:" + str(i_dic[yesterday_datum][1]) + " 3:" + str(i_dic[yesterday_datum][3]) + " 4:" + str(i_dic[yesterday_datum][4])
			data_array.append(enter_str)
		elif datum in v_dic:
			if yesterday_datum == "":
				yesterday_datum = datum
				continue
			ptr_datum = yesterday_datum
			#cumulative_data = v_dic[yesterday_datum]
			cumulative_data = (0.0,0.0,0.0,0.0,0.0,0.0)
			while ptr_datum not in v_dic:
				cumulative_data = (cumulative_data[0] + float(i_dic[ptr_datum][0]),cumulative_data[1] + float(i_dic[ptr_datum][1]),cumulative_data[2] + float(i_dic[ptr_datum][2]),cumulative_data[3] + float(i_dic[ptr_datum][3]),cumulative_data[4] + float(i_dic[ptr_datum][4]),cumulative_data[5] + float(i_dic[ptr_datum][5]))
				ptr_datum = str(int(ptr_datum) - 1)
				if len(ptr_datum) == 3 : ptr_datum = "0" + ptr_datum 
			result = 1
			if(v_dic[datum] - v_dic[ptr_datum] < 0) : result = -1
			enter_str = str(result) + " 1:" + str(cumulative_data[0]) + " 2:" + str(cumulative_data[1]) + " 3:" + str(cumulative_data[2]) + " 4:" + str(cumulative_data[3]) + " 5:" + str(cumulative_data[4]) + " 6:" + str(cumulative_data[5]) 
			#enter_str = str(result) + " 1:" + str(cumulative_data[0]) + " 2:" + str(cumulative_data[1]) + " 3:" + str(cumulative_data[3]) + " 4:" + str(cumulative_data[4])
			data_array.append(enter_str)
		yesterday_datum = datum

	############################################################################################
	# feature set for stock volume output
	output = []
	start_date = min(volume_book.keys())
	second_start_data = min(dt for dt in volume_book.keys() if dt > start_date)
	third_start_data = min(dt for dt in volume_book.keys() if dt > second_start_data)
	for today in sorted(volume_book.keys()):
		#volume_data = []
		str_out = ""
		if(today != start_date and today != second_start_data and today != third_start_data):
			yesterday = max(dt for dt in volume_book.keys() if dt < today)
			db_yesterday = max(dt for dt in volume_book.keys() if dt < yesterday)
			tb_yesterday = max(dt for dt in volume_book.keys() if dt < db_yesterday)
			# calculate target value
			'''
			if(volume_book[today] >= volume_book[yesterday]):
				str_out = str_out + '+1'
			else:
				str_out = str_out + '-1'
			'''
			# first feature: yesterday's volume
			str_out += ' 7:'
			str_out += str(volume_book[yesterday])
			# second feature: day before yesterday's volume
			str_out += ' 8:'
			str_out += str(volume_book[db_yesterday])
			# third feature: volume three days ago
			str_out += ' 9:'
			str_out += str(volume_book[tb_yesterday])
			# 4th feature: delta of previous two features
			str_out += ' 10:'
			str_out += str(volume_book[yesterday] - volume_book[db_yesterday])
			# 5th feature: delta of two-day ago and three-day ago volume
			str_out += ' 11:'
			str_out += str(volume_book[db_yesterday] - volume_book[tb_yesterday])
			# 6th feature: average of previous two days' volume
			str_out += ' 12:'
			str_out += str((volume_book[yesterday] + volume_book[db_yesterday])/2.0)
			# 7th feature: average of two-day ago and three-day ago volume
			str_out += ' 13:'
			str_out += str((volume_book[db_yesterday] + volume_book[tb_yesterday])/2.0)
			# str_out += '\n'
		output.append(str_out)
	for k, v in enumerate(data_array):
		data_array[k] = v + output[k]
		#print data_array[k]

	return data_array

if __name__ == "__main__":
	stock_name = "msft"
	stock_name = sys.argv[1]
	file_name = stock_name + "/" + stock_name + ".csv"
	train_name = stock_name + "/" + stock_name + ".train"
	test_name = stock_name + "/" + stock_name + ".test"
	volume_book = csv_read(stock_name)
	results = create_data(read_volume_data(stock_name), read_influence_file(file_name, smoothing), volume_book)

	train_file = open(train_name, 'w')
	test_file = open(test_name, 'w')
	iter = 0
	prob = 0.25
	for line in results:
		if len(line) > 2:
			if random.random() < prob or iter < 0.80 * len(results): train_file.write(line + "\n")
			else:  test_file.write(line + "\n")
		iter += 1
	train_file.close()
	test_file.close()
	
