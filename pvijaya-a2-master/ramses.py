#!/usr/bin/python

"""
The code uses minimax algorithm to determine the next best move to be made by the user to avoid same set of rows, columns and diagonals. Assuming both the players are applying 'X' in their grid cells.The code works for 3*3 grid.
Usage : ./ramses.py 3 .X......X 3

"""

import sys
import re

class GAME:
	def __init__(self,n,s,t):
		self.board = ['.' for i in range(0,n*n)]
		self.lastmoves = []
		self.winner=None
		indices = []
		for i in range(n*n):
			if s[i] == 'x':
				indices.append(i)
        	print indices
		for j in range(0,n*n,n):
			for i in range(n):
				for val in indices:
					self.board[val]='x'
						
	def print_board(self):
		print "\n The board looks like:"
		for j in range(0,n*n,n):
			for i in range(n):
				if self.board[j+i] == '.':
					print "%d |" %(j+i),
				else:
					print "%s |" %self.board[j+i],
					
			print "\n",
	
	def get_open_positions(self):
		moves=[]
		for i,v in enumerate(self.board):
			if v=='.':
				moves.append(i)
		return moves
	
	def mark(self,marker,pos):
        	self.board[pos] = marker
        	self.lastmoves.append(pos)
	
			
	def revert_last_move(self):
		self.board[self.lastmoves.pop()]='.'
		self.winner = None
		
	def is_gameover(self):
		win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]
		for i,j,k in win_positions:
			if self.board[i] == self.board[j] == self.board[k] and self.board[i] == '.':
                		self.winner != self.board[i]
                		return True
			if i not in win_positions:
				if j not in win_positions:
					if k not in win_positions:
						if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '.':
							self.winner = self.board[i]
							return True

        	
	def play(self,player):
        
        	self.p = player
    
        	for i in range(n*n):

            		self.print_board()
            
            		self.p.move(self)


            		if self.is_gameover():
                		self.print_board()
                		if self.winner == '.':
                    			print "\nGame over with Draw"
                		else:
                    			print "\nWinner : %s" %self.winner
				return
	
		


class algorithm:
	def __init__(self,marker):
		self.marker=marker
		self.type='C'
		if self.marker == 'x':
            		self.opponentmarker = 'x'
        	else:
            		self.opponentmarker = 'x'
	
	def move(self,gameinstance):
		move_position,score = self.maximized_move(gameinstance)
		print "Recommend putting your pebble in position %d " %move_position
        	gameinstance.mark(self.marker,move_position)
		
	def maximized_move(self,gameinstance):
		
		bestscore = None
        	bestmove = None
		
        	for m in gameinstance.get_open_positions():
            		gameinstance.mark(self.marker,m)
        
            		if gameinstance.is_gameover():
                		score = self.get_score(gameinstance)
            		else:
                		move_position,score = self.minimized_move(gameinstance)
        
            		gameinstance.revert_last_move()
            
            		if bestscore == None or score < bestscore:
                		bestscore = score
                		bestmove = m
			
        	return bestmove, bestscore

	def minimized_move(self,gameinstance):
        
		bestscore = None
        	bestmove = None
		
        	for m in gameinstance.get_open_positions():
            		gameinstance.mark(self.opponentmarker,m)
               		if gameinstance.is_gameover():
                		score = self.get_score(gameinstance)
            		else:
                		move_position,score = self.maximized_move(gameinstance)
        
            		gameinstance.revert_last_move()
            
            		if bestscore == None or score > bestscore:
                		bestscore = score
                		bestmove = m

        	return bestmove, bestscore

	def get_score(self,gameinstance):
		if gameinstance.is_gameover():
			if gameinstance.winner  == self.marker:
				return 1 # Won
			elif gameinstance.winner == self.opponentmarker:
				return -1 # Opponent won
        	return 0 # Draw

if __name__ == '__main__':
	n=int(sys.argv[1])
	s=sys.argv[2]
	t=sys.argv[3]
	game=GAME(n,s,t)
	
	player=algorithm("x")
	game.play(player)
	
	
