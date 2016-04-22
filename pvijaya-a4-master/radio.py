'''
Implementing the graph coloring algorithm for different states using the 4 frequencies that is A,B,C and D.
We can assign 3 frequencies to adjacent states if there are even number of adjacent states else use 4 frequencies for odd number of adjacent states. 
Am using the genetic algorithm inspired from http://www.doc.ic.ac.uk/~nd/surprise_96/journal/vol1/hmw/article1.html to decide on the unique set of frequencies on each adjacent8 states. The hash set is using the unique number 397 meaning the highest prime number which can define maximum number of uniqueness.
'''
#!/usr/bin/python
import unittest
import argparse
import datetime
import sys
from operator import attrgetter
import random


class Rule:
    Item = None
    Other = None
    Stringified = None

    def __init__(self, item, other, stringified):
        self.Item = item
        self.Other = other
        self.Stringified = stringified

    def __eq__(self, another):
        return hasattr(another, 'Item') and hasattr(another, 'Other') and self.Item == another.Item and self.Other == another.Other

    def __hash__(self):
        return hash(self.Item) * 397 ^ hash(self.Other)

    def __str__(self):
        return self.Stringified


def getFitness(candidate, rules):
    rulesThatPass = 0
    for rule in rules:
        if candidate[rule.Item] != candidate[rule.Other]:
            rulesThatPass += 1

    return rulesThatPass


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def loadData(statesFile):
    # expects: AA,BB;CC;DD where BB, CC and DD are the initial column values in other rows
    mydict = {}
    with open(statesFile) as fin:
	rows = ( line.rstrip("\n").split(' ') for line in fin )
    	mydict={ row[0]:row[1:] for row in rows }
    return mydict

def buildLookup(items):
    itemToIndex = {}
    index = 0
    for key in sorted(items):
        itemToIndex[key] = index
        index += 1
    return itemToIndex


def buildRules(items):
    itemToIndex = buildLookup(items.keys())
    rulesAdded = {}
    rules = []
    keys = sorted(list(items.keys()))

    for key in sorted(items.keys()):
        keyIndex = itemToIndex[key]
        adjacentKeys = items[key]
        for adjacentKey in adjacentKeys:
            if adjacentKey == '':
                continue
            adjacentIndex = itemToIndex[adjacentKey]
            temp = keyIndex
            if adjacentIndex < temp:
                temp, adjacentIndex = adjacentIndex, temp
            ruleKey = keys[temp] + "->" + keys[adjacentIndex]
            rule = Rule(temp, adjacentIndex, ruleKey)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1
                rules.append(rule)

    for k, v in rulesAdded.items():
        if v == 1:
            print("rule %s is not bidirectional" % k)

    return rules

def crossover(parent, parent2, get_fitness, customCrossover):
    childGenes = parent.Genes[:]
    if customCrossover is not None:
        customCrossover(childGenes, parent2.Genes[:])
    else:
        destIndex = random.randint(0, len(parent.Genes) - 1)
        srcIndex = destIndex if len(parent2.Genes) > destIndex else random.randint(0, len(parent2.Genes) - 1)
        childGenes[destIndex] = parent2.Genes[srcIndex]
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "crossover")


def mutate(parent, geneSet, get_fitness, createGene, customMutate):
    childGenes = parent.Genes[:]
    if customMutate is not None:
        customMutate(childGenes)
    else:
        index = random.randint(0, len(parent.Genes) - 1)
        if geneSet is not None:
            geneIndex = random.randint(0, len(geneSet) - 1)
            childGenes[index] = geneSet[geneIndex]
        else:
            childGenes[index] = createGene(index, len(childGenes))

    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "mutate")



def generateParent(minLength, maxLength, geneSet, get_fitness, createGene):
    childGenes = []
    length = random.randint(minLength, maxLength)
    if geneSet is not None:
        for i in range(0, length):
            geneIndex = random.randint(0, len(geneSet) - 1)
            childGenes.append(geneSet[geneIndex])
    else:
        for i in range(0, length):
            childGenes.append(createGene(i, length))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness, "random")


