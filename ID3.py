# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 11:32:10 2017

@author: Mohanakrishna
"""

import ID3_Entropy as ent
import ID3_Variance as var
import sys

L = int(sys.argv[1])
K = int(sys.argv[2])
training_set = sys.argv[3]
validation_set = sys.argv[4]
test_set = sys.argv[5]
construct_tree = sys.argv[6]
construct_tree = str(construct_tree).upper()

#print(L,K,training_set,validation_set,test_set,construct_tree)
if(construct_tree=='YES'):
    print('Tree created by Entropy Method:')
    ent.callEntropy(training_set,validation_set,test_set,construct_tree,L,K)
    
    print('Tree created by Variance Method:')
    var.callVarinance(training_set,validation_set,test_set,construct_tree,L,K)
elif(construct_tree=='NO'):
    print("Entropy Method:")
    ent.callEntropy(training_set,validation_set,test_set,construct_tree,L,K)
    print("Variance Method:")
    var.callVarinance(training_set,validation_set,test_set,construct_tree,L,K)
else:
    print("Please enter either 'yes' or 'no' to print the tree")
    



    
    