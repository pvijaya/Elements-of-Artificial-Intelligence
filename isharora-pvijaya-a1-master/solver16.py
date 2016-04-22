# code goes here
#!/usr/bin/python

'''
Report:

In this problem, we have implemented a solution to reach to the goal state of a 15 puzzle configuration
provided in the file.

The program opens the file and creates the initial state of the board and then apply all the moves to each state
to fetch the 16 possible configurations of each state.

I have used one package from online, for using the priority queue function from that for sorting the f values in A* algorithm.
This package is imported into this code and will be submitted as a separate file to be included in the folder before running the code.

here is the reference for the same:
http://pydoc.net/Python/pqdict/0.5/pqdict/

Only the PQDict function is used from this file.

We have used A* algorithm to find a path to the goal node and the heuristic function takes into account the
difference between the current location of the tile and its position in the goal state and then apply some calculations
to get the admissible heuristic considering it a rotation.

I have prepared the heuristic function by calculating the total h for all the tiles of a state 
manually and have used the same approach by using some alterations and logical calculations.
For eg, when the distance is 3, it will be considered only 1 because of rotation.
		for the other values of difference between the coordinates of current state and goal state I am using the same distance.

		We cannot use just the manhattan distance as heuristic here, as the rotation will change the location of 4 tiles at once.

	In the end for the moves and path, I am storing the move and parent for each generated state and printing it by backtracking from end to the start state.
	
	For the last configuration given in the question, my program takes almost 15 minutes to finish. But it generates a small path with around 14 nodes. 
	It takes more time as the rotations are too many for the given configuration.
	
	When there are less changes in the start state, then the program completes fast and gives the optimal path.
'''
import copy
import math
import time
import bisect
import random
import itertools
import re
import sys
from pqdict import PQDict
from collections import defaultdict

