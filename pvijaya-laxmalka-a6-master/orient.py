#--------------------------------------------REPORT---------------------------------------------
'''
KNN Classifier:
---------------
We use euclidean distance formula for the KNN classifier. Below is the confusion matrix and it's corresponding output.
[pvijaya@silo pvijaya-laxmalka-a6]$ python orient.py train-data.txt test-data.txt knn 5
KNN - Accuracy: 69.88335100742312%
****************CONFUSION MATRIX USING KNN CLASSIFIER***************

[166, 18, 34, 21]
[19, 156, 15, 34]
[38, 25, 158, 15]
[13, 32, 20, 179]
Time taken to run code: 102.675163869 minutes
-----------------------------------------------------------------------------------
[pvijaya@silo pvijaya-laxmalka-a6]$ python orient.py train-data.txt test-data.txt knn 8
KNN - Accuracy: 69.77730646871686%
****************CONFUSION MATRIX USING KNN CLASSIFIER***************

[163, 17, 30, 29]
[17, 155, 14, 38]
[34, 20, 159, 23]
[16, 29, 18, 181]
Time taken to run code: 109.66360925 minutes
-----------------------------------------------------------------------------------
[pvijaya@silo pvijaya-laxmalka-a6]$ python orient.py train-data.txt test-data.txt knn 10
KNN - Accuracy: 69.67126193001062%
****************CONFUSION MATRIX USING KNN CLASSIFIER***************

[163, 16, 33, 27]
[21, 155, 13, 35]
[32, 22, 158, 24]
[13, 31, 19, 181]
Time taken to run code: 102.11449095 minutes
-----------------------------------------------------------------------------------
[pvijaya@silo pvijaya-laxmalka-a6]$ python orient.py train-data.txt test-data.txt knn 15
KNN - Accuracy: 69.98939554612937%
****************CONFUSION MATRIX USING KNN CLASSIFIER***************

[159, 19, 32, 29]
[20, 166, 10, 28]
[31, 26, 158, 21]
[15, 36, 16, 177]
Time taken to run code: 100.488153017 minutes

==========================================================================================================================
Neural Network Classification:
-----------------------------
We represent the Neural Network by an object of the NNet class. The parameter to this object is a list containing number of nodes in each layer of the Neural Network.
The Neural Network in our problem comprises of three layers: an input layer, a hidden layer and an output layer.
-Input Layer: Contains 192 nodes represent 192 elements in the feature vector.
-Hidden Layer: Can contain any number of nodes. Ideally has 10 nodes.
-Output Layer: This is four node layer. Each node representing one of the four labels-0,90,180,270
A NNet Class object is defined by the above three hyperparameters.
Initially, the weights between :i/p layer & hidden layer, hidden layer & output layer are set to random values 
-------------------------------------------------
(1)Scaling the Inputs to Neural Network: 
The Network is fed with (X,Y) tuples as i/p where X is an array of size (192 X 1) 
denoting feature vector of each example such that the feature vector values are scaled between 0 and 1. 
Y is an array of size(4 X 1) representing actual label of the example such that:
if the original label is 0=> Y is [1,0,0,0] 
if the original label is 90=> Y is [0,1,0,0]
if the original label is 180=> Y is [0,0,1,0]
if the original label is 270=> Y is [0,0,0,1]
--------------------------------------------------------
(2)Algorithm: Stochastic gradient descent
	weights=random()
	for Each example(x,y) in training set do
		#feed forward
		for each node i in input layer do
			activation=x[i]
			for l=2 to LastLayer do
				for each node j in layerL do
					z = SUM(weights[i][j].activation[i])
					activation = sigmoid(z)
		#Back Propogation
		for each node j in output layer do
			delta[j] = sigmoid_deriv(z[j])*(Y[j]-activation[j])
		for l=L-1 to 1 do
			for each node i on layerL do
				delta[i]=sigmoid_deriv*SUM(weights[i][j]*delta)
		#update weights
		for each weight in network do
			weight[i][j] = weight[i][j] - learningparameter*activation[i]*delta[j]
		until all examples in training set are explored
-------------------------------------------------------------------------
(3) sample output
python orient.py train-data.txt test-data.txt nnet 10
training....
training set length 36976
testing...
*******CONFUSION MATRIX USING NEURAL NET********
[[ 161.   24.   39.   15.]
 [  12.  173.   22.   17.]
 [  22.   31.  177.    6.]
 [  12.   42.   21.  169.]]
Classification accuracy - Neural Net : 72.1102863203 %
Duration: 19.126789093 seconds
--------------------------------------------------------------------------------
'''
import operator	
import numpy as np
import random
import math
import sys
from timeit import default_timer
			

