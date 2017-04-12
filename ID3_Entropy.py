# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 09:52:55 2017

@author: Mohanakrishna
"""
import pandas as pd
import math
import Tree as tr
import random
import copy

def entropyCalculation(pos,neg):
    entropy = 0
    if(pos==neg):
        entropy = 1
    else:
        posterm = pos/(pos+neg)
        negterm = neg/(pos+neg)
        if(posterm==0):
            logpos = 0
        else:
            logpos = math.log(posterm,2)
        if(negterm==0):
            logneg = 0
        else:
            logneg = math.log(negterm,2)
        entropy = ((-1)*posterm*logpos) - (negterm*logneg)
    return entropy

def informationGainMaxIndex(s,dataset1,attr1):
    infoGainList = list()
    for each in attr1:
        total = 0
        for value in [0,1]:
            rows = dataset1.loc[dataset1[each]==value]
            zeroClass = len(rows.loc[rows['Class']==0])
            oneClass = len(rows.loc[rows['Class']==1])
            entropy = (entropyCalculation(oneClass,zeroClass))
            total+=(((zeroClass+oneClass)/len(dataset1))*entropy)
        infoGainList.append(s-total)
        
    return attr1[infoGainList.index(max(infoGainList))]

TreeEntropy = tr.BTree()   

def ID3_Entropy(examples,attribute,rootNode):
    
#    if counter > 0:
#        counter -=1
    totalones = len(examples.loc[examples['Class']==1])   
    totalzeros = len(examples.loc[examples['Class']==0])
   
    if (0 == totalones):
        return '0'
    if (0 == totalzeros):
        return '1'    
    if (len(attribute)==0):
        if totalones>totalzeros:
            return '1'
        else:
            return '0'
    else:
        totalEntropy = entropyCalculation(totalones,totalzeros)
        A =  informationGainMaxIndex(totalEntropy,examples,attribute)
        #print(A)
        if rootNode == None:
            rootNode = TreeEntropy.addleftchild(A,None,totalzeros,totalones)
        attribute.remove(A)
        for each in [0,1]:
            examplesvi = examples.loc[examples[A]==each]
            if(each == 0):
                leftchild = TreeEntropy.addleftchild(None,rootNode,totalzeros,totalones)
            else:
                rightchild = TreeEntropy.addrightchild(None,rootNode,totalzeros,totalones)
            #print("examples len",len(examplesvi))
            if len(examplesvi) == 0:
                if totalones>totalzeros:
                    if each == 0:
                        TreeEntropy.setValue('1',leftchild,totalzeros,totalones)
                    else:
                        TreeEntropy.setValue('1',rightchild,totalzeros,totalones)
                else:
                    if each == 0:
                        TreeEntropy.setValue('0',leftchild,totalzeros,totalones)
                    else:
                        TreeEntropy.setValue('0',rightchild,totalzeros,totalones)
            else:

                if each == 0:
                    leftnode = ID3_Entropy(examplesvi,list(attribute),leftchild)
                    TreeEntropy.setValue(leftnode,leftchild,totalzeros,totalones)
                else:
                    rightnode = ID3_Entropy(examplesvi,list(attribute),rightchild)
                    TreeEntropy.setValue(rightnode,rightchild,totalzeros,totalones)
    return A
                    
def callEntropy(training_set,validation_set,test_set,construct_tree,L,K):
    dataset = pd.read_csv(training_set)
    validation = pd.read_csv(validation_set)
    test = pd.read_csv(test_set)
    #Column list
    columns = dataset.iloc[:,:-1]
    #classifiers
#    classifier = dataset.iloc[:,-1:]
    #Names of the attributes(list)
    attr_list = list(columns)
    ID3_Entropy(dataset,attr_list,None)
    if(construct_tree == "YES"):
        TreeEntropy.printBTree()
#        print(TreeEntropy.getRoot())  
    else:
        print("You have selected 'No' to print tree argument, proceeding to pruning")
#        print(TreeEntropy.getRoot())  
    print("Accuracy before pruning by Entropy Method:",calculateAccuracy(test,TreeEntropy))
    d_best = postPruning(L,K,validation,construct_tree)
    print("Accuracy after pruning by Entropy Method:",calculateAccuracy(test,d_best))
      
def postPruning(L,K,validation_set,construct_tree):
    #Column list
#    columns = dataset.iloc[:,:-1]
    d_best = copy.deepcopy(TreeEntropy)
    L = L+1
    i = 1
    for i in range(1,L):
        d_dash = copy.deepcopy(TreeEntropy)
        m = (random.randint(1,K))+1
        for j in range(1,m):
            n = d_dash.numOfNonLeaves(d_dash.getRoot()) 
            if(n<=0):
                break
#            print(n)
            nodeList = d_dash.getNonleaves()
            
            p = random.randint(1,n)
            pNode = nodeList[p-1]
            pNode.left = None
            pNode.right = None
            if(pNode.ones > pNode.zeroes):
                pNode.value = '1'
            else:
                pNode.value = '0'

        if (calculateAccuracy(validation_set,d_dash)>calculateAccuracy(validation_set,d_best)):
            d_best = copy.deepcopy(d_dash)
    if construct_tree == 'YES':
        TreeEntropy.printBTree()
    return d_best

def calculateAccuracy(dataset,TreeEntropy):
    X = dataset.iloc[:,:-1]
    root = TreeEntropy.getRoot()
    accList = list()
    accCounter = 0
    for index, row in X.iterrows():
        target_value = TreeEntropy.traverse(root,row)
        accList.append(target_value)
        if(target_value == dataset['Class'][index]):
            accCounter+=1
    return (accCounter/len(dataset))*100

    