'''
Class to open the file and prepare the start state and the end state for the puzzle.
It also has the functions for the possible moves for each state including the rotate_down, rotate_left,
rotate_right and rotate_up.
'''
class Board_State:

	#intialization function for the class variables.
	def __init__(self, filename):
		self.num_lines = 0
		self.line_values = []
		self._tiles = []
		
		#preparing the first start state from the passed file.
		with open(filename,'r') as f:
			for line in f:
				newline = re.sub(' ', '#', line.rstrip())
				for x in newline.rstrip().split('#'):
					self.line_values.append(x)
					
				l = []
				for word in line.strip().split(' '):
					l.append(int(word))
				self._tiles.append(l)
				self.num_lines =  self.num_lines +1
		
		#check for the size of the board
		if self.num_lines < 4:
			print "size of the board is not correct, give 4 lines in the file"
			sys.exit()
			
			
		self.size = 4
		
		#goal state for the board
		self.end = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
		
		#dictionary for storing the goal locations for each tile in the board
		self.end_index = {1:[0,0] , 2:[0,1],3:[0,2],4:[0,3],5:[1,0],6:[1,1],7:[1,2],8:[1,3],9:[2,0],10:[2,1],11:[2,2],12:[2,3],13:[3,0],14:[3,1],15:[3,2],16:[3,3]}
		
		
	#method for right rotation move based on the rownum
	def rotate_right(self,tile,row_num):
		a= tile[row_num][0]
		b = tile[row_num][1]
		c = tile[row_num][2]
		d = tile[row_num][3]
		tile[row_num][0] = d
		tile[row_num][1] = a
		tile[row_num][2] = b
		tile[row_num][3] = c
		return tile
		
	#method for left rotation move based on the rownum
	def rotate_left(self,tile,row_num):
		a= tile[row_num][0]
		b = tile[row_num][1]
		c = tile[row_num][2]
		d = tile[row_num][3]
		tile[row_num][0] = b
		tile[row_num][1] = c
		tile[row_num][2] = d
		tile[row_num][3] = a
		return tile
		
	#method for down rotation move based on the column number
	def rotate_down(self,tile,column_num):
		a= tile[0][column_num]
		b = tile[1][column_num]
		c = tile[2][column_num]
		d = tile[3][column_num]
		tile[0][column_num] = d
		tile[1][column_num] = a
		tile[2][column_num] = b
		tile[3][column_num] = c
		return tile
	
	#method for upside rotation move based on the column number
	def rotate_up(self,tile,column_num):
		a= tile[0][column_num]
		b = tile[1][column_num]
		c = tile[2][column_num]
		d = tile[3][column_num]
		tile[0][column_num] = b
		tile[1][column_num] = c
		tile[2][column_num] = d
		tile[3][column_num] = a
		return tile
	
	#method for applying a star algorithm and finding the right solution to the goal node.
	def apply_astar(self):
		print "A star algorithm running to find the goal"
		close = set()
		open = set()
		open.add(self.return_key(self._tiles))
		
		parent = {}
		
		g_score = defaultdict(lambda: math.inf)
		g_score[self.return_key(self._tiles)] = 0
		
		f_score = PQDict.minpq()
		f_matric = {}
		value = g_score[self.return_key(self._tiles)] + self.heuristic(self._tiles,self.end_index)
		
		f_score[self.return_key(self._tiles)] = value
		f_matric[self.return_key(self._tiles)] = self._tiles
		
		while open:
			temp_current_key = f_score.pop()
			current = f_matric[temp_current_key]
			
			if temp_current_key == self.return_key(self.end):
				print "goal found"
				self.construct_path(parent,moves,temp_current_key)
				print "Number of closed states are ", len(close)
				return 1
				
				
				
			if temp_current_key in open:
				open.discard(temp_current_key)
				
			
			close.add(self.return_key(current))
			
			l = self.cal_child_nodes(current)
			moves = {}
			for x in l:
				temp_node = copy.copy(l[x][0])
				
				
				
				if self.return_key(temp_node) in close:
					continue
				new_g_value = g_score[self.return_key(current)] + 1
				if self.return_key(temp_node) not in open or new_g_value < g_score[self.return_key(temp_node)]:
					parent[self.return_key(temp_node)] = [self.return_key(current),l[x][1]]
					moves[self.return_key(temp_node)] = l[x][1]
					g_score[self.return_key(temp_node)] = new_g_value
					value_new = g_score[self.return_key(temp_node)] + self.heuristic(temp_node,self.end_index)
					f_score[self.return_key(temp_node)] = value_new
					
					if self.return_key(temp_node) not in open:
						open.add(self.return_key(temp_node))
						
					if self.return_key(temp_node) not in f_matric:
						f_matric[self.return_key(temp_node)] = temp_node
		
		return 0
		
	#method for calculating the heuristic of the state passed.
	def heuristic(self,temp,end):
		h = 0
		for i in range(self.size):
			for j in range(self.size):
				x = end[temp[i][j]][0]
				y = end[temp[i][j]][1]
				diff1 = abs(x-i) 
				diff2 = abs(y-j)
				if (diff1 == 3):
					diff1 = 1
				elif diff1 == 2:
					diff1 = 2
				elif diff1 == 1:
					diff1 = 1
				elif diff1 == 0:
					diff1 = 0
				if (diff2 == 3):
					diff2 = 1
				elif diff2 == 2:
					diff2 = 2
				elif diff2 == 1:
					diff2 = 1
				elif diff2 == 0:
					diff2 = 0
				h = h + diff1 +  diff2
		return h/3
		
	#method for displaying the path of reaching the goal from the start
	def construct_path(self,parent,moves,current):
		total_path = [current]
		moves = []
		final_move = ""
		while current in parent:
			move =  parent[current][1]
			current = parent[current][0]
			total_path.append(current)
			moves.append(move)
		for i in reversed(moves):
			final_move = final_move +" "+str(i)
		print "Length of the path is " , len(total_path)
		print final_move
		return total_path
			

	#method to calculate all the 16 possible states of one particular configuration after applying all the rotations
	def cal_child_nodes(self,tile):
		new_tiles = {}
		for i in range(self.size):
			temp = copy.deepcopy(tile)
			l = copy.copy(self.rotate_right(temp,i))
			new_tiles[self.return_key(l)]=[l,"R"+str(i+1)]
		for i in range(self.size):
			temp = copy.deepcopy(tile)
			l = copy.copy(self.rotate_left(temp,i))
			new_tiles[self.return_key(l)]=[l,"L"+str(i+1)]
		for i in range(self.size):
			temp = copy.deepcopy(tile)
			l = copy.copy(self.rotate_up(temp,i))
			new_tiles[self.return_key(l)]=[l,"U"+str(i+1)]
		for i in range(self.size):
			temp = copy.deepcopy(tile)
			l = copy.copy(self.rotate_down(temp,i))
			new_tiles[self.return_key(l)]=[l,"D"+str(i+1)]
		return new_tiles

	#method for generating the key for a state using the values in each tile
	def return_key(self,tile):
		l = ""
		counter = 0
		for i in range(4):
			for j in range(4):
				if tile[i][j]:
					l = l + str(tile[i][j])
					counter = counter + 1
					
			if counter == 16:
				
				break	
		return l

		
#main method for creating the instance of the Board_State class and calling the a star algorithm
def main():
	board = Board_State("input_board.txt")
	y = board.apply_astar()
	if y == 0:
		print "Goal state is not reachable!!"
		sys.exit()
	
main()