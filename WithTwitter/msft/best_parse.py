import sys
import random

def read_file(filename):
	fp = open(filename)
	lines = fp.readlines()
	fp.close()
	return lines

def read_influence_file(filename):
	lines = read_file(filename)
	matrix = []
	for line in lines:
		matrix.append(line.split(","))
	num_entries = 61
	inf_dict = {}
	iter = 1
	yesterday_info = (0,0,0)
	while iter != num_entries:
		date = matrix[0][iter][0:5]
		date = date.replace("/", "")
		#print str(iter) + " HI "
		#print date
		#print matrix[1][iter]
		#print yesterday_info[0]
		#print matrix[2][iter]
		#print yesterday_info[1]
		#print matrix[3][iter]
		#print yesterday_info[2]

		inf_dict[date] = (matrix[1][iter], matrix[2][iter], matrix[3][iter], float(matrix[1][iter]) - float(yesterday_info[0]), float(matrix[2][iter]) - float(yesterday_info[1]), float(matrix[3][iter]) - float(yesterday_info[2]))
		yesterday_info = (matrix[1][iter], matrix[2][iter], matrix[3][iter])
		iter += 1
	return inf_dict

def read_volume_data():
	lines = read_file("table.csv")
	volume_dict = {}
	for line in lines:
		elements = line.split(",")
		if elements[5] == "Volume": continue
		date = elements[0][5:]
		date = date.replace("-", "")
		#print date
		volume = (int) (elements[5])
		volume_dict[date] = volume
	return volume_dict

def create_data(v_dic, i_dic):
	predict_dates = sorted(v_dic.keys())
	influence_data = sorted(i_dic.keys())
	yesterday_volume = 0
	yesterday_datum = ""
	data_array = []
	for datum in influence_data:
		if yesterday_datum in v_dic and datum in v_dic:
			result = 1
			if(v_dic[datum] - v_dic[yesterday_datum] < 0) : result = -1
			data_array.append(str(result) + " 1:" + i_dic[yesterday_datum][0] + " 2:" + i_dic[yesterday_datum][1] + " 3:" + i_dic[yesterday_datum][2] + " 4:" + str(i_dic[yesterday_datum][3]) + " 5:" + str(i_dic[yesterday_datum][4]) + " 6:" + str(i_dic[yesterday_datum][5]) )
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
			data_array.append(str(result) + " 1:" + str(cumulative_data[0]) + " 2:" + str(cumulative_data[1]) + " 3:" + str(cumulative_data[2]) + " 4:" + str(cumulative_data[3]) + " 5:" + str(cumulative_data[4]) + " 6:" + str(cumulative_data[5]) )
		yesterday_datum = datum
	return data_array

if __name__ == "__main__":
	stock_name = "msft"
	stock_name = sys.argv[1]
	file_name = stock_name + ".csv"
	train_name = stock_name + ".train"
	test_name = stock_name + ".test"
	results = create_data(read_volume_data(), read_influence_file(file_name))

	train_file = open(train_name, 'w')
	test_file = open(test_name, 'w')
	iter = (float)(len(results)) * .8
	prob = 0.6
	for line in results:
		if random.random() < prob: train_file.write(line + "\n")
		else:  test_file.write(line + "\n")
		iter -= 1
	train_file.close()
	test_file.close()
	