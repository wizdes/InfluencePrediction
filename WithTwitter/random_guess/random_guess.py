import sys
import random

filename = "svm_final"
num_iter = 1000000

def load_results():
	predictions = []
	fp = open(filename)
	for line in fp:
		if len(line) > 0: predictions.append(line.split()[0])
	return predictions

def one_round_guessing(correct_results):
	num_correct = 0
	num_total = len(correct_results)
	for elt in correct_results:
		random_number = random.random()
		random_guess = "1"
		if random_number < 0.5: random_guess = "-1"
		if elt == random_guess: num_correct += 1
	return num_correct * 1.0 / num_total


def start_guessing(correct_results, num_iter):
	accuracy = 0
	iter = num_iter
	while(iter >= 0):
		accuracy += one_round_guessing(correct_results)
		iter -= 1
	return accuracy * 1.0/num_iter

if __name__ == "__main__":
	values = load_results()
	print "Accuracy is: " + str(start_guessing(values, num_iter))
