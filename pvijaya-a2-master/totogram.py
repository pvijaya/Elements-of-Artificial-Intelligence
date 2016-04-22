#!/usr/bin/python
"""
We are using local search algorithm to set a maximum evaluations of upto 10 to a value so that we get the optimal solution for those many iterations.
Taken inspiration from http://www.psychicorigami.com/2007/04/17/tackling-the-travelling-salesman-problem-part-one/
Usage: ./totogram.py 3

"""
import sys
import random

(_ROOT, _HEIGHT, _WIDTH) = range(3)
class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)
		
class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call
			
    def compare_adjacent(self, identifier, depth=_ROOT):
	children = self[identifier].children
        depth += 1
        for child in children:
	    print (child,"->", root)
            if child < root:
		print "root is greater"
	    else:
		print "child value is greater"
	    self.compare_adjacent(child, depth)
	
	
    def traverse(self, identifier, mode=_HEIGHT):
        # Python generator. Used to traverse through BFS and DFS
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _HEIGHT:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _WIDTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item
		
if __name__ == '__main__':
	tree = Tree()
	n=int(sys.argv[1])
	# always we get the root value to be total number of nodes by 2
	if n ==3:
		limit=10
		root=limit/2
		def generator_tree():
			
			mylist=list(range(1,limit+1))
			tree.add_node(root)
			mylist.remove(root)
			
			#now 3 kids
			kid1=random.choice(mylist)
			tree.add_node(kid1,root)
			mylist.remove(kid1)

			kid2=random.choice(mylist)
			tree.add_node(kid2,root)
			mylist.remove(kid2)

			kid3=random.choice(mylist)
			tree.add_node(kid3,root)
			mylist.remove(kid3)
			
			#now we create two children for each of the above kids until the mylist is empty
			kid11=random.choice(mylist)
			tree.add_node(kid11,kid1)
			mylist.remove(kid11)
			
			kid12=random.choice(mylist)
			tree.add_node(kid12,kid1)
			mylist.remove(kid12)
			
			kid21=random.choice(mylist)
			tree.add_node(kid21,kid2)
			mylist.remove(kid21)
			
			kid22=random.choice(mylist)
			tree.add_node(kid22,kid2)
			mylist.remove(kid22)
			
			kid31=random.choice(mylist)
			tree.add_node(kid31,kid3)
			mylist.remove(kid31)
			
			kid32=random.choice(mylist)
			tree.add_node(kid32,kid3)
			mylist.remove(kid32)
			
			for node in tree.traverse(root, mode=_WIDTH):
				print(node)
			
			tree.compare_adjacent(root)
		generator_tree()
		
		max_evaluations=10
		def init_random_tour(limit):
		   tour=range(limit)
		   random.shuffle(tour)
		   return tour
		
		#initialization function 
		init_function=lambda: init_random_tour(limit)
		objective_function=lambda tour: -limit(tree,tour)
		
		def swapped_cities(tour):
    			'''generator to create all possible variations
      				where two cities have been swapped'''
			for i,j in all_pairs(len(tour)):
				if i < j:
					copy=tour[:]
					copy[i],copy[j]=tour[j],tour[i]
					yield copy
		
		def hillclimb(init_function,move_operator,objective_function,max_evaluations):
			'''
			hillclimb until either max_evaluations
			is reached or we are at a local optima
			'''
			best=init_function()
			best_score=objective_function(best)
			
			num_evaluations=1
			
			while num_evaluations < max_evaluations:
				# examine moves around our current position
				move_made=False
				for next in move_operator(best):
					if num_evaluations >= max_evaluations:
						break
					
					# see if this move is better than the current
					next_score=objective_function(next)
					num_evaluations+=1
					if next_score > best_score:
						best=next
						best_score=next_score
						move_made=True
						break # depth first search
					
				if not move_made:
					break # we couldn't find a better move 
							 # (must be at a local maximum)
			
			return (num_evaluations,best_score,best)
		def hillclimb_and_restart(init_function, move_operator,objective_function,max_evaluations):
    			'''
    			repeatedly hillclimb until max_evaluations is reached
    			'''
			best=None
			best_score=0
			
			num_evaluations=0
			while num_evaluations < max_evaluations:
				remaining_evaluations=max_evaluations-num_evaluations
				
				evaluated,score,found=hillclimb(
					init_function,
					move_operator,
					objective_function,
					remaining_evaluations)
				
				num_evaluations+=evaluated
				if score > best_score or best is None:
					best_score=score
					best=found
				
			return (num_evaluations,best_score,best)
			
			
		hillclimb_and_restart(init_function,swapped_cities,objective_function,max_evaluations)
