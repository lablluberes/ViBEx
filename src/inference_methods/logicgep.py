##########################################
#
# Code was taken from https://github.com/DZ-Z/LogicGep
# This is the code of the method created by Dezhen Zhang in following paper
#
# Zhang, D., Gao, S., Liu, Z. P., & Gao, R. (2024). LogicGep: Boolean networks inference using symbolic regression from time-series transcriptomic profiling data. Briefings in Bioinformatics, 25(4), bbae286.
#
# DOI: https://doi.org/10.1093/bib/bbae286
##########################################

import deap
import random
import pandas as pd

def _validate_basic_toolbox(tb):
	"""
	Validate the operators in the toolbox *tb* according to our conventions.
	"""
	assert hasattr(tb, 'select'), "The toolbox must have a 'select' operator."
	# whether the ops in .pbs are all registered
	for op in tb.pbs:
		assert op.startswith('mut') or op.startswith(
			'cx'), "Operators must start with 'mut' or 'cx' except selection."
		assert hasattr(tb, op), "Probability for a operator called '{}' is specified, but this operator is not " \
								"registered in the toolbox.".format(op)
	# whether all the mut_ and cx_ operators have their probabilities assigned in .pbs
	for op in [attr for attr in dir(tb) if attr.startswith('mut') or attr.startswith('cx')]:
		if op not in tb.pbs:
			warnings.warn('{0} is registered, but its probability is NOT assigned in Toolbox.pbs. '
						  'By default, the probability is ZERO and the operator {0} will NOT be applied.'.format(
				op),
						  category=UserWarning)

def _apply_modification(population, operator, pb):
	"""
	Apply the modification given by *operator* to each individual in *population* with probability *pb* in place.
	"""
	for i in range(len(population)):
		if random.random() < pb:
			population[i], = operator(population[i])
			del population[i].fitness.values
	return population

def _apply_crossover(population, operator, pb):
	"""
	Mate the *population* in place using *operator* with probability *pb*.
	"""
	for i in range(1, len(population), 2):
		if random.random() < pb:
			population[i - 1], population[i] = operator(population[i - 1], population[i])
			del population[i - 1].fitness.values
			del population[i].fitness.values
	return population

