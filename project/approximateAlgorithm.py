from Tree import Tree
import random

class approximateAlgorithm:
    def __init__(self):
        self.capacity = 0
        self.nodes = []
	self.totDist = 0

    """
    # This function is to make the class more modular.
    # This function doesn't need to be tested because it can be moved staright away to replac self.binAndPackSolution() under function solve()
    """
    def binAndPackSolution(self, test = False):
	# Finding node with children more than 0. The root is the grand-parent!
	# this makes sense because our tree representation only have 1 child in each node.
        nodeWithChildren = [x for x in self.myTree.root.children if len(x.children)>0]

        while len(nodeWithChildren)>0:
	    if test:
		print '\n### Printing the tree before algorithm runs. ###'
		# Print current tree
		for node in self.myTree.tree:
			if len(node.children)>0:
				print '\n# Node name: '+str(node.name)
				if node.parent is None:
					print '# Node parent: None'
				else:
					print '# Node parent: '+str(node.parent.name)
				print '# Node children: '+','.join([x.name for x in node.children])
		print '### Finish loop testing ###'

	    # Get random node.
            randomNode = self.getRandomNode()

            if(randomNode == self.myTree.root):
                continue
          
            self.prepareBinPack(randomNode)
            
            nodeWithChildren = [x for x in self.myTree.root.children if len(x.children)>0]

        # Adding the route's name for printing solution
        for child in self.myTree.root.children:
            child.route.insert(0, child.name)
            child.route.insert(0,self.myTree.root.name)
	    child.totalDistance += self.myTree.getDistanceFromRoot(child)

    """
    # Param:
    # parent is the parentNode.
    # sortedChildren is the list of children sorted by capacity.

    # Basic idea is if it's a leaf:
    1. Get the capacity of the leaf
    2. Delete the leaf from the tree
    
    # Otherwise, if the node is not the leaf, we sort the children of the child by capacity and do recursive
    function until the node becomes a leaf and then we use the bin and pack solution.
    """
    def prepareBinPack(self, parent):
        # Sort the children based on their capacity
        sortedChildren = sorted(parent.children, key=lambda x: x.capacity) 
        for child in sortedChildren:
            if len(child.children) == 0:
                self.binPackCondition(parent, child, sortedChildren)
            else:
                self.prepareBinPack(child) # this recursive will make the child a leaf.
                if child.isLeaf():
                    self.binPackCondition(parent, child, sortedChildren)

    """
    # Param:
    # parentNode: Parent node of child node.

    # This function is to check whether the capacity combined between
    parent and its children exceeds the capacity of the vehicle.

    # If it isn't, combine the child node to parent node.
    If this happend, we need to:
    1. delete the node since it'll be combined with parent node.
    2. Get the info of this node! E.g route, distance and
    save those at parent node.
    3. delete the node from the tree as well, as to prevent index error from
    getting randomNode from the tree.

    # If it exceeds the capacity, change the parent of the node!
    If this happens, we need to also append this node as:
    1. Grandparent's child which is done in class Node.
    2. Add this node to for the node needs to be checked in sortedChildren.

    # Test: Returned string must be not exceeding parent capacity or exceeding parent capacity and changing parent.
    Other than that, "Not changing parent, because parent is root" and there will be a check the name of the root/depot.
    """
    def binPackCondition(self, parentNode, childNode, childrenList):
        if parentNode.capacity + childNode.capacity <= self.capacity:
            # these 2 lines are for #2
            childNode.route.insert(0,childNode.name)
            parentNode.setRoute(childNode.route)
            
            parentNode.totalDistance += childNode.totalDistance
            childNode.removeNode() #1
            self.myTree.nodes.remove(childNode) #3
            parentNode.capacity += childNode.capacity
	
	    return "Not exceeding maximum capacity"
        else:
            # Only change parent if it's grandparent of root!
            if childNode.parent != self.myTree.root:
                childNode.changeParent() #1
                childrenList.append(childNode) #2
	    	return "Exceeding maximum capacity and changing parent"
	    return "Not changing parent, because parent is root. Check:"+childNode.parent.name

    """
    # Find random node in the tree
    # Unit test: Whether the return is of type Node.
    """
    def getRandomNode(self):
        treeLength = len(self.myTree.nodes)
        index = random.randint(0, treeLength-1)
        return self.myTree.nodes[index]

    """
    # Preparing string representation to output file.
    """
    def printSol(self):
	self.totDist = 0
	returnStr = ""
	returnStr += " ### Approximate Algorithm ### \n"

        # Actual printing solution.
        for i in range(0,len(self.myTree.root.children)):
	    returnStr += "Vehicle "+str(i+1)+":"+' -> '.join(self.myTree.root.children[i].route) +". Capacity: "+str(self.myTree.root.children[i].capacity)+"."
            returnStr += "Distance for this route: "+str(self.myTree.root.children[i].totalDistance)+"\n"   
	    self.totDist += self.myTree.root.children[i].totalDistance
	returnStr += "Total Distance: "+str(self.totDist)+"\n"  
	returnStr += " ### End of Approximate Algorithm ### "	
	return returnStr

    """
    # This function is needed to build routeList, where the list later is used to build the GUI.
    # routeList is a list of the route of the children of the root.
    # Test : Whether the return routeList are of type list of list. Each individual list are of type integer.
    """
    def prepareGUI(self):        
	routeList = []
	for i in self.myTree.root.children:
		routeList.append(i.route)
	return routeList

    """
    # This is the first method will be called to initate the execution of solution in the class.
    # Param:
    # readFile = Pass an object of class reading_file.py

    # This function will return the routeList which is the list of string.
    """
    def solve(self, readFile):
        self.capacity = readFile.capacity
        self.nodes = readFile.allNodeList        

        self.myTree = Tree(self.nodes)
        self.myTree.root = self.myTree.findDepot()
        self.myTree.makeTree()

        self.binAndPackSolution() 

	return self.prepareGUI()

