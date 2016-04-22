# Automatic Zacate game player
# B551 Fall 2015
# Purnima Vijaya- pvijaya 
#
# Based on skeleton code by D. Crandall
#
# Trying to use a greedy approach to determine which category to be assigned to what rolling of dice.Depending on whatever first roll value we get based on that we assign the category which best fits the particular set so as to achieve the maximum score.We continue this until we complete assigning to all of those categories.
#Determining probabilities for few roll occurences we get the first dice rolling 
#
#
# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#

from ZacateState import Dice
from ZacateState import Scorecard
import random
import operator

class ZacateAutoPlayer:

      def __init__(self):
            pass  

      def first_roll(self, dice, scorecard):
		        '''dice=dice.dice
			scorecard = scorecard.scorecard
			counts = [dice.count(i) for i in range(1,7)]
			max_value=max(counts)'''
			def random_distr(l):
				assert l # don't accept empty lists
				r = random.uniform(0, 1)
				s = 0
				for i in xrange(len(l)):
					item, prob = l[i]
					s += prob
					if s >= r:
						l.pop(i) # remove the item from the distribution
						break
				else: # Might occur because of floating point inaccuracies
					l.pop()
				# update probabilities based on new domain
				d = 1 - prob 
				for i in xrange(len(l)):
					l[i][1] /= d
				return item, l

			dist = [[1, 0.9], [2, 0.8], [3, 0.7], [4, 0.6], [5, 0.5], [6, 0.598]]
			while dist:
				val, dist = random_distr(dist)
				dice=val
			print dice

			return [] #always re-roll first die (blindly)

      def second_roll(self, dice, scorecard):
	    return [] #always re-roll second and third dice (blindly)
      
      def third_roll(self, dice, scorecard):
            # stupidly just randomly choose a category to put this in return random.choice( list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())) )
			dice=dice.dice
			
			scorecard = scorecard.scorecard
			print scorecard
			
			counts = [dice.count(i) for i in range(1,7)]
			
			if any("unos" not in s for s in scorecard) and counts[0]*1 > counts[1]*2 and counts[2]*3 and counts[3]*4 and counts[4]*5 and counts[5]*6 :
				return "unos"
				
			elif any("doses" not in s for s in scorecard) and counts[1]*2 > counts[0]*1 and counts[2]*3 and counts[3]*4 and counts[4]*5 and counts[5]*6:
				scorecard=i
				return "doses"
				
				
			elif any("treses" not in s for s in scorecard) and counts[2]*3 > counts[0]*1 and counts[1]*2 and counts[3]*4 and counts[4]*5 and counts[5]*6:
				scorecard=i
				return "treses"
				
				
			elif any("cuatros" not in s for s in scorecard) and counts[3]*4 > counts[0]*1 and counts[2]*3 and counts[1]*2 and counts[4]*5 and counts[5]*6:
				scorecard=i
				return "cuatros"
				
				
			elif any("cincos" not in s for s in scorecard) and counts[4]*5 > counts[0]*1 and counts[2]*3 and counts[3]*4 and counts[1]*2 and counts[5]*6:
				scorecard=i
				return "cincos"
				
				
			elif any("seises" not in s for s in scorecard) and counts[5]*6 > counts[0]*1 and counts[2]*3 and counts[3]*4 and counts[4]*5 and counts[1]*2:
				scorecard=i
				return "seises"
				
				
			elif any("quintupulo" not in s for s in scorecard) and max(counts) == 5:
				scorecard=i
				return "quintupulo"
				
			
			elif any("cuadruple" not in s for s in scorecard) and max(counts) >= 4:
				scorecard=i
				return "cuadruple"
				
			elif any("triple" not in s for s in scorecard) and max(counts) >= 3:
				scorecard=i
				return "triple"
				
			elif any("elote" not in s for s in scorecard) and (2 in counts) and (3 in counts):
				scorecard=i
				return "elote"
			
			elif any("pupusa de queso" not in s for s in scorecard) and sorted(dice) == [1,2,3,4,5] or sorted(dice) == [2,3,4,5,6]:
				scorecard=i
				return "pupusa de queso"
			
			elif any("pupusa de frijol" not in s for s in scorecard) and (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0):
				scorecard=i
				return "pupusa de frijol"
				
			elif any("tamal" not in s for s in scorecard):
				return "tamal"
				
			else:
				return "unos" 
			
			#return max(scorecard.scorecard.keys().iteritems(), key=operator.itemgetter(1))[0]
			

