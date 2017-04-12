# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 23:13:53 2017

@author: Mohanakrishna
"""


class Node:
    def __init__(self,value,idx,zeroes,ones):
        self.left=None
        self.right=None
        self.value=value
        self.idx = idx
        self.zeroes = zeroes
        self.ones =ones
        

class BTree:
    def __init__(self):
        self.root=None
        self.nodeidx = 0
        self.findReturn = None
        self.nonLeavesSet = list()
        
    def addleftchild(self,value,parent,zeroes,ones):
        if self.root==None:
            self.root = Node(value,self.nodeidx,zeroes,ones)
        else:
            self.node_traverse(parent,self.root)
            self.nodeidx+=1
            self.findReturn.left=Node(value,self.nodeidx,zeroes,ones)
        return self.nodeidx
    
    def getRoot(self):
        return self.root
    
    def get_left(self,node):
        return node.left

    def get_right(self,node):
        return node.right
        
    def setValue(self,value,idx,zeroes,ones):
        self.node_traverse(idx,self.root)
        self.findReturn.value = value
        self.findReturn.ones= ones
        self.findReturn.zeroes = zeroes
        
    def addrightchild(self,value,parent,zeroes,ones):
        if self.root==None:
            self.root = Node(value,self.nodeidx,zeroes,ones)
        else:
            self.node_traverse(parent,self.root)
            self.nodeidx+=1
            self.findReturn.right=Node(value,self.nodeidx,zeroes,ones)
        return self.nodeidx
            
    def node_traverse(self,idx,root):       
        if root.idx == idx:
            self.findReturn = root
        else:
            if root.left!=None:
                self.node_traverse(idx,root.left)
            if root.right!=None:
                self.node_traverse(idx,root.right)
                
    def numOfNonLeaves(self,root):
        if (self.get_left(root) == None and self.get_right(root) == None):
            return 0
        return 1 + self.numOfNonLeaves(self.get_left(root)) + self.numOfNonLeaves(self.get_right(root))
    
    def getNonleaves(self):
        self.nonLeavesSet = list()
        self._getNonleaves(self.root)
        return self.nonLeavesSet
        
    def _getNonleaves(self,rootNode):
        if(rootNode.left != None or rootNode.right != None):
            self.nonLeavesSet.append(rootNode)
        if rootNode.left != None:
            self._getNonleaves(rootNode.left)
        if rootNode.right != None:
            self._getNonleaves(rootNode.right)
        return

    def printBTree(self):
        self.findReturn = 0
        if(self.root != None):
            if(self.root.left == None and self.root.right==None):
                print(self.root.value)
            else:
                self.printTree(self.root)
                
    def printTree(self,root):
        if(root.left!=None):
            pStr = ""
            for each in range(0,self.findReturn):
                pStr=pStr+"| "
            
            if(root.left!=None and root.left.left==None and root.left.right==None):
                str1 = pStr+root.value+" = 0 : "+root.left.value
                print(str1)
            else:
                str1 = pStr+root.value+" = 0 : "
                print(str1)
                self.findReturn=self.findReturn+1
                self.printTree(root.left)
                self.findReturn=self.findReturn - 1
            
        if(root.right!=None):
            pStr=""
            for each in range(0,self.findReturn):
                pStr=pStr+"| "
                
            if(root.right!=None and root.right.left==None and root.right.right==None):
                str1 = pStr+root.value+" = 1 : "+root.right.value
                print(str1)
            else:
                str1 = pStr+root.value+" = 1 : "
                print(str1)
                self.findReturn+= 1
                self.printTree(root.right)
                self.findReturn-= 1
    
    def traverse(self,root,X):
        if(root.left==None and root.right==None):
            return int(root.value)
        elif(X[root.value]==0):            
            return int(self.traverse(root.left,X))       
        else:
            return int(self.traverse(root.right,X))
                    
#tree = BTree()
#root = tree.addleftchild("wesley",None)
#honor = tree.addleftchild("honor",root)
#tree.addrightchild("0",root)
#barclay = tree.addleftchild("barclay",honor)
#tree.addleftchild("1",barclay)
#tree.addrightchild("0",barclay)
#tea = tree.addrightchild("tea",honor)
#tree.addrightchild("1",tea)
#tree.addleftchild("0",tea)
#tree.printBTree()     
            
        
        