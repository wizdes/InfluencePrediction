import sys
import math

def loadTrainingData(filename):
	fileP = open(filename)
	lines = fileP.readlines()
	return lines
	trainingData = []
	for line in lines:
		element = {}
		parsed = line.split()
		for elt in parsed:
			datum = elt.split(":")
			if len(datum) == 1:
				element[0] = datum[0]
			else:
				element[datum[0]] = datum[1]
		trainingData.append(element)
	return trainingData

def loadTestingData(filename):
	fileP = open(filename)
	lines = fileP.readlines()
	return lines
	trainingData = []
	for line in lines:
		element = {}
		parsed = line.split()
		for elt in parsed:
			datum = elt.split(":")
			if len(datum) == 1:
				element[0] = datum[0]
			else:
				element[datum[0]] = datum[1]
		trainingData.append(element)
	return trainingData

def getDistance(trainElement, testElement):
	weightone = -0.2
	weighttwo = 2.5
	weightthree = 1
	trainEltArray = trainElement.split()
	for index, elt in enumerate(trainEltArray):
		if index == 0: continue
		#print index 
		#print elt
		trainEltArray[index] = elt.split(":")[1]
	testEltArray = testElement.split()
	for index, elt in enumerate(testEltArray):
		if index == 0: continue
		testEltArray[index] = elt.split(":")[1]
	distance = 0
	for index, elt in enumerate(trainEltArray):
		#if index != 0: distance += math.fabs(float(testEltArray[index]) - float(trainEltArray[index]))
		if index == 0: continue
		if index == 1 or index == 4: distance += math.fabs(float(testEltArray[index]) - float(trainEltArray[index])) * weightone
		if index == 2 or index == 5: distance += math.fabs(float(testEltArray[index]) - float(trainEltArray[index])) * weighttwo
		if index == 3 or index == 6: distance += math.fabs(float(testEltArray[index]) - float(trainEltArray[index]))* weightthree
	#print distance
	return distance

def singlePredict(testElement, trainingData):
	numExamples = 20
	distances = [-1]*numExamples
	predict = [0]*numExamples
	for element in trainingData:
		iter = 0 
		distance = getDistance(element, testElement)
		for index, var in enumerate(distances):
			if var == -1 or distance < distances[index]:
				distances[index] = distance
				predict[index] = float(element.split()[0])
				iter += 1
				break;
	#print predict
	sum = 0
	for index, element in enumerate(predict): 
		sum += (numExamples - index) * 1.0 * element
	return sum * 1.0 / ((numExamples * (numExamples + 1))/2.0)
	#for index, element in enumerate(predict): 
	#	sum += element
	#return sum * 1.0 / numExamples

def predict(trainingData, testingData):
	within = 0
	total = 0
	good = 0
	for testElement in testingData:
		predictedResult = singlePredict(testElement, trainingData)
		validResult = float(testElement.split()[0])
		#print "Comparing: " + str(predictedResult) + " " + str(validResult)
		diff = (predictedResult - validResult) * 1.0/predictedResult
		print diff
		if diff > -0.22 and diff < 0.22 : good += 1
		if diff < 0: diff = diff * -1
		within += diff
		total += 1
	print "good is: " + str(good) + " out of: " + str(total)
	print within * 1.0/total


if __name__ == "__main__":
	train = loadTrainingData(sys.argv[1])
	test = loadTestingData(sys.argv[2])
	predict(train, test)