def gep_simple(population, toolbox, n_generations, n_elites,
			   stats=None, hall_of_fame=None, verbose=__debug__):
	"""
	This algorithm performs the simplest and standard gene expression programming.
	The flowchart of this algorithm can be found
	`here <https://www.gepsoft.com/gxpt4kb/Chapter06/Section1/SS1.htm>`_.
	Refer to Chapter 3 of [FC2006]_ to learn more about this basic algorithm.

	.. note::
		The algorithm framework also supports the GEP-RNC algorithm, which evolves genes with an additional Dc domain for
		random numerical constant manipulation. To adopt :func:`gep_simple` for GEP-RNC evolution, use the
		:class:`~geppy.core.entity.GeneDc` objects as the genes and register Dc-specific operators.
		A detailed example of GEP-RNC can be found at `numerical expression inference with GEP-RNC
		<https://github.com/ShuhuaGao/geppy/blob/master/examples/sr/numerical_expression_inference-RNC.ipynb>`_.
		Users can refer to Chapter 5 of [FC2006]_ to get familiar with the GEP-RNC theory.

	:param population: a list of individuals
	:param toolbox: :class:`~geppy.tools.toolbox.Toolbox`, a container of operators. Regarding the conventions of
		operator design and registration, please refer to :ref:`convention`.
	:param n_generations: max number of generations to be evolved
	:param n_elites: number of elites to be cloned to next generation
	:param stats: a :class:`~deap.tools.Statistics` object that is updated
				  inplace, optional.
	:param hall_of_fame: a :class:`~deap.tools.HallOfFame` object that will
					   contain the best individuals, optional.
	:param verbose: whether or not to print the statistics.
	:returns: The final population
	:returns: A :class:`~deap.tools.Logbook` recording the statistics of the
			  evolution process

	.. note:
		To implement the GEP-RNC algorithm for numerical constant evolution, the :class:`geppy.core.entity.GeneDc` genes
		should be used. Specific operators are used to evolve the Dc domain of :class:`~geppy.core.entity.GeneDc` genes
		including Dc-specific mutation/inversion/transposition and direct mutation of the RNC array associated with
		each gene. These operators should be registered into the *toolbox*.
	"""
	_validate_basic_toolbox(toolbox)
	logbook = deap.tools.Logbook()
	logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

	for gen in range(n_generations + 1):
		# evaluate: only evaluate the invalid ones, i.e., no need to reevaluate the unchanged ones

		if gen != n_generations:
			invalid_individuals = [ind for ind in population if not ind.fitness.valid]
			# print(invalid_individuals)
			fitnesses = toolbox.map(toolbox.evaluate, invalid_individuals)
			# print(fitnesses)
			for ind, fit in zip(invalid_individuals, fitnesses):
				# print(fit)
				ind.fitness.values = fit
			if hall_of_fame is not None:
				hall_of_fame.update2(population)
			record = stats.compile(population) if stats else {}
			logbook.record(gen=gen, nevals=len(invalid_individuals), **record)
			#if verbose:
				#print(logbook.stream)

			if gen == n_generations:
				break

			elites =hall_of_fame[:n_elites]
			offspring = toolbox.select(population, len(population) - n_elites,2)

			# replication
			offspring = [toolbox.clone(ind) for ind in offspring]

			# mutation
			for op in toolbox.pbs:
				if op.startswith('mut'):
					offspring = _apply_modification(offspring, getattr(toolbox, op), toolbox.pbs[op])

			# crossover
			for op in toolbox.pbs:
				if op.startswith('cx'):
					offspring = _apply_crossover(offspring, getattr(toolbox, op), toolbox.pbs[op])

			# replace the current population with the offsprings
			population = elites + offspring

		else:
			invalid_individuals = [ind for ind in population if not ind.fitness.valid]
			# print(invalid_individuals)
			fitnesses = toolbox.map(toolbox.evaluate, invalid_individuals)
			# print(fitnesses)
			for ind, fit in zip(invalid_individuals, fitnesses):
				# print(fit)
				ind.fitness.values = fit
			if hall_of_fame is not None:
				hall_of_fame.update2(population)
			fitnesses1 = toolbox.map(toolbox.evaluate, hall_of_fame)
			for ind, fit in zip(hall_of_fame, fitnesses1):
				ind.fitness.values = fit
			#if verbose:
			#	print(logbook.stream)
			if gen == n_generations:
				break
			elites = hall_of_fame[:n_elites]
			offspring = toolbox.select(population, len(population) - n_elites, 2)
			# replication
			offspring = [toolbox.clone(ind) for ind in offspring]
			# mutation
			for op in toolbox.pbs:
				if op.startswith('mut'):
					offspring = _apply_modification(offspring, getattr(toolbox, op), toolbox.pbs[op])
			# crossover
			for op in toolbox.pbs:
				if op.startswith('cx'):
					offspring = _apply_crossover(offspring, getattr(toolbox, op), toolbox.pbs[op])

			# replace the current population with the offsprings
			population = elites + offspring

	return population, logbook

