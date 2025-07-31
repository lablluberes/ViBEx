"""REVEAL.py: Description of what foobar does."""
__author__      = "Natalie Berestovsky, Rice University"

from bitarray import bitarray
import itertools, random
from math import log
from inference_methods.bestfit.utilsS2B import KarnaughMaps


debug = False    

def getAllCombinations(keys, maxLevel):   
	# create combinations for the list of entropies 
	allCombinations = {}  
	ps = {}
	for i in range(0, maxLevel+1):           
		a = itertools.combinations(keys, i)    
		allCombinations[i] = list(a)   
		b = itertools.product("01", repeat=i)   
		ps[i] = list(b) 

	return allCombinations, ps  
	
def intpuEntropiesDeterministic(keys, tt, maxLevel, allCombinations, ps):

	allE = {}   
	# for each combination find entropy
	for length, combinations in allCombinations.items():  
		#print(length) 
		#print(combinations)
		for c in combinations:   
			#print(c) 
			#p = itertools.product("01", repeat=length) 
			p = ps[length]    
			totals = []
			for p1 in p:    
				finalOuts = list(tt.keys())
				'''# ---- THIS INCLUDES Inputs with multiple Outputs, len(outputs) times----
				for kkk,l in tt.items():
					if len(l) > 1:
						for ll in range(len(l)-1):
							finalOuts.append(kkk)
				'''

				for k in tt.keys():
					# that is done by matching the idx
					for idx in range(length):
						character = c[idx]
						value = p1[idx] 
						position = keys.index(character)
						if int(k[position]) != int(value):
							'''# ---- This removes multiple outputs if needed (all of them) - needed if adding things arount the line 115
							zz = finalOuts.count(k)
							#for zzz in range(zz):'''
							finalOuts.remove(k)
							break
				#print len(consideredOuts), len(finalOuts)
				totals.append(len(finalOuts))
			if debug:
				print(totals)
			s = float(sum(totals))
			#counted all permutations, now calc entropy
			entr = 0 
			for t in totals:   
				if t != 0: 
					entr -= t/s * log(t/s,2)
			allE[c] = entr  
		
	return allE     


def outputEntropy(item, keys, tt, inputE, allE, level, allCombinations, ps):
	# calculate single output entropies H(A')
	# items position in the key
	iidx = keys.index(item)
	#combinations = itertools.combinations(keys, level) 
	combinations = allCombinations[level]  
	for c in combinations:  
		totals = []
		for bin in range(2):
			# since item is output, we are seeing if it has the right value in the OUTPUTS, not keys
			consideredIns = []
			for k in tt.keys():
				for kk in tt[k]:
					if int(kk[iidx]) == bin:
						consideredIns.append(k)
			#print item,c,bin
			#p = itertools.product("01", repeat=level)
			p = ps[level]   
			for p1 in p:
				finalList = list(consideredIns)
				#print p1, finalOuts
				
				for k in consideredIns:
					# that is done by matching the idx
					for idx in range(len(c)):
						character = c[idx]
						value = p1[idx]
						position = keys.index(character)
						#print character, value, position, int(k[position]), k
						if int(k[position]) != int(value):
							finalList.remove(k)
							break
				#print len(consideredOuts), len(finalOuts)
				totals.append(len(finalList))
		if debug:
			print(totals)		
		s = float(sum(totals))
		#counted all permutations, now calc entropy
		entr = 0
		for t in totals:
			if t != 0:
				entr -= t/s * log(t/s,2)
		allE[(item, c)] = entr 
		#print(allE)  
	return allE 

def calculateM(item, keys, inputE, allE, level, allCombinations):
	if (level == 0):  
		return 
	allMs = {} 
	iidx = keys.index(item)
	#combinations = itertools.combinations(keys, level)
	combinations = allCombinations[level]    
	for c in combinations:
		entr1 = allE[(item,())] 
		entr2 = inputE[c]
		
		entrBoth = allE[(item,c)]        
		#print item, c, item, entr1, comb, entr2, entrBoth
		m = entr1 + entr2 - entrBoth
		if entr1 == 0:
			m = 0
		else:
			m /= entr1 
		allMs[(item,c)] = m    

	return allMs

'''
data: key is the name of interactions, item is the function dictionary
used to extract a complete rule table for individual species
'''
def getText(data, ps):  
	toInterprete = {} 
	texts2return = []  
	
	for name in data.keys():  
		func = data[name]       
		
		o = name[0] 
		i = name[1] 
		#o,i = name.split("\'")
		if len(i) > 3:		# only interpprete function with 3 or less inputs
			print(str(name)+": Input is too large " )
			continue     

		# check completeness and get the final list of what to interprete
		#p = itertools.product("01", repeat=len(i)) 
		p = ps[len(i)]  
		good = True	#assume it's a good table
		for p1 in p:
			valp1 = "".join(p1)
			zeroOut = func[0]
			oneOut = func[1]
			if valp1 not in zeroOut and valp1 not in oneOut:
				print("Incomplete transition "+str(name)+" "+str(func)) 
				good = False  
				break
		if good:
			toInterprete[name] = func

	km = KarnaughMaps()
	allTexts = {}
	for name, func in toInterprete.items():
		#print name, func
		o = name[0]
		i = name[1]
		#o,i = name.split("\'") 

		if len(i) == 1:
			f = km.getFunction1(o, i, func)       
		elif len(i) == 2:
			f = km.getFunction2(o, i, func) 
		elif len(i) == 3:
			f = km.getFunction3(o, i, func)  
		
		if o in allTexts:
			allTexts[o].append(f)
		else:
			allTexts[o] = [f]
			
	#for zz in range(100): 
	text = ''
	for k in allTexts.keys():
		rText = ''
		while rText == '':
			rText = random.choice(allTexts[k])
			if rText != '':
				text += rText +'\n' 
	if text not in texts2return and text != '':
		texts2return.append(text)  
		
	return texts2return 