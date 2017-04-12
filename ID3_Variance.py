# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 20:59:12 2017

@author: Mohanakrishna
"""

import pandas as pd
import math
import Tree as tr
import copy
import random

def viCalculation(k1,k0):
    vi = 0
    if k1==0 or k0 ==0:
        return 0
    totalterms = k0+k1
    posterm = k1/totalterms
    negterm = k0/totalterms
    vi= posterm*negterm
    return vi

def gainMaxIndex(s,dataset1,attr1):
    gainList = list()
    for each in attr1:
        total = 0
        for value in [0,1]:
            rows = dataset1.loc[dataset1[each]==value]
            zeroClass = len(rows.loc[rows['Class']==0])
            oneClass = len(rows.loc[rows['Class']==1])
            viterm = (viCalculation(oneClass,zeroClass))
            #print(viterm)
            total+=(((zeroClass+oneClass)/len(dataset1))*viterm)
        gainList.append(s-total)
        
    return attr1[gainList.index(max(gainList))]

def ID3_Variance(examples,attribute,rootNode):
    
    k1 = len(examples.loc[examples['Class']==1])   
    k0 = len(examples.loc[examples['Class']==0])
   
    if (0 == k1):
        return '0'
    if (0 == k0):
        return '1'    
    if (len(attribute)==0):
        if k1>k0:
            return '1'
        else:
            return '0'
    else:
        totalVariance = viCalculation(len(examples.loc[examples['Class']==1]),
            len(examples.loc[examples['Class']==0]))
        #print(totalVariance)
        A =  gainMaxIndex(totalVariance,examples,attribute)
        #print(A)
        if rootNode == None:
            rootNode = Tree.addleftchild(A,None,k0,k1)
        attribute.remove(A)
        for each in [0,1]:
            examplesvi = examples.loc[examples[A]==each]
            if(each == 0):
                leftchild = Tree.addleftchild(None,rootNode,k0,k1)
            else:
                rightchild = Tree.addrightchild(None,rootNode,k0,k1)
            #print("examples len",len(examplesvi))
            if len(examplesvi) == 0:
                if k1>k0:
                    if each == 0:
                        Tree.setValue('1',leftchild,k0,k1)
                    else:
                        Tree.setValue('1',rightchild,k0,k1)
                else:
                    if each == 0:
                        Tree.setValue('0',leftchild,k0,k1)
                    else:
                        Tree.setValue('0',rightchild,k0,k1)
            else:

                if each == 0:
                    leftnode = ID3_Variance(examplesvi,list(attribute),leftchild)
                    Tree.setValue(leftnode,leftchild,k0,k1)
                else:
                    rightnode = ID3_Variance(examplesvi,list(attribute),rightchild)
                    Tree.setValue(rightnode,rightchild,k0,k1)
    return A

Tree = tr.BTree()   

def callVarinance(training_set,validation_set,test_set,construct_tree,L,K):
    dataset = pd.read_csv(training_set)
    validation = pd.read_csv(validation_set)
    test = pd.read_csv(test_set)
    #Column list
    columns = dataset.iloc[:,:-1]
    #classifiers
#    classifier = dataset.iloc[:,-1:]
    #Names of the attributes(list)
    attr_list = list(columns)
    ID3_Variance(dataset,attr_list,None)
    if(construct_tree == "YES"):
        Tree.printBTree()
#        print(TreeEntropy.getRoot())  
    else:
        print("You have selected 'No' to print tree argument, proceeding to pruning")
#        print(TreeEntropy.getRoot())  
    print("Accuracy before pruning by Variance Method:",calculateAccuracy(test,Tree))
    d_best = postPruning(L,K,validation,construct_tree)
    print("Accuracy after pruning by Variance Method:",calculateAccuracy(test,d_best))
        
def postPruning(L,K,validation_set,construct_tree):
    #Column list
#    columns = dataset.iloc[:,:-1]
    d_best = copy.deepcopy(Tree)
    L = L+1
    i = 1
    for i in range(1,L):
        d_dash = copy.deepcopy(Tree)
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
        Tree.printBTree()
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


    