from operator import eq
from copy import deepcopy
import geppy as gep
class HallOfFame(object):
    """The hall of fame contains the best individual that ever lived in the
    population during the evolution. It is lexicographically sorted at all
    time so that the first element of the hall of fame is the individual that
    has the best first fitness value ever seen, according to the weights
    provided to the fitness at creation time.

    The insertion is made so that old individuals have priority on new
    individuals. A single copy of each individual is kept at all time, the
    equivalence between two individuals is made by the operator passed to the
    *similar* argument.

    :param maxsize: The maximum number of individual to keep in the hall of
                    fame.
    :param similar: An equivalence operator between two individuals, optional.
                    It defaults to operator :func:`operator.eq`.

    The class :class:`HallOfFame` provides an interface similar to a list
    (without being one completely). It is possible to retrieve its length, to
    iterate on it forward and backward and to get an item or a slice from it.
    """
    def __init__(self, maxsize, similar=eq):
        self.maxsize = maxsize
        self.keys = list()
        self.items = list()
        self.similar = similar

    def update(self, population):
        """Update the hall of fame with the *population* by replacing the
        worst individuals in it by the best individuals present in
        *population* (if they are better). The size of the hall of fame is
        kept constant.

        :param population: A list of individual with a fitness attribute to
                           update the hall of fame with.
        """
        for ind in population:
            if len(self) == 0 and self.maxsize !=0:
                # Working on an empty hall of fame is problematic for the
                # "for else"
                self.insert(population[0])
                continue
            if ind.fitness.values[0] > self[-1].fitness.values[0] or len(self) < self.maxsize:
                for hofer in self:
                    # Loop through the hall of fame to check for any
                    # similar individual
                    if self.similar(gep.simplify(ind), gep.simplify(hofer)):
                        break
                else:
                    # The individual is unique and strictly better than
                    # the worst
                    if len(self) >= self.maxsize:
                        self.remove(-1)
                    self.insert(ind)

    def update2(self, population):
        """Update the hall of fame with the *population* by replacing the
        worst individuals in it by the best individuals present in
        *population* (if they are better). The size of the hall of fame is
        kept constant.

        :param population: A list of individual with a fitness attribute to
                           update the hall of fame with.
        """
        for ind in population:
            if len(self) == 0 and self.maxsize !=0:
                # Working on an empty hall of fame is problematic for the
                # "for else"
                self.insert(population[0])
                continue
            if ind.fitness.values[0] > self[-1].fitness.values[0] or len(self) < self.maxsize:
                for hofer in self:
                    # Loop through the hall of fame to check for any
                    # similar individual
                    if self.similar(ind.fitness.values[0], hofer.fitness.values[0]):
                        break
                else:
                    # The individual is unique and strictly better than
                    # the worst
                    if len(self) >= self.maxsize:
                        self.remove(-1)
                    self.insert(ind)


    def insert(self, item):
        """Insert a new individual in the hall of fame using the
        :func:`~bisect.bisect_right` function. The inserted individual is
        inserted on the right side of an equal individual. Inserting a new
        individual in the hall of fame also preserve the hall of fame's order.
        This method **does not** check for the size of the hall of fame, in a
        way that inserting a new individual in a full hall of fame will not
        remove the worst individual to maintain a constant size.

        :param item: The individual with a fitness attribute to insert in the
                     hall of fame.
        """
        item = deepcopy(item)
        i = bisect_right(self.keys, item.fitness)
        self.items.insert(len(self) - i, item)
        self.keys.insert(i, item.fitness)

    def remove(self, index):
        """Remove the specified *index* from the hall of fame.

        :param index: An integer giving which item to remove.
        """
        del self.keys[len(self) - (index % len(self) + 1)]
        del self.items[index]

    def clear(self):
        """Clear the hall of fame."""
        del self.items[:]
        del self.keys[:]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def __str__(self):
        return str(self.items)

