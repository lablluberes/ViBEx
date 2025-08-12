#!/usr/bin/env python
"""
BinInfer.py: An example of how to interact with the plotting canvas by connecting
to move and click events
"""
__author__      = "Natalie Berestovsky, Rice University"

import sys, os, itertools, random, math, numpy, pickle
from io import StringIO
from operator import itemgetter, attrgetter
from bitarray import bitarray
from inference_methods.BooleanModeling2post.utilsS2B import Binarization, KarnaughMaps, BestFit
import inference_methods.BooleanModeling2post.REVEAL
from inference_methods.BooleanModeling2post.boolean2 import Model, util
from subprocess import Popen, PIPE, STDOUT
from time import time

originalSeries = {}	# original series stored here as a list  
binarySeries = {}	# structure same as the original but with binary series
inputoutput = {}	# keys are combinations, with a list of compbinations that are outputs of it
debug = True 
binz = Binarization()



argumentsValues = {'input':'','iterations':5000, 'maxscore':0,'solutions':1,'output':['score','text'],'verbose':1, 'learn-method':'REVEAL',  'bin-method':0, 'reduction':0, 'outputFile':None} 

def main(argv=sys.argv):  
	
	global argumentValues 
	bestBinarySeries = None  
	bestScore = None 
	bestSums = None 
	bestText = None 
	bestCompleteSTT = None 
	allScores = None
	
	output = {'binSer':bestBinarySeries,'score':bestScore,'sums':bestSums,'text':bestText,"stt":bestCompleteSTT,'allScores':allScores}
	
	dirArg = []
	for arg in sys.argv:
		if ".py" not in arg and "=" not in arg:
			raise TypeError("incorrect argument "+arg)
			break
		if ".py" not in arg:
			name,val = arg.split("=")
			if name == 'input' or name == 'learn-method' or name == 'outputFile':   
				argumentsValues[name] = val 
			elif name == 'iterations' or name == 'solutions' or name == 'verbose' or name == 'reduction':
				argumentsValues[name] = int(val) 
			elif name == 'bin-method':
				if val.isdigit():
					argumentsValues[name] = int(val)
				elif val == 'A':
					argumentsValues[name] = 0
				else:
					argumentsValues[name] = 3 # k-means with 3 levels
			elif name == 'maxscore':
				argumentsValues[name] = float(val)
			elif name == 'output':
				# configure output
				argumentsValues[name] = val.split(',')
				
				
	if argumentsValues['input'].endswith("pkl"):
		s = pickle.load(open(argumentsValues['input'], "rb"))
		for k,j in s.items():
			originalSeries[k] = j
		order = originalSeries.keys()
	else:
		if(os.path.exists(argumentsValues['input'])):
			f = open(argumentsValues['input'], 'r')
		else:
			f = StringIO.StringIO(argumentsValues['input']) #create text stream if string is provided instead of file   
			
		topLine = f.readline().split()
		order = []
		for t in topLine:
			g = "Gene" + str(int(t)+1)               
			originalSeries[g] = []
			order.append(g)  
		
		for line in f:
			if line.startswith("#"):
				continue 
			words = line.split() 
			for i in range(len(words)):   
				originalSeries[order[i]].append(float(words[i])) 
				
		
	#print argumentsValues
	allConvergence = [] 
	allTimes = []
	bMethod = argumentsValues['bin-method']
	bSer = None  

	if(bMethod==None):   			
		bSer = originalSeries  #data is already binarized  

	if bMethod == 0:
		bSer = {'A': bitarray('010000'), 'C': bitarray('010000'), 'B': bitarray('011000'), 'E': bitarray('000011'), 'D': bitarray('000011')}#{'Gene2': bitarray('010000'), 'Gene3': bitarray('011000'), 'Gene4': bitarray('010000'), 'Gene5': bitarray('000011'), 'Gene6': bitarray('000011')}#binz.BASC_A_binarization(dict(originalSeries), argumentsValues['reduction'])	
	elif bMethod == -1:
		bSer = binz.BASC_B_binarization(dict(originalSeries), argumentsValues['reduction'])
		
		
	textSolutions = []
	
	for i in range(argumentsValues['solutions']):
		print('Cycle ', i)
		
		if argumentsValues['learn-method'] == 'REVEAL':
			conv = findOne_REVEALSolution(argumentsValues['iterations'],argumentsValues['maxscore'],output,binarySeries=bSer)
		else:
			conv = findOne_BESTFULLFITSolution(argumentsValues['iterations'],argumentsValues['maxscore'],output,binarySeries=bSer,lMethod=argumentsValues['learn-method'])

		
		# record individual solution
		allConvergence.append(conv)
		output['allScores'] = conv 
		#findKMeansSolution(output) 
		print("\nSolution found:")
		toPrint = argumentsValues['output']
		for tp in toPrint: 
			if tp in output:
				print(output[tp])
		textSolutions.append(output["text"])			
		# reset solution
		output['score'] = None
		output['sums'] = None
		output['text'] = None
		output['binSer'] = None
		output['stt'] = None
		output['allScores'] = None    		  
	#print allConvergence
	#idxOfDot = argumentsValues['input'].index('.')
	# can be used to dump convergence data
	#output = open(argumentsValues['input'][0:idxOfDot]+"_"+argumentsValues['learn-method']+str(argumentsValues['bin-method'])+'_data1000.pkl', 'wb')
	#pickle.dump(allConvergence, output)
	#output.close()	
	'''
	else:
		if bMethod == 0:
			print 'BASC A'
			if argumentsValues['learn-method'] == 'BESTFIT':
				solutions = findAllBASCA_BESTFITSolutions()
			elif argumentsValues['learn-method'] == 'ENUM':
				print "soon"
			else:
				solutions = findAllBASCA_REVEALSolutions()
			
			# print all the soltuons
			for sol in solutions:
				text,score = sol
				print score
				print text
			
		elif bMethod == 1:
			print 'BASC B'
		else:
			print 'Unidentified binariztion method. See README.'
	'''
	
			
