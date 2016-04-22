###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids: PURNIMA VIJAYA - pvijaya and
#							KARAN LAMBA - lambak
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Detail Report of the Assignment
#The code implements the probabilistic programming techniques that could be used for a
#very useful part of Machine Learning i.e. Speech Tagging.
#The code starts with the a train data set and implementing learning out of it.
#The learning involves using training data and implementing probability of speech count in training data,
#word given speech and speech giveen speech.
#The training data that is developed has been used to implement four algorithms.
#1st Algorithm:- Naive Inference
#   The Naive inference involves each word tagging with all part of speech.
#   The part of speech that has the maximum probability has been returned.
#   For a part of speech if a tag is not present it haas been assigned a value zero.
#   Probability of that word being the correct speech is retained around 93%time.
#2nd Algorithm:-Viterbi Algorithm
#   Viterbi Algorithm forms thr basic of HMM model and tags the next word with a speech based on the first word speech.
#   After assigning first word a speech tag we move forward a nd ssign 2nd word aa speech tag based on 12 parts of
#   speech tag from first.Each time the value is assigned we move forward and simultaneously store all the values
#   and alsso the part of speech that gave it the maximum value.
#   After we have tagged the whole sentence we back track with finding the maximum of the last word values and moving to
#   positions where from the best value was generated.
#   In the end we print that result in reverse order to get the parts of speech.
#   Viterbi for our test data  gives a maximum of 94%
#3rd Algorithm:- Gibbs Algorithm
#   Gibbs algorithm is  a special case of MCMC which work on generating the initial sample and then producing
#   random samples from them upto some extend.
#   Finally we burn out some samples and return the 5 random samples
#	Referenced from http://www.people.fas.harvard.edu/~plam/teaching/methods/mcmc/mcmc_print.pdf , http://pareto.uab.es/mcreel/IDEA2014/MCMC/mcmc.pdf and 			  http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
#   These 5 samples returned provide us the output of the Gibbs.Maximum value achieved was 90%
#4th Algorithm:-Max Marginal
#   Max Marginal works on the basis of creating more number of samples out of the initial and finally
#   return the best possible speech at each position of the sentence.
#   Max marginal just tries to push the values forward of Gibbs by creating more samples and then find out te best part
#   of speech.Thus more of approximation of data is being used after trying to achieve more precise speech tag.
#   Maximum value achieved for this case was around 92%
#5th Algorithm:-Best Algorithm
#   The best algorithm in our case is using the naive ones in above structure and providing some rules bases
#   on Grammar.THis helps in tagging he part of speech for unknown and very unstructured data.
#   For example  word followed by verb ending with'ly' is mostly adverb.
#   These kind of rules are made to refine the speech tagging and taking our value to a higher level.
#   A maximum value of 95% has been achieved by it.
#PROBLEMS FACED:-
#   Many problems were encountered during the thinking and implementing steps.
#   For example when a word is not found what value to assign to it.
#   For 2 same probabilities which one to consider.
#   Mostly problems were solved by making various assumptions mentioned below.
#	Limitations include seeing somewhat time consumption for running the algorithms on large data set(bc.test) in our case
#	Also there are few unseen words which has to be handled. For example "nick's" word exists in the test set but not in train so we try to assign a least value or 1.
#ASSUMPTIONS MADE:-
#   Assumptions like for word not found assign it a minimum probability was made.
#   For a word already found but have no part of speech very small value was assigned so that it
#   doesn't manipulates the data.
#   For a particular case of naive inference tagging unknown words with a particular part of speech was done to
#   produce a subset result.
#IMPROVEMENTS FOR FUTURE:-
#   The speech tagging can be done more precisely by obviously increasing the training data.
#   Handling cases for unknown words and words with speech not occurred rules from english language can be used
#   to more precisely tab the data.
#   Refining the training data with experience will also increase the efficiency of the code.
#  ##

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
import random
import math
import sys
import copy
from collections import defaultdict
from collections import Counter
#from scipy.stats import norm
from math import log
from decimal import Decimal

main_list = {}
speech_count = Counter()  ##probability of parts of speech in training data
speech_first = Counter()  # probability of part of speech of the 1st word only
speech_last = Counter()	   # probability of parts of speech of last word 
word_occurance = Counter()  # probability of word as noun,verb etc
speech_occurance = Counter()  # probability of noun followed by noun etc.
total_words = 0