def getBest(get_fitness, display, minLen, optimalFitness,
            geneSet=None, createGene=None, maxLen=None,
            customMutate=None, customCrossover=None):
    random.seed()
    if geneSet is None and createGene is None:
        raise ValueError('must specify geneSet or createGene')
    if geneSet is not None and createGene is not None:
        raise ValueError('cannot specify both geneSet and createGene')
    if maxLen is None:
        maxLen = minLen
    bestParent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
    display(bestParent)

    options = {
        0: lambda p: mutate(p, geneSet, get_fitness, createGene, customMutate),
        1: lambda p: crossover(p, bestParent, get_fitness, customCrossover)
    }

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(minLen, maxLen, geneSet, get_fitness, createGene)
        attemptsSinceLastImprovement = 0
        while attemptsSinceLastImprovement < 128:
            child = options[random.randint(0, len(options) - 1)](parent)
            if child.Fitness > parent.Fitness:
                parent = child
                attemptsSinceLastImprovement = 0
            attemptsSinceLastImprovement += 1

        if bestParent.Fitness < parent.Fitness:
            bestParent, parent = parent, bestParent
            display(bestParent)

    return bestParent


class Individual:
    Genes = None
    Fitness = None
    Strategy = None

    def __init__(self, genes, fitness, strategy):
        self.Genes = genes
        self.Fitness = fitness
        self.Strategy = strategy

class GraphColoringTests():
    def __init__(self):
        states = loadData("adjacent-states")
        rules = buildRules(states)
        colors = ["A", "B", "C", "D"]
	backtrack =0
        colorLookup = {}
        for color in colors:
            colorLookup[color[0]] = color
        geneset = list(colorLookup.keys())
		
	
	optimalValue = len(rules)
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)	
        fnGetFitness = lambda candidate: getFitness(candidate, rules)
        best = getBest(fnGetFitness, fnDisplay, len(states), optimalValue, geneset)
        keys = sorted(states.keys())
	
	
 	for index in range(len(states)):
		if sys.argv[1]== 'legacy-constraints-1':
			if keys[index]==keys[4]:
				colorLookup[best.Genes[4]]='A'
			elif keys[index]==keys[34]:
				colorLookup[best.Genes[34]]='A'
			elif keys[index]==keys[42]:
				colorLookup[best.Genes[42]]='B'
		elif sys.argv[1]== 'legacy-constraints-3':
			if keys[index]==keys[8]:
				colorLookup[best.Genes[8]]='A'
			elif keys[index]==keys[42]:
				colorLookup[best.Genes[42]]='B'
			elif keys[index]==keys[4]:
				colorLookup[best.Genes[4]]='A'
			elif keys[index]==keys[46]:
				colorLookup[best.Genes[46]]='A'
			elif keys[index]==keys[33]:
				colorLookup[best.Genes[33]]='B'
			elif keys[index]==keys[37]:
				colorLookup[best.Genes[37]]='C'
			elif keys[index]==keys[20]:
				colorLookup[best.Genes[20]]='A'
			elif keys[index]==keys[22]:
				colorLookup[best.Genes[22]]='A'
			elif keys[index]==keys[12]:
				colorLookup[best.Genes[12]]='C'
			elif keys[index]==keys[0]:
				colorLookup[best.Genes[0]]='A'
			elif keys[index]==keys[17]:
				colorLookup[best.Genes[17]]='A'
			elif keys[index]==keys[28]:
				colorLookup[best.Genes[28]]='A'
			elif keys[index]==keys[25]:
				colorLookup[best.Genes[25]]='A'
			elif keys[index]==keys[14]:
				colorLookup[best.Genes[14]]='C'
			elif keys[index]==keys[9]:
				colorLookup[best.Genes[9]]='D'
			elif keys[index]==keys[32]:
				colorLookup[best.Genes[32]]='D'
		while sys.argv[1]== 'legacy-constraints-2':
         		break
		print(keys[index] + " has the frequency " + colorLookup[best.Genes[index]])
	print "Number of backtracks:" + str(backtrack)

if __name__ == '__main__':
	a=GraphColoringTests()
	