class knn:
	def loadDataset(self, trainfile_name, testfile_name, trainingSet=[] , testSet=[]):
		with open(trainfile_name) as f:
			for line in f:
				line = line.split() # to deal with blank 
				trainingSet.append(line)
		with open(testfile_name) as f:
			for line in f:
				line = line.split() # to deal with blank 
				testSet.append(line)
		
		
	def euclideanDistance(self, instance1, instance2, length):
		distance = 0
		for x in range(2,length):
			distance += pow((int(instance1[x]) - int(instance2[x])), 2)
		return math.sqrt(distance)
	 
	def getNeighbors(self, trainingSet, testInstance, k):
		distances = []
		length = len(testInstance)
		for x in range(0,len(trainingSet)):
			dist = self.euclideanDistance(testInstance, trainingSet[x], length)
			distances.append((trainingSet[x], dist))
		distances.sort(key=operator.itemgetter(1))
		neighbors = []
		for x in range(int(k)):
			neighbors.append(distances[x][0])
		return neighbors

	def getResponse(self, neighbors):
		classVotes = {}
		for x in range(0,len(neighbors)):
			response = neighbors[x][1]
			if response in classVotes:
				classVotes[response] += 1
			else:
				classVotes[response] = 1
		#print "classvotes:", classVotes
		sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
		#print "sortedVotes:",sortedVotes,"sortedVotes 0 0:", sortedVotes[0][0]
		return sortedVotes[0][0]

	def getAccuracy(self, testSet, predictions):
		correct = 0
		for x in range(0,len(testSet)):
			if testSet[x][1] == predictions[x]:
				correct += 1
		return (correct/float(len(testSet))) * 100.0
		