def findOne_REVEALSolution(maxIters, goodScore, output,binarySeries=None):  
	maxLevel = 3      

	convergence = [] 
	#for xyz in range(maxIters):
	xyz = 0
	bMethod = argumentsValues['bin-method']
	
	if bMethod > 0: 
		clusters = int(math.pow(2,bMethod))
	
	#convert binary series to bit arrays  
	keys = sorted(binarySeries.keys()) 
	if	not isinstance(binarySeries[keys[0]], bitarray): 
		for key in keys:
			binarySeries[key] = bitarray(map(int, binarySeries[key]))      
	
	while (output['score'] > goodScore or output['score'] == None):
		if xyz >= maxIters:
			break
		xyz +=1
		if output['score'] != None and output['score'] <= goodScore:
			if argumentsValues['verbose'] >= 1:
				print("STOP since reached score of "+str(goodScore)+" in "+str(xyz) + " iterations")
			break
		if argumentsValues['verbose'] >= 1 and xyz % 100 == 0: 
			print("ITERATIONS "+str(xyz))
		# only if we are doing k-means, we have re-binarize every time
		if bMethod > 0:
			binarySeries = binz.decrementalKMeanBinarization(dict(originalSeries), clusters, argumentsValues['reduction'])	
		
		# otherwise, just battle non-determanism
		#print(binarySeries)
		print("here i am ooo")  
		
		allKeys, allFreq, transitionsList = binz.stateTTMostFreq([binarySeries])
		allCombinations, ps = REVEAL.getAllCombinations(keys, maxLevel)       
		
		print("here i am") 
		
		transitions = transitionsList[0]
		'''get the initial state for this division'''
		initialState = {}
		for k in allKeys:
			initialState[k] = bool(binarySeries[k][0])
		'''execute binary using the transition table'''
				
		entropy = REVEAL.intpuEntropiesDeterministic(allKeys, transitions, maxLevel, allCombinations, ps)   
		
		print("here i am 2")
		
		resovled = {}
		unresolved = binarySeries.keys()
		allEntropy = {}
	
		myIteration = {}
		#limit search to 3 inputs max
		for i in range(0,maxLevel + 1):       
			newUnresolved = list(unresolved)
			k = 0
			for un in newUnresolved:
				k = k + 1 
				print(len(newUnresolved)-k)   
				if debug:
					print("Resolving "+un+" at level "+str(i))
				allEntropy = REVEAL.outputEntropy(un, allKeys, transitions, entropy, allEntropy, i, allCombinations, ps)    
				m = REVEAL.calculateM(un, allKeys, entropy, allEntropy, i, allCombinations)    
				if m != None:
					for a,b in m.items():
						if debug:
							print("..."+str(a)+": "+str(b))		
						if abs(b-1) < 0.000000001:
							if un in unresolved:
								unresolved.remove(un)
								
							x = a[0]  
							y = a[1]  
							myT = binz.getTTFunction(y,x,transitions, allKeys)
							if debug:
								print(myT)
							myIteration[a] = myT
		header = ''
		for i in allKeys:
			header += i + " = " + str(initialState[i]) + "\n"
		allTexts = REVEAL.getText(myIteration, ps)  
		length = len(binarySeries[allKeys[0]])
		bestText = ''
		bestScore = 10000
		
		for onlytext in allTexts:
			text = header + onlytext
			model = Model( mode='sync', text=text )
			model.initialize()
			model.iterate( steps=length-1 )
			count = 0
			sums = {}
	
			#compare the binary series
			for k in allKeys:
				sums[k] = 0
			for d in model.states:
				for k in d.keys():
					sums[k] += abs(binarySeries[k][count] - int(d[k]))
		
				count += 1
	
			score = 0
			for s,v in sums.items():
				score += v
			score /= (float(len(binarySeries[binarySeries.keys()[0]])) * float(len(sums)))
			if score < bestScore:
				bestScore = score
				bestText = onlytext  
	
		convergence.append(bestScore)			
		
		if output['score'] is None or bestScore < output['score']:
			output['score'] = bestScore
			#output['sums'] = sums
			output['text'] = bestText
			output['binSer'] = binarySeries 
			#output['stt'] = binz.getResultCompleteTT(myIteration, allKeys)  
			if argumentsValues['verbose'] >= 2: 
				toPrintLev2 = argumentsValues['output']
				for tp in toPrintLev2:
					if tp in output:
						print(output[tp])
	print("Reached in ",xyz," iterations")			
	return convergence			


