import numpy as np
import pandas as pd
from itertools import product

BITS_PER_BLOCK_32 = 32


def GET_BIT(x, i):
  return (((x) & (1 << (i))) != 0)


def getDNF(truthTable, genes):
     
  if (truthTable == np.zeros(len(truthTable))).all():
    return "False"
  else:
    if (truthTable == np.ones(len(truthTable))).all():
      return "True"

  entries = np.array(list(product([0,1], repeat=len(genes))))

  #print("entries:")
  #print(entries)

  queryEntry = entries[truthTable==1].T
  
    #print(genes, queryEntry)
  conjunctions = []

  for i in range(len(queryEntry[0])):
      conjunctions.append(dict(zip(genes, queryEntry[:,i])))

    #print(conj)

  exprs = [] 

  for conj in conjunctions:
      currExpr = []
      for k in conj.keys():
        if conj[k] == 1:
          currExpr.append(k)
        else:
          currExpr.append("not " + k)
      exprs.append("(" + " and ".join(currExpr) + ")")
  
  exprs1 = [e for e in exprs if e != ""]
  string_expr = " or ".join(exprs1)
  return string_expr



def get_rules(res, genes):

  rules = {}
  exprs = []
  for i in range(len(res)):
    #print(f"Gene {i}:")
    for l in range(1): #range(len(res[i])):
     
      gene_in_rule = [genes[i] for i in res[i][l]['input_genes']]
      transition_function = res[i][l]['transition_function']

      curr_rule = getDNF(np.array(transition_function), sorted(gene_in_rule))

      rules[genes[i]] = curr_rule
      exprs.append(curr_rule)

  return rules, exprs