class NNet(object):
    
    def __init__(self, network_specs):  # network_specs is a list of size 3 representing number of nodes in i/p layer, hidden layer and output layer
        #defining hyper parameters
        self.network_specs = network_specs
        self.total_layers = len(network_specs)
        self.weights=[]
        for x, y in zip(network_specs[:-1], network_specs[1:]):
            self.weights.append(np.random.randn(y, x)) 
    
    def gradient_descent(self, training_data, alpha):
        print "training...."
        train_len = len(training_data)
        print "training set length",train_len 
        for i in range(0,5):
            random.shuffle(training_data)
            for x,y in training_data:              #for each example in training set
                self.backpropogation(x,y,alpha)
    
    def backpropogation(self, x, y, alpha):
         activ_list = []
         z_list = []
         gradient_w = []
         for w in self.weights:
             gradient_w.append(np.zeros(w.shape)) 
         
         activ = x
         activ_list.append(x)
         
         for w in self.weights:
             z = np.dot(w, activ)
             z_list.append(z)
             activ = self.sigmoid(z)
             activ_list.append(activ)
         
         delta = (activ_list[-1] - y)*self.sigmoid_deriv(z_list[-1])
         gradient_w[-1] = np.dot(delta, activ_list[-2].T)
         
         # back propogation
         for layer in xrange(2, self.total_layers):
            z = z_list[-layer]
            sig_deriv = self.sigmoid_deriv(z)
            delta = np.dot(self.weights[-layer+1].T, delta) * sig_deriv
            gradient_w[-layer] = np.dot(delta, activ_list[-layer-1].T)
         
         #update weights
         self.weights = [w-alpha*gw for w, gw in zip(self.weights, gradient_w)]
    
    def forward_propogation(self, a):
        for w in self.weights:
            a = self.sigmoid(np.dot(w, a))
        return a
    
    def check(self, test_data, testlabels):
          test_results = [(np.argmax(self.forward_propogation(x)), y) for (x, y) in test_data]
          f = open("nnet_output.txt","w") #opens file with name of "nnet_output.txt"
          sum=0
          #print test_data
          i=0
          confusion_matrix = np.zeros((4,4))
          for (x, y) in test_results:
              assigned_label=0
              #original_label=0
              if x==0: assigned_label=0
              elif x==1: assigned_label=90
              elif x==2: assigned_label=180
              elif x==3: assigned_label=270
              
              '''if y[0]==1: original_label=0
              elif y[1]==1: original_label=90
              elif y[2]==1: original_label=180
              elif y[3]==1: original_label=270'''
              #f.write(testlabels[i]+" "+str(assigned_label)+" "+str(original_label)+'\n')
              f.write(testlabels[i]+" "+str(assigned_label)+'\n')
              itemindex = np.where(y == 1)[0]
              confusion_matrix[itemindex[0]][x]=confusion_matrix[itemindex][0][x]+1
              if(y[x][0]==1):
                  sum+=1
              i+=1    
          f.close()
          print "*******CONFUSION MATRIX USING NEURAL NET********"
          print confusion_matrix
          return sum 

    def check_best(self, test_data, testlabels):
          test_results = [(np.argmax(self.forward_propogation(x)), y) for (x, y) in test_data]
          f = open("best_output.txt","w") #opens file with name of "nnet_output.txt"
          sum=0
          #print test_data
          i=0
          confusion_matrix = np.zeros((4,4))
          for (x, y) in test_results:
              assigned_label=0
              #original_label=0
              if x==0: assigned_label=0
              elif x==1: assigned_label=90
              elif x==2: assigned_label=180
              elif x==3: assigned_label=270
              
              '''if y[0]==1: original_label=0
              elif y[1]==1: original_label=90
              elif y[2]==1: original_label=180
              elif y[3]==1: original_label=270'''
              #f.write(testlabels[i]+" "+str(assigned_label)+" "+str(original_label)+'\n')
              f.write(testlabels[i]+" "+str(assigned_label)+'\n')
              itemindex = np.where(y == 1)[0]
              confusion_matrix[itemindex[0]][x]=confusion_matrix[itemindex][0][x]+1
              if(y[x][0]==1):
                  sum+=1
              i+=1    
          f.close()
          print "*******CONFUSION MATRIX USING BEST MODEL********"
          print confusion_matrix
          return sum 

    def sigmoid(self,z):
        g_x = 1.0/(1.0+np.exp(-z))
        return g_x 
    
    def sigmoid_deriv(self,z):
        g_x_prime = self.sigmoid(z)*(1-self.sigmoid(z))
        return g_x_prime 

		
