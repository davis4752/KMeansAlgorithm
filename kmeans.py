import argparse
import random
import math
import copy
#Author: Adam Davis
#Date: 02/25/2019
#Class: CSE 5243
#title: Programming Assingment 3
#Discription: This program is an implementation of k-means algorithm to do clustering. This uses
#			  uses a multi feature datapoints by a matrix
#command Line: python kmeans.py -database_file database.txt -k 10 -max_iters 20 -eps .1 -output_file output.txt


parser = argparse.ArgumentParser() #create command line Parser

#add Command line arguments
parser.add_argument('-database_file')  
parser.add_argument('-k')
parser.add_argument('-max_iters')
parser.add_argument('-eps')
parser.add_argument('-output_file')

args = parser.parse_args() # Send all arguments to args

#Put the command line argument file to individual objects
Database_file = str(args.database_file)   #train_data.txt
kClusters = int(args.k)                   #number of clusers
Max_iterations = int(args.max_iters)      #max iterations
MinDist = float(args.eps)                 #min distance to stop
output_file = str(args.output_file)       #file to print output


def read_data():                  #read in data from database
	fp = open(Database_file, 'r') #open database.txt
	database = []				  #initialize empty list
	while True:                   #reads in the database line by line spliting values
		hold  = fp.readline()
		if not hold: break
		else: database.append(map(float, hold.split()))
		
	return database #return list[] containing the database
	
def getCentroids(database):    #Get the starting centroids

	rowCandidates = []         #initlialize list of row candidates
	centroids = []             #hold the value of the feature
	for x in range(kClusters): #create k number of clusters
		while(True): 
			row = random.randint(0,len(database) - 2)
			if row not in rowCandidates:               #if not already used
				rowCandidates.append(row)
				centroids.append(database[row])
				break	
	return centroids #return starting centroids

def Euclideandistance(datapoint,centroid): #calculate the distance between two points
	distance = 0;
	for x in range(len(datapoint)):   #add the difference between each point squared
		distance += math.pow(datapoint[x] - centroid[x], 2)
	return math.sqrt(distance)        #return the sqrt of the sum
	
	
def seperate(database, centroids):  #seperate the data points by their nearest centroid

	clusters = []               #initilized cluster list
	for x in range(kClusters): #create list to fit each cluster
		clusters.append([x])       
		
	for n in range(len(database) - 1): #Go through each row in the database
		closeClust = 0                 #initial distance
		closeDist = Euclideandistance(database[n], centroids[0])
		
		for  x in range(1, kClusters):        #rotate through each k cluseter
			TestDist = Euclideandistance(database[n],centroids[x])
			if(TestDist < closeDist):
				closeClust = x
				closeDist = TestDist
				
		clusters[closeClust].append(n)
		
	return clusters   #return the group of clusters
	
def updateCentroids(database, clusters, centroids): #update centroids to the mean of the valuse that belong to it
	for x in range(kClusters):   #Goes through each cluster
		for n in range(len(database[0])): #goes through each feature
			meanValue = 0;
			for z in range(1, len(clusters[x])): #goes through each value in the cluster
			 	meanValue += database[clusters[x][z]][n]

			centroids[x][n] = (meanValue / len(clusters[x])) #replaces the value with the mean 
	return centroids #return the new centroids
	
def Check_E_distance(oldcentroids, newcentroids): #calculate the distance change from old to new
	maxDistance = 0
	
	for x in range(len(oldcentroids)): #rotate through each centroid 
		DistanceCheck = 0
		DistanceCheck = Euclideandistance(oldcentroids[x],newcentroids[x])
		if(DistanceCheck > maxDistance):
			maxDistance = DistanceCheck
		

	return maxDistance #return the max change from the old to new centroids
			 	
def printOutput(clusters):         #print the output to output.txt
		f = open(output_file, "w") #open output file 
		for x in range(kClusters):
			f.write(`x`+ ":")
			for n in range(len(clusters[x])):
				f.write(" " + `clusters[x][n]`)
			f.write("\n")
		f.close()
	


def genKmeans(database): #goes through each step of k means
	
	#initialize k centroids
	centroids = getCentroids(database)
	
	#Repeat until convergence w.r.t.e or n interations
	for x in range(Max_iterations):
		clusters = seperate(database, centroids)
		oldcentroids = copy.deepcopy(centroids)
		
		#UpdateCentroids
		#assign each data point to each of the k clusters based on Euclidean distance
		updateCentroids(database, clusters, centroids)

		distance = Check_E_distance(oldcentroids, centroids)
		
		#if no clusters pass e the loop ends
		if(distance < MinDist):
			break
		
		
	#output the k clusters
	printOutput(clusters)


def main():

	database = read_data() #create a usable form for the database
	genKmeans(database)    #kmeans algorithm
	
main()