def get_states(textHeaderdict, textRules, length):
    
    states = []
    
    #print(textHeaderdict, textRules)
    
    #print(textHeaderdict)
    
    states.append(textHeaderdict)
    
    for i in range(length):
        
        prev_state = textHeaderdict
        
        #print(curr_state, textRules)
        
        for e in textRules:
            
            textHeaderdict[e] = eval(textRules[e], {}, prev_state)
            
        #print(textHeaderdict)
        
        states.append(textHeaderdict)
    
    #print("sali")
    return states


def findOne_BESTFULLFITSolution(maxIters, goodScore, output, binarySeries=None, lMethod='BESTFIT'):
	convergence = []
	#for xyz in range(maxIters):
	xyz = 0
	bMethod = argumentsValues['bin-method']
	if bMethod > 0:
		clusters = int(math.pow(2,bMethod))
	bf = BestFit()
	
	
	while (output['score'] == None or output['score'] > goodScore): 
		if xyz >= maxIters:
			break
		xyz +=1
		if output['score'] != None and output['score'] <= goodScore:
			if argumentsValues['verbose'] >= 1:
				print("STOP since reached score of "+str(goodScore)+" in "+str(xyz) + " iterations")
			break
		#if argumentsValues['verbose'] >= 1 and xyz % 100 == 0: 
			#print("ITERATIONS "+str(xyz))

		if bMethod > 0:
			binarySeries = binz.decrementalKMeanBinarization(dict(originalSeries), clusters, 0)	

		order = sorted(binarySeries.keys())  
		seriesLength = len(binarySeries[list(binarySeries.keys())[0]])
		
		
		k = 1
		p = itertools.combinations(order, 1)      	
		answers1, error1 = bf.getBestFitAndError(k, p, [binarySeries], order)


		k = 2
		p = itertools.combinations(order, 2)		
		answers2, error2 = bf.getBestFitAndError(k, p, [binarySeries], order)


		k = 3
		p = itertools.combinations(order, 3) 
		answers3, error3 = bf.getBestFitAndError(k, p, [binarySeries], order)    

		bestsFunc = {}
		bestsScore = {}
		for o in order:
			bestsFunc[o] = []
			bestsScore[o] = 10000

		if lMethod == 'BESTFIT':
			bestsFunc, bestsScore = bf.inferBestFunc(order,error1,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferBestFunc(order,error2,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferBestFunc(order,error3,bestsFunc,bestsScore)
		else:
			bestsFunc, bestsScore = bf.inferFullFunc(order,error1,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferFullFunc(order,error2,bestsFunc,bestsScore)
			bestsFunc, bestsScore = bf.inferFullFunc(order,error3,bestsFunc,bestsScore)
		

		# clean up those that are longer but have score as the shortest ones
		for k, item in bestsFunc.items():   
			if len(item) > 0:
				shortest = len(min(item, key=len))
				newList = []
				for i in item:
					if len(i) == shortest:
						newList.append(i)
				bestsFunc[k] = newList

		initialState = {}
		for k in order:
			initialState[k] = bool(binarySeries[k][0])
		textHeader = ""
		for i in order:
			textHeader += i + " = " + str(initialState[i]) + "\n"

		bestText = ''
		bestScore = 10000
		texts = bf.getText(bestsFunc, order, answers1, answers2, answers3, textHeader)
		length = len(binarySeries[order[0]])
		
		for textwh in texts:
      
			rules = textwh.split("\n")
			rules_dict = {}
			genes_dict = {}
			#print(rules)

			genes = textHeader.split("\n")
			
			for expression in genes:
				if expression:
					parts = expression.split(' = ')
					if len(parts) == 2:
						key = parts[0].replace('*', '').strip()
						value = parts[1].strip()
						genes_dict[key] = eval(value)
   
			for expression in rules:
				if expression:
					parts = expression.split(' = ')
					if len(parts) == 2:
						key = parts[0].replace('*', '').strip()
						value = parts[1].strip()
						rules_dict[key] = value
      
			text = textHeader + textwh
			#print(textHeader)

			states = get_states(genes_dict, rules_dict, length-1)
			
			#model = Model( mode='sync', text=text )
			#model.initialize()
			#model.iterate( steps=length-1 )
   
			count = 0
			sums = {}

			#compare the binary series
			for k in order:
				sums[k] = 0
			for d in states: #model.states:
				for k in d.keys():
					sums[k] += abs(binarySeries[k][count] - int(d[k]))

				count += 1

			score = 0
			for s,v in sums.items():
				score += v
			score /= (float(len(binarySeries[list(binarySeries.keys())[0]])) * float(len(sums)))

			if score < bestScore:
				bestScore = score
				bestText = textwh 

		convergence.append(bestScore)


		if output['score'] is None or bestScore < output['score']:
			#print score
			#print text 
			#print(bestScore, output['score'])
			output['score'] = bestScore
			output['text'] = bestText
			output['binSer'] = binarySeries
			#output['stt'] = binz.getResultCompleteTT(myIteration, order)
			if argumentsValues['verbose'] >= 2: 
				toPrintLev2 = argumentsValues['output']
				for tp in toPrintLev2:
					if tp in output:
						print(output[tp])
	#print("Reached in ",xyz," iterations")
	return convergence


def run(data, iterations, goodScore):
    
    bestBinarySeries = None
    bestScore = None
    bestSums = None
    bestText = None
    bestCompleteSTT = None
    allScores = None
    
    output = {'binSer':bestBinarySeries,'score':bestScore,'sums':bestSums,'text':bestText,"stt":bestCompleteSTT,'allScores':allScores}
    
    conv = findOne_BESTFULLFITSolution(iterations, goodScore, output, binarySeries=data, lMethod='BESTFIT')
    
    
    textSolutions = []
    textSolutions.append(output["text"])

	#print(textSolutions) 
 	
    lines = textSolutions[0].strip().split('\n')

	# Parse into a dictionary
	
    expr_dict = {}
    
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            expr_dict[key] = value
            
            
    rules_dict = {'Gene':[], 'Rule':[]}
    
    for k in data.keys():
        rules_dict['Gene'].append(k)
        
        if k not in expr_dict:
            rules_dict['Rule'].append('')
            
        else:
            rules_dict['Rule'].append(expr_dict[k])
        
    #print(rules_dict)
        
    output['score'] = None
    output['sums'] = None
    output['text'] = None
    output['binSer'] = None
    output['stt'] = None
    output['allScores'] = None
    
    return rules_dict

#if __name__ == "__main__":
    
#    res = run({'A': bitarray('010000'), 'B': bitarray('010000'), 'C': bitarray('011000'), 'D': bitarray('000011'), 'E': bitarray('000011')}, 5000, 10)
    
#    print(res)
    
    #main()