def bisect_right(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        # Use __lt__ to match the logic in list.sort() and in heapq
        if x < a[mid]: hi = mid
        else: lo = mid+1
    return lo

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.feature_selection import mutual_info_classif
from xgboost import plot_importance
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
def data_pre (target,a):
    data_y = a.loc[ : ,target]
    #data_x=a.drop([target],axis=1)
    data_x=a.copy()
    data_1=data_x.drop(data_x.tail(1).index)
    data_2=data_y.drop(data_y.head(1).index,)
    list1=[]
    for i in range(0,len(data_1)):
        list1.append(i)
    data_1.index =list1
    data_2.index=list1
    zz=pd.concat([data_1,data_2],axis=1)
    return zz

def RF_XG_regulators(x,y,zz, target):
    
    random.seed(42)
    np.random.seed(42)
    
    col = zz.columns
    rfc = RandomForestClassifier(n_estimators=1000, min_samples_leaf=1, n_jobs=-1, random_state=42)
    #print("error rf")
    
    rfc.fit(x, y[target])
    importance_rfc = rfc.feature_importances_
    re_rfc = pd.DataFrame({'feature':np.array(col)[:-1],'IMP':importance_rfc}).sort_values(by = 'IMP',axis = 0,ascending = False)
    re_rfc=re_rfc.head(10)
    RF_features=re_rfc["feature"].tolist()
    le = LabelEncoder()
    
    #print("warning fittransform")
    y_train = le.fit_transform(y[target])
    model = xgb.XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=160, objective='binary:logistic',
                              n_jobs=-1, random_state=42)
    
    #print(len(np.unique(y_train)))
    
    model.fit(x, y_train)
    importance_xgb = model.feature_importances_
    re_xgb = pd.DataFrame({'feature':np.array(col)[:-1],'IMP':importance_xgb}).sort_values(by = 'IMP',axis = 0,ascending = False)
    re_xgb=re_xgb.head(10)
    XG_features=re_xgb["feature"].tolist()
    
    #print(target)
    #print("randomforest", re_rfc)
    #print("xgboost", re_xgb)
    
    return RF_features, XG_features

def Regulators(target,a):
    ab=a
    regu=[]
    #print("before pre")
    zz=data_pre(target,ab)
    #print("after pre")
    #x,y = np.split(zz, (len(zz.columns)-1,), axis = 1)
    
    x = zz.iloc[:, :len(zz.columns)-1]
    y = zz.iloc[:, len(zz.columns)-1:]
    
    #print("\n", x.equals(x_), y.equals(y_), "\n")
    #print("before ml")
    RF_features,XG_features=RF_XG_regulators(x,y,zz, target)
    
    # ['p53', 'ATM', 'MDM2', 'WIP1'] ['ATM', 'p53', 'WIP1', 'MDM2']
    #RG_sets =list(set(RF_features).union(set(XG_features)))
    
    #if target == "ATM":
    #    print(RF_features, XG_features, RG_sets)
    
    RG_sets = RF_features
    
    for x in XG_features:
        if x not in RG_sets:
            RG_sets.append(x)
        
    
    #RG_sets =list(set(RF_features).union(set(XG_features)))
    
    #if target == "ATM":
    #    print(RG_sets, RF_features, XG_features)

    return RG_sets

import numpy as np
import pandas as pd
import multiprocessing
import operator
from deap import creator, base, tools
from operator import eq
#from pre_RG import Regulators
import deap
#from HallOfFame import *
#from Gep_simple import gep_simple
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing

def iterativeKmeans(data, d=3):
    data = np.array(data)
    while d > 0:
        data = np.reshape(data, (-1,1))
        clusters = pow(2, d)
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data)
        data = kmeans.cluster_centers_[kmeans.labels_]
        d = d - 1
    boolVal = kmeans.cluster_centers_[0,0] > kmeans.cluster_centers_[1,0]
    centers = np.array([int(boolVal), int(not boolVal)])
    return pd.Series(centers[kmeans.labels_].tolist())


def mlp2(raw_dataIn,y,list1):
    min_max_scaler = preprocessing.MinMaxScaler()
    # y = min_max_scaler.fit_transform(y) # if necessary
    y=y.ravel()
    X = np.array(raw_dataIn[list(set(list1))])
    # X = min_max_scaler.fit_transform(X) # if necessary
    fit1 = MLPRegressor(hidden_layer_sizes=(50, 15), activation='relu', solver='adam', alpha=0.01, max_iter=200, random_state=42)
    fit1.fit(X, y)
    pred1_train = fit1.predict(X)
    mse_1 = mean_squared_error(pred1_train, y)
    return mse_1


