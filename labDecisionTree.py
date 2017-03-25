import fileinput
import math
import copy

attributesValues = {}
attributes = [] 
answer = {}
readData = False
data = []
totalValues = {}
numberData = 0
gainInformation = {}

'''
  /**********************************************
	Get the subset of training data
	@param List Data
  **********************************************/
'''
def getTotalValues(data):
	values = {}
	for dat in data:
		if dat[-1] in values:
			values[dat[-1]] = values[dat[-1]] + 1
		else:
			values[dat[-1]] = 1
	return values

def isPure(result):
	for val in result:
		if result[0][-1] != val[-1]: 
			return False
	return True


'''
  /**********************************************
	Get entropy
	@param Dictionary Susbet of training examples
	@param Number Total amount of data
  **********************************************/
'''
def getEntropy(dictionary, total):
	sumEntropy = 0.0
	for val in dictionary.values():
		sumEntropy += (float(val) / float(total)) * math.log((float(val) / float(total)), 2)
	return (-sumEntropy)

def id3(childrens, parent, attributesCopy, dataFilter, depth):
	pure = -1
	for child in childrens:
		print "%s%s: %s" % (" " * depth * 2, parent, child)
		result = filter(lambda x: x[attributes.index(parent)] == child, dataFilter)
		pure = isPure(result)
		if pure or len(result) == 1:
			if any(result):
				print "%sANSWER: %s" % (" " * ((depth + 1) * 2), result[0][-1])
			else:
				print "%sANSWER:" % (" " * ((depth + 1) * 2))
		else:
			copy_list = copy.deepcopy(attributesCopy)
			copy_list.remove(parent)
			nextNode = getInformationGain(getEntropy(getTotalValues(result), len(result)), result, copy_list)
			id3(attributesValues[nextNode], nextNode, copy_list, result, depth + 1)

'''
  /**********************************************
	Get Information Gain 
	@param Number Parent's entropy value 
	@param List Susbet of training examples
	@param List Name of the variables that have not been used
  **********************************************/
'''

def getInformationGain(parentEntropy, dataFiltered, attributesFiltered):
	gainValue = []
	keyValue = []
	for val in attributesFiltered:
		index = attributes.index(val)
		gain = {}
		for value in range(len(dataFiltered)):
			if dataFiltered[value][index] in gain:
				if dataFiltered[value][-1] in gain[dataFiltered[value][index]]:
					(gain[dataFiltered[value][index]])[dataFiltered[value][-1]] = (gain[dataFiltered[value][index]])[dataFiltered[value][-1]] + 1
				else:
					(gain[dataFiltered[value][index]])[dataFiltered[value][-1]] = 1
			else:
				gain[dataFiltered[value][index]] = {dataFiltered[value][-1]: 1}
		sumGain = 0.0
		for x in gain.values():
			total = sum(x.values())
			sumGain += (getEntropy(x, total) * total / len(dataFiltered))
		keyValue.append(val)
		gainValue.append(parentEntropy - sumGain)
	if gainValue.count(gainValue[0]) == len(gainValue): 
		return keyValue[0]
	else:
		join = (zip(gainValue, keyValue))
		join.sort(reverse=True)
		return join[0][1]
 
#Parser
for line in fileinput.input():
	#Ignore comments
	if '%' not in line:
		#Get attributes
		if '@attribute' in line:
			line = line.split("@attribute",1)[1]
			line = line.rstrip('\n').rstrip('\r')
			key = line[0:line.find('{')].strip()
			keyValues = (line[line.find('{')+ 1:-1]).replace(',', '').split()
			attributes.append(key)
			if any(answer):
				attributesValues[answer.keys()[0]] = answer.values()[0]
			answer.clear()
			answer[key] = keyValues
		if readData and line != '' and line != '\n' :
			line = ((line.rstrip('\n').rstrip('\r')).replace(' ', '')).split(',')
			if line[-1] in totalValues:
				totalValues[line[-1]] = totalValues[line[-1]] + 1
			else:
				totalValues[line[-1]] = 1
			data.append(line)
		if '@data' in line:
			#Start reading the data
			readData = True

trya = getInformationGain(getEntropy(getTotalValues(data), len(data)), data, attributes[:-1])
id3(attributesValues[trya], trya, attributes[:-1], data, 0)

