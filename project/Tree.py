import random
import math

class Tree:

    """
    # Param:
    # nodes = list of nodes e.g Nodes[]
    # Variables:
    # self.nodes will be the list that is edited (removed/added)
    # self.actualNodes is the actual list of node. This should not be changed.
    # self.distanceList is the list of distance from one node to another.
    """
    def __init__(self, nodes):
        self.nodes = nodes
        self.actualNodes = nodes[:]
        self.tree = []
        self.root = None
        self.distanceList = []

    def isRootExist(self):
        return self.root!=None

    """
    # Get index from node in the list.
    # Test: return the indx of the node if found, other return -1.
    """
    def getIndexFromNode(self,node):
        i=0
        for nodeCheck in self.actualNodes:
            if(node == nodeCheck):
                return i
            i += 1
	return -1

    """
    # Get the distance from root to any nodes.
    # Test: return the distance in the list, otherwise return 0
    """
    def getDistanceFromRoot(self,node):
        distanceListFromRoot = self.distanceList[0]
        for i in distanceListFromRoot:
            if i[0] == node:
                return i[1]
	return 0

    """
    # Get the disance from a node to other node.
    # Test: return the distance between these two node, otherwise return 0
    """
    def getDistanceFromToNode(self, fromNode, toNode):
        distanceList = self.distanceList[self.getIndexFromNode(fromNode)] 	
        for i in distanceList:
            if i[0] == toNode:
                return i[1]
	return 0

    """
    # Function is to calculate the distance of each other nodes.
    # E.g: [ [0,2,3], [6,0,8], [10,11,0]]
    # In this case, the first list of list [0,2,3] means the distance from root to other nodes.
    If it's 0, it means the direction is going to the node itself.
    """
    def calculateDistance(self):
        for i in range(0,len(self.nodes)):
            self.distanceList.append([])
            for j in range(0,len(self.nodes)):
                if i==j:
                    self.distanceList[i].append([self.nodes[j],0])
                else:
                    self.distanceList[i].append([self.nodes[j],self.euclid(self.nodes[i],self.nodes[j])])

    """
    # Function to calculate the distance in euclid 2D.
    """
    def euclid(self, aNode, bNode):
        x1, y1 = aNode.x, aNode.y
        x2, y2 = bNode.x, bNode.y

        return int(round(math.sqrt(((x1 - x2) ** 2) + (((y1 - y2) ** 2)))))

    """
    # This function is needed to sort the self.distance by its distance.
    """
    def getKey(self,item):
        return item[1]

    """
    # Finding depot. Usually depot will have capacity of 0.
    """
    def findDepot(self):
        for node in self.actualNodes:
            if(node.capacity == 0):
                return node

    """
    # Creating tree from the root.
    # Adding to self.tree for every node allocated in the tree.
    # Start from the root, we want to assign children and keep going until all the nodes assigned.
    """
    def makeTree(self):
        self.calculateDistance()
        currentNode = self.root
        while(len(self.nodes) != len(self.tree)):
            # If root not exists
            if (self.isRootExist):
                self.root = self.findDepot()
                self.tree.append(self.root)
                currentNode = self.root
            justAdded = []
            justAdded = self.assignToChildren(currentNode)
            self.makeTreeFromLeaves(justAdded)

    """
    # This method used to assign child(ren) to a node.
    # Will return the list of child that just added to the tree so we could continue from there before doing any recursive to other children.
    """
    def assignToChildren(self, currentNode):
        # Get distance from currentNode
        distanceFromCurNode = self.distanceList[self.getIndexFromNode(currentNode)]
        
        # Get the numOfChild nodes ranked by distance
        sortedDistance = sorted(distanceFromCurNode, key=self.getKey)
        
        justAdded = []
        if(len(sortedDistance)==0):
            return justAdded

        # the idea is to make a tree with 1 child each
        # The child always is the shortest distance
        numOfChild = 1

        availableNodes = self.getAvailableNodes()
	if len(availableNodes) > 0:
		for i in sortedDistance:
		    if i[0] in availableNodes and len(currentNode.children) < numOfChild:
		        currentNode.addChild(i[0])
		        currentNode.totalDistance = i[1]
		        justAdded.append(i[0])
		        self.tree.append(i[0])
                
        return justAdded

    """
    # Continue making tree from leaves.
    # This is the recursive action to keep going until all the nodes allocated.
    """
    def makeTreeFromLeaves(self, leaves):
        for currentNode in leaves:
            if(currentNode==None):
                break
            justAdded = self.assignToChildren(currentNode)
            self.makeTreeFromLeaves(justAdded)

    """
    # Function is to get all the available nodes which is the un allocated nodes.
    # Will return the list of nodes.
    """
    def getAvailableNodes(self):
        availableNodes = []
        for node in self.actualNodes:
            if not node in self.tree:
                availableNodes.append(node)
        return availableNodes


    def printAllDistance(self):
	distList = []
	for i in self.distanceList:
		tmpList = []
		for j in i:
			tmpList.append (j[0].name+","+str(j[1]))
		distList.append(tmpList)

	return distList

    def printNodesName(self,alist):
        astr = "Children: "
        for i in alist:
            astr += i.name+" "
        if astr == "Children: ":
            astr += "None"
        print astr