def mainn(target,Regulators_sets,data_Out,Input_data,binary_data,raw_dataIn,raw_dataOut,ss,rules,pre_RG=True):
    
    random.seed(42)
    np.random.seed(42)

    if pre_RG:
        Regulators_sets=Regulators(target,binary_data)
        Input_data = Input_data[Regulators_sets].values.tolist()
        #if target == "ATM":
        #    print(Regulators_sets)
    else:
        Input_data = Input_data[Regulators_sets].values.tolist()

    Out_data=data_Out[target].tolist()

    y = np.array(raw_dataOut[target].tolist()).reshape(len(raw_dataOut[target]), 1)

    pset = gep.PrimitiveSet('Main', input_names=Regulators_sets)
    pset.add_function(operator.and_, 2)
    pset.add_function(operator.or_, 2)
    pset.add_function(operator.not_, 1)

    creator.create("FitnessMin", base.Fitness, weights=(1,-1,1))  # to maximize the objective (fitness)
    creator.create("Individual", gep.Chromosome, fitness=creator.FitnessMin)

    h = 5  # head length
    n_genes = 1   # number of genes in a chromosome
    toolbox = gep.Toolbox()
    toolbox.register('gene_gen', gep.Gene, pset=pset, head_length=h)
    toolbox.register('individual', creator.Individual, gene_gen=toolbox.gene_gen, n_genes=n_genes, linker=None)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # compile utility: which translates an individual into an executable function (Lambda)
    toolbox.register('compile', gep.compile_, pset=pset)

    # def evaluate(individual):
        # """Evalute the fitness of an individual"""

        # for gene in individual:
            # input_variables=gene.kexpression
        # list1= ['' + item.name + '' for item in input_variables]

        # for item in list1[:]:
            # if item == 'and_' or item == 'or_' or item == 'not_':
                # list1.remove(item)
        # n_regulators = len(set(list1))
        # func= toolbox.compile(individual)
        # n_correct=sum(func(*pIn) ==pOut for pIn, pOut in zip(Input_data, Out_data))
        # chen=1
        # return (n_correct, n_regulators,chen)

    def evaluate(individual):
        """Evalute the fitness of an individual"""

        for gene in individual:
            input_variables = gene.kexpression
        list1 = ['' + item.name + '' for item in input_variables]
        for item in list1[:]:
            if item == 'and_' or item == 'or_' or item == 'not_':
                list1.remove(item)
        n_regulators = len(set(list1))
        func = toolbox.compile(individual)
        n_correct = sum(func(*pIn) == pOut for pIn, pOut in zip(Input_data, Out_data))
        mlp_loss = mlp2(raw_dataIn, y, list1)
        return (n_correct, n_regulators,mlp_loss)


    toolbox.register('evaluate', evaluate)

    toolbox.register('select', tools.selTournament)
    ## general mutations whose aliases start with 'mut'
    # We can specify the probability for an operator with the .pbs property
    toolbox.register('mut_uniform', gep.mutate_uniform, pset=pset, ind_pb=2 / (2 * h + 1))
    toolbox.pbs['mut_uniform'] = 0.5
    # Alternatively, assign the probability along with registration using the pb keyword argument.
    toolbox.register('mut_invert', gep.invert, pb=0.5)
    toolbox.register('mut_is_ts', gep.is_transpose, pb=0.5)
    toolbox.register('mut_ris_ts', gep.ris_transpose, pb=0.5)
    toolbox.register('mut_gene_ts', gep.gene_transpose, pb=0.5)
    ## general crossover whose aliases start with 'cx'
    toolbox.register('cx_1p', gep.crossover_one_point, pb=0.5)
    toolbox.register('cx_2p', gep.crossover_two_point, pb=0.5)
    toolbox.register('cx_gene', gep.crossover_gene, pb=0.5)
    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    n_pop = 50
    n_gen = 200
    elites=10
    pop = toolbox.population(n=n_pop)
    
    #if target == "ATM":
    #    print(pop)
    
    hof = HallOfFame(5)   # only record the best individual ever found in all generations
    # start evolution
    pop2, log = gep_simple(pop, toolbox,
                              n_generations=n_gen, n_elites=elites,
                              stats=stats, hall_of_fame=hof, verbose=False)

    hof_sort=sorted(pop2, key=lambda ind: (-int(ind.fitness.values[0]), ind.fitness.values[2]))
    hof_sort2=[gep.simplify(ind) for ind in hof_sort]
    #print(hof_sort2)

    symplified_best=hof_sort2[:1]
    #print(symplified_best)
    #with open(ss, 'a') as f:
    #    f.write(f'{target} = {symplified_best}\n')

    rules[target] = symplified_best


