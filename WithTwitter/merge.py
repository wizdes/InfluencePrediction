import sys

def read_data(filename):
  read_lines_array = []
  file_handler = open(filename, 'r')
  for read_buffer in file_handler:
    read_lines_array.append(read_buffer)
  #print read_lines_array
  return read_lines_array

if __name__ == "__main__":
  volume_lines = []
  train_lines = read_data("data.svm")
  volume_lines = read_data("volume_data.csv")
  volume_ind = []
  iter = len(volume_lines) - 2
  while iter >= 0:
    ind_buffer = float(volume_lines[iter]) - float(volume_lines[iter + 1])
    if ind_buffer > 0 : volume_ind.append("1")
    else : volume_ind.append("-1")
    iter -= 1
  file_write = open("svm_final", 'w')
  for index, elt in enumerate(volume_ind):
    print index
    file_write.write(str(elt) + " " + train_lines[index]) 
