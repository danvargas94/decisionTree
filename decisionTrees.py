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

'''
  /**********************************************
	Get Information Gain 
	@param Number Parent's entropy value 
	@param List Susbet of training examples
	@param List Name of the variables that have not been used
  **********************************************/
'''

def getInformationGain(parentEntropy, dataFiltered, attributesFiltered):
	#print(len(dataFiltered))
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
	join = (zip(gainValue, keyValue))
	join.sort(reverse=True)
	#print(join)
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

'''#print("attributesValues")
#print(attributesValues)
#print("attributes")
#print(attributes)
#print("answer")
#print(answer)
#print("data")
#print(data)'''
entropy = getEntropy(getTotalValues(data), len(data))
#print(entropy)
trya = getInformationGain(getEntropy(getTotalValues(data), len(data)), data, attributes[:-1])

#Test
result = filter(lambda x: x[attributes.index(trya)] == "sunny", data)
#print(attributes[1:-1])
copy_list = copy.deepcopy(attributes)
copy_list.remove("outlook")
getInformationGain(getEntropy(getTotalValues(result), len(result)), result, copy_list[:-1])