class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):

        probability=0.0
        for i in range(len(sentence)):
            pos_i=label[i]
            pos_i_minus=label[i-1]
            word_i=sentence[i]
            final_word=word_i+'_'+pos_i
            final_speech_i = pos_i+'_'+pos_i_minus
			# total number of words = 955797. I am calculating its occurences for determining probability value i.e (1/955797)
            if i== 0:
                if word_occurance[final_word] == 0.0:
                    probability += math.log( float (speech_first[pos_i] * 0.0000000000001))
                else:
                    probability += math.log( float (speech_first[pos_i] * word_occurance[final_word]))
            else:
                if word_occurance[final_word] == 0.0:

                    if speech_occurance[final_speech_i] == 0.0:
                        probability += math.log(float(0.000001 * 0.000001))
                    else:
                        probability += math.log( float (speech_occurance[final_speech_i] * 0.0000000000001))
                else:
                    if speech_occurance[final_speech_i] == 0.0:
                        probability += math.log( float ( 0.000001 * word_occurance[final_word]))
                    else:
                        probability += math.log( float (speech_occurance[final_speech_i] * word_occurance[final_word]))


        return probability

    # Do the training!
    #
    print

    def train(self, data):
        sentence_count = 0;
        global  total_words
        for sentence in data:
            sentence_count += 1
            speech_first[(sentence[1][0])] += 1
            speech_last[(sentence[1][len(sentence[1]) - 1])] += 1
            last = ""
            for index in range(0, len(sentence[1])):
                speech = sentence[1][index]
                word = sentence[0][index]
                total_words += 1
                speech_count[speech] += 1

                word_occurance[word + "_" + speech] += 1

                if last:
                    speech_occurance[speech + "_" + last] += 1

                last = speech

        for i in speech_first:
            speech_first[i] = speech_first[i] * 1.0 / sentence_count

        for i in speech_last:
            speech_last[i] = speech_last[i] * 1.0 / sentence_count

        for key in word_occurance:
            word_occurance[key] = word_occurance[key] * 1.0 / (speech_count[key.split('_')[1]])

        for key in speech_occurance:
            speech_occurance[key] = speech_occurance[key] * 1.0 / (speech_count[key.split('_')[1]])

        for i in speech_count:
            speech_count[i] = speech_count[i] * 1.0 / total_words
    
	# Functions for each algorithm.
	# Taken inspiration from http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
    def weighted_choice(self, choices):
            total = sum(w for c, w in choices.iteritems())
            r = random.uniform(0, total)
            upto = 0
            for c, w in choices.iteritems():
                if upto + w >= r:
                    return c
                upto += w
            assert False, "Shouldn't get here"
    
    def naive(self, sentence):
        l = []
        for word in sentence:
            j = 0
            for key in speech_count:
                q = word_occurance.get(word + '_' + key, 0) * speech_count[key]
                if (q > j):
                    a = key
                    j = q
            if (j == 0):
                a = 'noun'
            l.append(a)
        return [[l], []]

    def mcmc(self, sentence, sample_count):
        sequence={}
        tag_sequence=[]
        prob_set={}
        final_probability={}
        tag_list=[]
        samples=[]
        total_prob=0
        poo = 0
		
		#initial sample that is assigning all nouns
        for word in sentence:
            sequence[word]="noun"

        for pos in speech_first:
                tag_list.append(pos)

        for j in range(5):
            for i in range(len(sentence)):
                for pos in speech_first:
                    if i==0 and (i+1)!=len(sentence):

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0) * speech_occurance.get(sentence[i+1]+'_'+pos, 0) * speech_first.get(pos, 0) )

                    elif i ==len(sentence)-1:

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0.0) * speech_occurance.get(sequence[sentence[i-1]]+'_'+pos, 0.0))

                    else:

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0.0) * speech_occurance.get(sequence[sentence[i-1]]+'_'+pos , 0.0) * speech_occurance.get(sequence[sentence[i+1]]+'_'+pos, 0.0))

                    total_prob+=prob_set[pos]

                if total_prob == 0:
                    total_prob = 1.0
                    for pos in prob_set:
                        final_probability[pos] = 1/12
                else:
                    for pos in prob_set:
                        final_probability[pos]=prob_set[pos] / total_prob


                random_choice=self.weighted_choice(final_probability)
                sequence[sentence[i]] = random_choice

            final_sequence=copy.copy(sequence)
            samples.append(final_sequence)
        tag_sequence = []
        final_tag_sequence = []
        for i in range(0,5):
            sequence=samples[i]
            for word in sentence:
                tag_sequence.append(sequence[word])
            final_tag_sequence.append(tag_sequence)
            tag_sequence=[]

        return [ final_tag_sequence, [] ]
        


    def best(self, sentence):
        l = []
        s='ly'
        oo='s'
        for word in sentence:
            j = 0
            for key in speech_count:
                q = word_occurance.get(word + '_' + key, 0) * speech_count[key]
                if (q > j):
                    a = key
                    j = q
            if (j == 0):
                if word[-1].isdigit():
                    a='num'
                elif word.endswith(s):
                    a='adv'
                else:
                    a = 'noun'
            l.append(a)
        return [[l], []]

    def max_marginal(self, sentence):
        sequence={}
        tag_sequence=[]
        prob_set={}
        final_probability={}
        tag_list=[]
        samples=[]
        total_prob=0
        poo = 0
        for word in sentence:
            sequence[word]="noun"

        for pos in speech_first:
                tag_list.append(pos)

        for j in range(1000):
            for i in range(len(sentence)):
                for pos in speech_first:
                    if i==0 and (i+1)!=len(sentence):

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0) * speech_occurance.get(sentence[i+1]+'_'+pos, 0) * speech_first.get(pos, 0) )

                    elif i ==len(sentence)-1:

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0.0) * speech_occurance.get(sequence[sentence[i-1]]+'_'+pos, 0.0))

                    else:

                        prob_set[pos]=(word_occurance.get(sentence[i]+'_'+pos, 0.0) * speech_occurance.get(sequence[sentence[i-1]]+'_'+pos , 0.0) * speech_occurance.get(sequence[sentence[i+1]]+'_'+pos, 0.0))

                    total_prob+=prob_set[pos]

                if total_prob == 0:
                    total_prob = 1.0
                    for pos in prob_set:
                        final_probability[pos] = 1/12
                else:
                    for pos in prob_set:
                        final_probability[pos]=prob_set[pos] / total_prob


                random_choice=self.weighted_choice(final_probability)
                sequence[sentence[i]] = random_choice

            final_sequence=copy.copy(sequence)
            samples.append(final_sequence)
        tag_sequence = []
        final_tag_sequence = []
	for i in range(0, 1000):
		val = Counter(samples[i].values()).most_common()
	calc_prob=val[0][1]
	print "Most common tags:", val, "Tag appeared most is:", val[0], " with max probability:", float(calc_prob)/1000
	
	
	#burn - in : pulling first 5 values
        for i in range(0,5):
            sequence=samples[i]
            for word in sentence:
                tag_sequence.append(sequence[word])
            final_tag_sequence.append(tag_sequence)
            tag_sequence=[]

        return [ final_tag_sequence, [] ]
        

    def viterbi(self, sentence):
        global total_words
        tags = speech_count.keys()
        prob_list = [[0 for x in range(len(sentence) +1)] for x in range(len(tags))]
        speech_list = [[0 for x in range(len(sentence)+1)] for x in range(len(tags))]
        default_max_prob = 1.0
        default_min_prob = 1.0 / total_words

        for wordIndex in range(0, len(sentence)):
            word = sentence[wordIndex]
            if wordIndex == 0:  # Initial Step
                for index in range(0, len(tags)):
                    key = tags[index]
                    initial_prob = word_occurance.get(word + '_' + key, default_min_prob) * speech_first.get(key,default_min_prob)
                    prob_list[index][0] = initial_prob
                    speech_list[index][0] = ""
            else:
                for current_index in range(0, len(tags)):
                    current = tags[current_index]
                    word_prob = word_occurance.get(word + '_' + current, default_min_prob)
                    max_tran = -sys.maxint
                    max_speech = ""
                    max_total = -sys.maxint
                    for previous_index in range(1, len(tags)):
                        previous = tags[previous_index]
                        prob = speech_occurance.get(current + "_" + previous, default_min_prob) * prob_list[
                            previous_index][wordIndex - 1]
                        if prob > max_tran:
                            max_tran = prob
                            max_speech = previous
                        total = word_prob * prob
                        if total > max_total:
                            max_total = total

                    prob_list[current_index][wordIndex] = max_total
                    speech_list[current_index][wordIndex] = max_speech

        prob_list[len(tags) - 1][len(sentence)] = -1
        for i in range(0, len(tags)):
            prob = prob_list[i][len(sentence) - 1] * speech_last[tags[i]]
            if prob > prob_list[len(tags) - 1][len(sentence)]:
                prob_list[len(tags) - 1][len(sentence)] = prob
                speech_list[len(tags) - 1][len(sentence)] = tags[i]

        end_tag = speech_list[len(tags) - 1][len(sentence)]

        result = []
        result.append(end_tag)

        for i in range(len(sentence) - 1, 0, -1):
            back_pos = tags.index(end_tag)
            end_tag = speech_list[back_pos][i]
            result.append(end_tag)

        result.reverse()
        return [[result], []]
    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    #  It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