def LogicGep(binary_data, raw_data):
    random.seed(42)
    np.random.seed(42)
    
    Regulators_sets = list(binary_data.columns)

    rows, cols = raw_data.shape

    dataIn=binary_data.loc[0:rows-2]
    dataOut=binary_data.loc[1:rows-1]
    data_In=dataIn==1
    data_Out=dataOut==1
    Input_data=data_In[list(dataIn.columns)].values.tolist()

    raw_dataIn = raw_data.loc[0:rows - 2]
    raw_dataOut = raw_data.loc[1:rows - 1]
    ss= "result.tsv"
    #open(ss, 'w')
    manager = multiprocessing.Manager()
    rules = manager.dict()

    list1=[(x1,Regulators_sets,data_Out,data_In,binary_data,raw_dataIn,raw_dataOut,ss,True)for x1 in list(binary_data.columns)]
    processes = [ multiprocessing.Process(target= mainn, args=[name, count, data_Out, Input_data, binary_data,raw_dataIn,raw_dataOut, ss, rules, pre_RG])
    for name, count,data_Out,Input_data, binary_data,raw_dataIn,raw_dataOut,ss,pre_RG in list1]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    #print(rules)

    #print(Regulators_sets)

    df = pd.DataFrame()

    rule_list = []
    for gene in Regulators_sets:
      r = str(rules[gene][0])
      
      r = r.replace("&", "and")
      
      r = r.replace("|", "or")

      r = r.replace("~", "not ")

      rule_list.append(r)

    df['Gene'] = Regulators_sets
    df['Rule'] = rule_list

    return df

#if __name__ == "__main__":
#    raw_data = pd.read_csv("./rawdata.tsv", sep="\t", decimal=",")
#    raw_data = raw_data.apply(pd.to_numeric)
#    raw_data= raw_data.dropna()
    #print(raw_data)
#    binary_data = raw_data.apply(iterativeKmeans, axis=0)
    #print(binary_data)

#    LogicGep(binary_data, raw_data)


"""
if __name__ == "__main__":
    
    binary = {'ATM': [1, 1, 1, 0, 1, 1, 1], 'p53': [0, 1, 1, 1, 0, 0, 0], 'WIP1': [0, 0, 0, 0, 0, 0, 0], 'MDM2':[0, 1, 1, 1, 1, 1, 1]}
    binary_df = pd.DataFrame(binary)
    
    data_raw = {'ATM':[7.566794133,6.919266152,6.946090736,6.239093403,6.990152544,7.114905693,7.136699878],
               'p53':[6.495043069,6.954698878,7.189797494,7.007641718,6.728389309,6.448082276,6.246030288],
               'WIP1':[6.407645941,7.8061397,7.733830573,7.822113611,7.747800782,7.192744808,7.412382975],
               'MDM2':[5.484177372,6.068058137,6.542947218,6.653667869,6.057462484,6.056829114,6.07915675]}
    
    data_df = pd.DataFrame(data_raw)
    
    rule = []
    
    
    for i in range(10):
        print(f"iter {i}")
        rule.append(LogicGep(binary_df, data_df))
        
    #print(rule)
    
    # ['p53', 'ATM', 'MDM2', 'WIP1'] ['ATM', 'p53', 'WIP1', 'MDM2'] ['p53', 'WIP1', 'ATM', 'MDM2']
    # ['p53', 'ATM', 'MDM2', 'WIP1'] ['ATM', 'p53', 'WIP1', 'MDM2'] ['WIP1', 'p53', 'ATM', 'MDM2']
    
    first_df = rule[0]
    equal = 1
    for i in range(1, len(rule)):
        if not first_df.equals(rule[i]):
            print( "dataframees not equal")
            equal = 0
            
    if equal:
        print("dataframes equal")
        
    print(rule)
"""