def main():
	start = default_timer()
	
	# prepare data
	trainingSet=[]
	testSet=[]
	trainfile_name=sys.argv[1];						
	testfile_name=sys.argv[2];
	type_classifier=sys.argv[3];
	k=sys.argv[4];
	
	
	if type_classifier == 'knn':
		knn_instance = knn();
		knn_instance.loadDataset(trainfile_name, testfile_name, trainingSet, testSet)
		#print 'Train set: ' + repr(len(trainingSet))
		#print 'Test set: ' + repr(len(testSet))
		# generate predictions
		predictions=[]
		conf_matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		#print "\n".join(item[0] for item in conf_matrix)
		
			
		for x in range(len(testSet)):
			neighbors = knn_instance.getNeighbors(trainingSet, testSet[x], k)
			result = knn_instance.getResponse(neighbors)
			predictions.append(result)
			#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][1]) + ',file:', repr(testSet[x][0]))
			if int(testSet[x][1]) ==  0 :
				if int(result) == 0:
					conf_matrix[0][0] += 1
				elif int(result) == 90:
					conf_matrix[0][1] += 1
				elif int(result) == 180:
					conf_matrix[0][2] += 1
				elif int(result) == 270:
					conf_matrix[0][3] += 1
			elif int(testSet[x][1]) ==  90 :
				if int(result) == 0:
					conf_matrix[1][0] += 1
				elif int(result) == 90:
					conf_matrix[1][1] += 1
				elif int(result) == 180:
					conf_matrix[1][2] += 1
				elif int(result) == 270:
					conf_matrix[1][3] += 1
			elif int(testSet[x][1]) ==  180 :
				if int(result) == 0:
					conf_matrix[2][0] += 1
				elif int(result) == 90:
					conf_matrix[2][1] += 1
				elif int(result) == 180:
					conf_matrix[2][2] += 1
				elif int(result) == 270:
					conf_matrix[2][3] += 1
			elif int(testSet[x][1]) ==  270 :
				if int(result) == 0:
					conf_matrix[3][0] += 1
				elif int(result) == 90:
					conf_matrix[3][1] += 1
				elif int(result) == 180:
					conf_matrix[3][2] += 1
				elif int(result) == 270:
					conf_matrix[3][3] += 1
			
			f = open('knn_output.txt','a')
			f.write(' '.join((testSet[x][0], ' ', result, "\n")))
		accuracy = knn_instance.getAccuracy(testSet, predictions)
		print('KNN - Accuracy: ' + repr(accuracy) + '%')
		
		print "****************CONFUSION MATRIX USING KNN CLASSIFIER***************", "\n"
		for row in conf_matrix:
			print(row)
	
	elif type_classifier == 'nnet':
		hidden_count = int(k)
		trainingSet=[]
		testSet=[]
		training_data=[]
		test_data=[]
		testlabels=[]
		with open(trainfile_name) as f:
				for line in f:
					line = line.split()  
					trainingSet.append(line)
		with open(testfile_name) as f:
				for line in f:
					line = line.split()  
					testSet.append(line)

		for xi in trainingSet:
			y=[0]*4
			if(xi[1]=='0'): y[0]=1
			elif(xi[1]=='90'): y[1]=1
			elif(xi[1]=='180'): y[2]=1
			elif(xi[1]=='270'): y[3]=1
			X=np.asarray(map(float, xi[2:]))/256
			Y=np.asarray(y,dtype=float)
			twoD_X = np.array(X)[np.newaxis]      
			twoD_Y = np.array(Y)[np.newaxis]
			training_data.append((twoD_X.T,twoD_Y.T))
		for xi in testSet:
			testlabels.append(xi[0])
			y=[0]*4
			if(xi[1]=='0'): y[0]=1
			elif(xi[1]=='90'): y[1]=1
			elif(xi[1]=='180'): y[2]=1
			elif(xi[1]=='270'): y[3]=1
			X=np.asarray(map(float, xi[2:]))/256
			Y=np.asarray(y,dtype=float)
			twoD_X = np.array(X)[np.newaxis]      
			twoD_Y = np.array(Y)[np.newaxis]
			test_data.append((twoD_X.T,twoD_Y.T))
		net = NNet([192,hidden_count,4])
		net.gradient_descent(training_data,0.1)
		print "testing..."
		accuracy = net.check(test_data,testlabels)*100.0/len(test_data)
		print "Classification accuracy - Neural Net :",accuracy,"%"
    
		
	elif type_classifier == 'best':
		trainingSet=[]
		testSet=[]
		training_data=[]
		test_data=[]
		testlabels=[]
		with open(trainfile_name) as f:
				for line in f:
					line = line.split()  
					trainingSet.append(line)
		with open(testfile_name) as f:
				for line in f:
					line = line.split()  
					testSet.append(line)

		for xi in trainingSet:
			y=[0]*4
			if(xi[1]=='0'): y[0]=1
			elif(xi[1]=='90'): y[1]=1
			elif(xi[1]=='180'): y[2]=1
			elif(xi[1]=='270'): y[3]=1
			X=np.asarray(map(float, xi[2:]))/256
			Y=np.asarray(y,dtype=float)
			twoD_X = np.array(X)[np.newaxis]      
			twoD_Y = np.array(Y)[np.newaxis]
			training_data.append((twoD_X.T,twoD_Y.T))
		for xi in testSet:
			testlabels.append(xi[0])
			y=[0]*4
			if(xi[1]=='0'): y[0]=1
			elif(xi[1]=='90'): y[1]=1
			elif(xi[1]=='180'): y[2]=1
			elif(xi[1]=='270'): y[3]=1
			X=np.asarray(map(float, xi[2:]))/256
			Y=np.asarray(y,dtype=float)
			twoD_X = np.array(X)[np.newaxis]      
			twoD_Y = np.array(Y)[np.newaxis]
			test_data.append((twoD_X.T,twoD_Y.T))
		net = NNet([192,10,4])
		net.gradient_descent(training_data,0.1)
		print "testing..."
		accuracy = net.check_best(test_data,testlabels)*100.0/len(test_data)
		print "Classification accuracy - Neural Net :",accuracy,"%"
	duration = default_timer() - start
	print "Duration:", duration/60, "minutes"

main()