if __name__ == '__main__':
	from Node import Node
	print "******** Testing for class Tree and its integration with class Node ********"
	
	# Making list of nodes
	print '### Making list of nodes, as the requirement to initialize the class we need to have list of nodes ###'
	print '''# Input for nodeList:
nodesList = []
a = Node("1",1, 0)
nodesList.append(a)
b = Node("2",2, 2)
nodesList.append(b)
c = Node("3",3, 3)
nodesList.append(c)
d = Node("4",4, 4)
nodesList.append(d)
e = Node("5",5, 5)
nodesList.append(e)
f = Node("6",0, 1)
nodesList.append(f)'''
	nodesList = []
	a = Node("1",1, 0)
	nodesList.append(a)
	b = Node("2",2, 2)
	nodesList.append(b)
	c = Node("3",3, 3)
	nodesList.append(c)
	d = Node("4",4, 4)
	nodesList.append(d)
	e = Node("5",5, 5)
	nodesList.append(e)
	f = Node("6",0, 1)
	nodesList.append(f)

	print '\n'

	print '### Creating a tree ###'
	print '# Input: Tree(nodesList) #'	
	myTree = Tree(nodesList)
	
	# Check if the root exist in the tree
	print '### Checking if root has been assigned in this tree ###'
	print '# False if there is not any root, True otherwise #'
	print '- Output: '+str(myTree.isRootExist())+'. Expected: False'
	
	print '\n'
	
	# Check functio findDepot to find root.
	print '### Testing function findDepot() to find a root of the tree ###'
	print '# Return a type of node #'
	myTree.root = myTree.findDepot()
	print '- Output: '+str(myTree.root.name)+'. Expected: 1'

	print '\n'
	
	# Check root in the tree after find a depot to assign as a root
	print '### Checking if root has been assigned in this tree ###'
	print '# False if there is not any root, True otherwise #'
	print '- Output: '+str(myTree.isRootExist())+'. Expected: True'

	print '\n'

	# Check getIndexFromNode(Node)
	print '### Check fnction getIndexFromNode(Node) with Node as an object of class Node ###'
	print '# Return index of the node otherwise return -1. #'
	print '# Executing: myTree.getIndexFromNode(f) #'
	
	index = myTree.getIndexFromNode(f)
	print '- Output: '+str(index)+'. Expected: 5'

	print '# Check to find node that is not in the tree #'
	print '# Executing: myTree.getIndexFromNode(Node("9",1,2)) #'
	index = myTree.getIndexFromNode(Node("9",1,2))
	print '- Output: '+str(index)+'. Expected: -1'

	print '\n'

	# Checking function calculateDistance() to calculate distance from one node to all the other nodes
	myTree.calculateDistance()
	print '### Checking function calculateDistance() ###'
	print '# Printing the distance from root. It should be of type list of list #'
	print '# Expected: First element in the list of list to be of type Node and second element to be of type int #'
	print '- Output: '+str(myTree.distanceList[0])

	# Checking function getDistanceFromRoot and getDistanceFromToNode
	print '### Checking function getDistanceFromRoot ###'
	print '# Printing the distance from root to a specific node. #'
	print '# Expected: Return a value of integer #'
	print '# Executing: myTree.getDistanceFromRoot(b) #'
	print '- Output: '+str(myTree.getDistanceFromRoot(b))+'. Expected: 2'

	print '### Checking function getDistanceFromToNode ###'
	print '# Executing: myTree.getDistanceFromToNode(b,c) #'
	print '- Output: '+str(myTree.getDistanceFromToNode(b,c))+'. Expected: 1'
	
	# Checking function getAvailableNodes()
	print '# Expected: Value of type list. Should be the list of nodes that has not been assigned to a tree. #'
	print '# Executing: print myTree.getAvailableNodes() #'
	print '- Output: '+','.join([x.name for x in myTree.getAvailableNodes()])
	print '- Expected: 1,2,3,4,5,6.\nAll the name of the nodes since none is in the tree now.'

	print '# Executing: print myTree.tree #'
	print '- Output: '+str(myTree.tree)
	print '- Expected: []'


	print '\n'
	
	print '# Executing: myTree.makeTree() #'
	print '# Making a tree. Now, the tree should be filled up with some nodes #'
	myTree.makeTree()
	print '# Done executing makeTree() now check by printing the myTree.tree #'
	print '- Output: '+str(','.join([x.name for x in myTree.tree]))
	print '- Expected: 1,6,2,3,4,5.\nAll the nodes from 1-6 basically. The order might not be the same.'

	print '\n'

	# Checking function assignToChildren()
	print '### Checking function assignToChildren() ###'
	print '# Executing: myTree.assignToChildren(e) #'
	print '- Output: '+str(myTree.assignToChildren(e))
	print '- Expected: [] since all the nodes have been assigned'

	print '\n'

	print '# Adding new node #'
	print '# Executing: g = Node("7",99,99) #'
	g = Node("7",99,99)
	myTree.nodes.append(g)
	myTree.actualNodes.append(g)
	myTree.calculateDistance()
	print '# Executing: myTree.assignToChildren(e) #'
	print '- Output: '+str(','.join([x.name for x in myTree.assignToChildren(e)]))
	print '- Expected: 7'	

	print '\n'