if __name__ == '__main__':
	print "******** Testing for class approximate algorithm ********"

	print '### Reading file from input called test.vrp using a class called Read_File ###'
	print '# Executing rf= Read_File("./input/test.vrp") #'
	from reading_file import Read_File
	rf = Read_File("./input/test.vrp")

	print '\n'	

	print '### initializing class approximateAlgorithm() ###'
	print '# Executing: al = approximateAlgorithm() #'
	al = approximateAlgorithm()

	print '\n'

	print '### Initializing class Tree with input from file test.vrp ###'
	print '# Executing: myTree = Tree(rf.allNodeList). This will make a tree and save it in a variable myTree #'
	al.myTree = Tree(rf.allNodeList)
	print '# Executing: myTree.isRootExist(). This will check if there is a root in the tree. #'
	print '- Expected: False. \n' + '- Output: '+str(al.myTree.isRootExist())

	print '\n'

	print '### Assigning root to a tree and make the tree ###'
	print '# Executing: myTree.root = myTree.findDepot() and myTree.makeTree(). #'
	al.myTree.root = al.myTree.findDepot()
	al.myTree.makeTree()
	print '# Exeucting myTree.tree to see all the nodes in the tree #'
	print '- Expected: All the nodes from 1-10. Order might change.'
	print '- Output: '+','.join([x.name for x in al.myTree.tree])

	print '\n'


	print '### Checking binAndPackCondition(parentNode, childNode, childrenList) ###'
	print '# This function is used to either combined the parent nodes to its children when the capacity is within the limit or to change the parent of the child''s node when the capacity of the two nodes are exceeding the maximum capacity #'
	print '# chidrenList is a list of children of parentNode. parentNode and childNode are of type Node #'
	print '# For example of this test, we are going to take an example of a node #'
	print '#- Checking a node. -#'
	checkNode = al.myTree.tree[len(al.myTree.tree)-2]
	print 'Node name: '+str(checkNode.name)+'. Node parent: '+str(checkNode.parent.name)+'. Node children: '+','.join([x.name for x in checkNode.children])

	print '## Set maximum capacity into 2 ##'
	al.capacity = 2
	print '## Check maximum capacity: '+str(al.capacity)+' ##'
	print '# Executing: al.binPackCondition(checkNode, checkNode.children[0], checkNode.children)#'
	print '- Check: Capacity of child:'+str(checkNode.children[0].capacity)+'. And capacity of parent:'+str(checkNode.capacity)		
	print '- Output: '+al.binPackCondition(checkNode, checkNode.children[0], checkNode.children)
	print '- Expected: Not exceeding maximum capacity. Means that the node will be packed.'

	print '# Test if the current node that only has 1 child and has been packed still have a child or not. #'
	print '- Expected: no child at all since it has been packed together.'
	print '- (Executing: checkNode.children) Output: '+str(checkNode.children)

	print '# Test if the current node capacity and its chidren capacity is more than the maximum capacity #'
	checkNodeParent = checkNode.parent
	print 'Current node name: '+str(checkNode.name)+'. Node parent: '+str(checkNode.parent.name)+'. Node children: '+str(checkNode.children)+'. Node capacity: '+str(checkNode.capacity)
	print '# Using the same node and its parent. Executing: al.binPackCondition(checkNode.parent, checkNode.parent.children[0], checkNode.parent.children) #'
	print '- Output: '+str(al.binPackCondition(checkNode.parent, checkNode.parent.children[0], checkNode.parent.children))
	print '- Expected: Exceeding maximum capacity and changing parent'

	print '# Check the if the current node parent has been changed. #'
	print '- Parent before changed: '+str(checkNodeParent.name)+'. Parent after changed: '+str(checkNode.parent.name)
	print '- Expected: For the parents of both above to be different'


	print '\n'

	print '### Check function prepareBinPack(parent) with parent as type Node ###'
	print '# This function will be calling binPackCondition() function and hence the input for binPackCondition() is always maintained #'
	print '# Let''s try to do this with the child of root #'
	print '# Executing checkNode = al.myTree.tree[1] #'
	checkNode = al.myTree.tree[1]
	print 'Node name: '+str(checkNode.name)+'. Node parent: '+str(checkNode.parent.name)+'. Node children: '+','.join([x.name for x in checkNode.children])
	print '# Check the root BEFORE function binPackCondition called. #'
	rootNode = al.myTree.root
	print 'Root node: name: '+str(rootNode.name)+' Children: '+','.join([x.name for x in rootNode.children])
	al.prepareBinPack(checkNode)
	print '# Check the root AFTER function binPackCondition called. #'
	print 'Root node: name: '+str(rootNode.name)+' Children: '+','.join([x.name for x in rootNode.children])
	print '- Expected: There would be additional child in root since the capacity of the first child and the second child cannot be combined or exceeding the maximum capacity.'
	print '- Output: root node first child capacity: Name: '+str(rootNode.children[0].name)+'. Capacity: '+str(rootNode.children[0].capacity)
	print '- Output: root node second child capacity: Name: '+str(rootNode.children[1].name)+'. Capacity: '+str(rootNode.children[1].capacity)
	print '- Expected: Capacity for both of the output is at most 2 since the maximum capacity is set to 2 for the example before'

	print '\n'

	print '### Now checking integration of all the functions within this class by using functin solve(). ###'
	print '# Executing: solve(rf) with rf is the read_file object #'
	print '# It shold return the list of route made by this algorithm. (List of list, oter list for vehicles, inner list for route) #'
	rf = Read_File("./input/test.vrp")
	al = approximateAlgorithm()
	print al.solve(rf)

	print "******** End testing for class approximate algorithm ********"