def run_bestfit(measurements, maxK=5):

    numGenes = len(measurements)

    if numGenes < maxK:
            maxK = numGenes

    genenames = list(measurements.index)

    inputStates = []
    outputStates = []

    array_binary = np.matrix(measurements).flatten(order='F').tolist()[0]

    inputStates = array_binary[:-numGenes]
    outputStates = array_binary[numGenes:]

    numStates = len(inputStates) // numGenes

    #print(inputStates)
    #print(outputStates)

    if (numGenes % BITS_PER_BLOCK_32 == 0):
        numElts = numGenes // BITS_PER_BLOCK_32
    else:
        numElts = numGenes // BITS_PER_BLOCK_32 + 1

    #print(numElts, numStates)

    encodedInputStates = [0] * (numElts * numStates)
    encodedOutputStates = [0] * (numElts * numStates)

    for state in range(numStates):

        for gene in range(numGenes):
            encodedInputStates[(numElts * state) + gene // BITS_PER_BLOCK_32] |= (inputStates[state*numGenes + gene] << (gene % BITS_PER_BLOCK_32))
            encodedOutputStates[(numElts * state) + gene // BITS_PER_BLOCK_32] |= (outputStates[state*numGenes + gene] << (gene % BITS_PER_BLOCK_32))
            

    #print("encoded input: ")
    #print(encodedInputStates)

    #print("encoded output: ")

    #print(encodedOutputStates)

    #print("number states: ", numStates)
    #print("maxK: ", maxK)
    #print("number genes: ", numGenes)

    res = [[] for i in range(numGenes)]
    errors = [0] * numGenes


    res = bestFitExtension(encodedInputStates,encodedOutputStates,
                            numStates,numGenes,maxK,res,errors)
    
    #print(res)

    rules = get_rules(res, genenames)

    return rules




def addFunctionListElement(root, k, transitionFunctionSize, inputGenes, transitionFunction):

  if not isinstance(inputGenes, list):
    inputGenes = [inputGenes]

  if not isinstance(transitionFunction, list):
    transitionFunction = [transitionFunction]

  #print(inputGenes)
  el = {'k':k, 'input_genes':inputGenes, 'transition_function':transitionFunction}

  #print("before adding: ", root)

  root.insert(0, el)

  #print("after adding:", root)

  return root

class InputCombination:
  def __init__(self, pos, numFixed, numAvailable, k, n, indexMapping, comb, intComb):
    self.pos = pos
    self.numFixed = numFixed
    self.numAvailable = numAvailable
    self.k = k
    self.n = n
    self.indexMapping = indexMapping
    self.comb = comb
    self.intComb = intComb

def initCombination(k, n):
  res = InputCombination(0, 0, 0, k, n, [0]*n, [0]*k, 0)

  for j in range(n):
        res.indexMapping[res.numAvailable] = j
        res.numAvailable += 1

  res.intComb = [0] * res.numAvailable

  for j in range(res.k - res.numFixed):
    res.intComb[j] = k - res.numFixed - j - 1
    res.comb[res.numFixed+j] = res.indexMapping[res.intComb[j]]

  ##print(f" initialize comb = res.k: {res.k}, res.n: {res.n}, res.numFixed: {res.numFixed}, res.numAvailable: {res.numAvailable} comb: {res.comb} indexMapping: {res.indexMapping} intComb: {res.intComb}")

  return res

def nextCombination(comb):
  posChanged = False

  while comb.pos < comb.k - comb.numFixed and comb.intComb[comb.pos] == comb.numAvailable - comb.pos - 1:
    comb.pos += 1
    posChanged = True

  if comb.pos == comb.k - comb.numFixed:
    return False, None

  if posChanged:
    comb.intComb[comb.pos] += 1
    for i in range(comb.pos, 0, -1):
      comb.intComb[i-1] = comb.intComb[i] + 1
    comb.pos = 0

  else:

    comb.intComb[comb.pos] += 1

  for j in range(0, comb.k - comb.numFixed):
    comb.comb[comb.numFixed+j] = comb.indexMapping[comb.intComb[j]]

  ##print(f" do nextCombination = comb: {comb.comb}")

  return True, comb

def bestFitExtension(inputStates, outputStates, numStates, numGenes, maxK, result, errors):

  if (numGenes % BITS_PER_BLOCK_32 == 0):
    numElts = numGenes // BITS_PER_BLOCK_32
  else:
    numElts = numGenes // BITS_PER_BLOCK_32 + 1

  bestLength = [255] * numGenes

  for i in range(numGenes):
    #print(f"\nGene {i}:")
    currentMaxK = maxK
    minK = 0
    excludedCount = 0

    if (currentMaxK < minK):
      currentMaxK = minK

    if (currentMaxK > numGenes - excludedCount):
      currentMaxK =  numGenes - excludedCount

    errors[i] = ~0

    if (minK == 0):

      geneVal = GET_BIT(outputStates[i//BITS_PER_BLOCK_32],i % BITS_PER_BLOCK_32)
      isConst = True

      const0Err = (geneVal > 0)
      const1Err = (geneVal == 0)

      for s in range(1, numStates):

        nextBit = GET_BIT(outputStates[s*numElts + i//BITS_PER_BLOCK_32],i % BITS_PER_BLOCK_32);
        if(nextBit	!= geneVal):
          isConst = False

        if(nextBit):
          const0Err += 1
        else:
          const1Err += 1

      if (isConst):
        inputGenes = -1
        result[i] = addFunctionListElement(result[i],1,1,inputGenes,geneVal)
        errors[i] = 0
        bestLength[i] = 0
        #print("aqui")

      else:
        if (const0Err <= const1Err):
          inputGenes = -1
          val = 0
          result[i] = addFunctionListElement(result[i],1,1,inputGenes,val)
          errors[i] = const0Err
          bestLength[i] = 0
          #print("aqui")

        if (const1Err <= const0Err):
          #print("aqui")
          inputGenes = -1
          val = 1
          result[i] = addFunctionListElement(result[i],1,1,inputGenes,val)
          errors[i] = const1Err
          bestLength[i] = 0
          #print("aqui")

    #"Minor" if age < 18 else "Adult"
    for k in range(minK if minK > 1 else 1, currentMaxK+1):
      if (errors[i] == 0):
        break

      comb = initCombination(k, numGenes)

      array_sz = 1 << k

      if array_sz % BITS_PER_BLOCK_32 == 0:
        numEltsFunc = array_sz // BITS_PER_BLOCK_32
      else:
        numEltsFunc = array_sz // BITS_PER_BLOCK_32 + 1

      next_comb = True

      while(next_comb):
        
        #print("\nwhile\n")

        c_0 = [0] * array_sz
        c_1 = [0] * array_sz

        for s in range(numStates):

          input = 0

          for bit in range(k):
            input |= (GET_BIT(inputStates[s*numElts + comb.comb[bit]//BITS_PER_BLOCK_32],comb.comb[bit] % BITS_PER_BLOCK_32) << bit)

          response = GET_BIT(outputStates[s*numElts + i//BITS_PER_BLOCK_32],i % BITS_PER_BLOCK_32)

          if response == 0:
            c_1[input] += 1
          else:
            c_0[input] += 1

        f = [0] * numEltsFunc
        error = 0

        for c in range(array_sz):
          if c_0[c] > c_1[c]:
            error += c_1[c]
          else:
            error += c_0[c]

        if error < errors[i]:
          errors[i] = error
          bestLength[i] = k
          #freeFunctionList(result[i])
          #print("elimine la lista\n")
          result[i] = []

        #print("aqui3")
        ##print(f"\n error: {error}, errors: {errors[i]}, bestlength: {bestLength[i]}, k: {k}, allSolutions: {allSolutions}\n")
        if (error <= errors[i]) and (bestLength[i] >= k):
          #print("aqui4")
            ##print("\n PBN is false \n")
            f = [0] * array_sz
            for l in range(array_sz):
              if c_1[l] < c_0[l]:
                f[l] = 1
              elif c_1[l] > c_0[l]:
                f[l] = 0
              else:
                f[l] = -1
            ##print(" add inside PBN is false\n")
            #print(f"voy a añadir input_genes: {comb.comb}")
            result[i] = addFunctionListElement(result[i], k, array_sz, comb.comb.copy(), f)
            #print(f"{result[i][0]['input_genes']}")
          
        next_comb, comb = nextCombination(comb)
        #print(result[i])
    #printObject(result)
    #break
  #print(f"{result[0][2].input_genes}")
  #print(errors)
  return result


"""
if __name__ == "__main__":
  data = {
    'Fkh2': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'Swi5': [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    'Sic1': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    'Clb1': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  }
  
  data = {
    'Gene1': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    'Gene2': [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    'Gene3': [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    'Gene4': [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    'Gene5': [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
}


  df = pd.DataFrame(data).T
  
  res, expr = run_bestfit(df, maxK=4)
  
  print(res)
  
  ru = pd.DataFrame()
  
  ru['Gene'] = list(df.index)
  ru['Rule'] = expr
  
  print(ru)
  
  dd = "{'Gene1': '(not Gene3 and not Gene4 and not Gene5) or (Gene3 and not Gene4 and Gene5)', 'Gene2': '(not Gene1 and Gene3)', 'Gene3': '(not Gene3 and not Gene4 and Gene5) or (not Gene3 and Gene4 and not Gene5) or (Gene3 and not Gene4 and not Gene5) or (Gene3 and not Gene4 and Gene5)', 'Gene4': '(not Gene4 and not Gene5) or (Gene4 and Gene5)', 'Gene5': '(not Gene2 and not Gene4 and not Gene5) or (Gene2 and Gene4 and not Gene5)'}"
  
  aa = "{'Gene1': '(not Gene3 and not Gene4 and not Gene5) or (Gene3 and not Gene4 and Gene5)', 'Gene2': '(not Gene1 and Gene3)', 'Gene3': '(not Gene3 and not Gene4 and Gene5) or (not Gene3 and Gene4 and not Gene5) or (Gene3 and not Gene4 and not Gene5) or (Gene3 and not Gene4 and Gene5)', 'Gene4': '(not Gene4 and not Gene5) or (Gene4 and Gene5)', 'Gene5': '(not Gene2 and not Gene4 and not Gene5) or (Gene2 and Gene4 and not Gene5)'}"
  
  print(dd == aa)

  #res = [[] for i in range(4)]"""
