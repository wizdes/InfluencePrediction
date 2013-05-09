import sys

lines = []
inf_data = []
prev_delta = []
filename = "calc.csv"

def read_data():
  read_lines_array = []
  file_handler = open(filename, 'r')
  for read_buffer in file_handler:
    read_buffer = read_buffer.strip()
    read_lines_array.append(read_buffer.split(','))
  #print read_lines_array
  return read_lines_array

def fix_weekends(lines):
  inf_buffer = []
  for line in lines:
    #print len(lines[0])
    buffer = []
    iter = 0
    while iter < len(line):
      #print lines[5][iter]
      if int(lines[5][iter]) == 1:
	buffer[len(buffer) - 1] += float(line[iter])
      elif int(lines[4][iter]) == 0 : 
	buffer.append(float(line[iter]))
      else:
	if(iter + 2 < len(line) ): combine = float(line[iter]) + float(line[iter + 1]) + float(line[iter + 2])
	else: combine = float(line[iter])
	iter += 2
	buffer.append(combine)
      iter += 1
    inf_buffer.append(buffer)
    #print len(buffer)
  return inf_buffer
  
def gen_prev_delta(inf_data):
  prev_delta_buffer = []
  for index, data_set in enumerate(inf_data):
    if index > 2 : continue
    prev_buffer = []
    delta_buffer = []
    for index, elt in enumerate(data_set):
      if index == 0:
	prev_buffer.append(elt)
	delta_buffer.append(elt)
      else:
	prev_buffer.append(data_set[index - 1])
	#print str(data_set[index - 1]) + " " + str(elt)
	delta_buffer.append(elt - data_set[index - 1])
    prev_delta_buffer.append(prev_buffer)
    prev_delta_buffer.append(delta_buffer)
  #print len(prev_delta_buffer)
  return prev_delta_buffer

def print_data(inf_data, prev_delta, save_file):
  print prev_delta
  file_handler = open(save_file, 'w')
  iter = 1
  while iter < len(inf_data[0]):
    loop_iter = 0
    while loop_iter < len(inf_data):
      file_handler.write(str(loop_iter + 1) + ":" + str(inf_data[loop_iter][iter]) + " ")
      loop_iter += 1
    loop_iter = 0
    while loop_iter < len(prev_delta):
      file_handler.write(str(loop_iter + 7) + ":" + str(prev_delta[loop_iter][iter]) + " ")
      loop_iter += 1
    file_handler.write("\n")
    iter += 1

if __name__ == "__main__":
  lines = read_data()
  inf_data = fix_weekends(lines)
  prev_data = gen_prev_delta(inf_data)
  print_data(inf_data, prev_data, "data.svm")
