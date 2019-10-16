class Node:

    def __init__(self,name, x, y):
        self.parent = None
        self.children = []
        self.x = int(x)
        self.y = int(y)
        self.capacity = 0
        self.name = name
        self.route = []
        self.totalDistance = 0

    """
    # This function is to check if the node is a leaf or not.
    # Test : True if leaf, false if not.
    """
    def isLeaf(self):
        if(len(self.children) == 0):
            return True
        return False

    """
    # This function is to add child(ren).
    # Test : true if the child is a node, false if child is not a node.
    """
    def addChild(self, child):
	try:
	        self.children.append(child)
	        child.parent = self
	        return True
	except:
		return False

    """ 
    # This function is to set the capacity of each node/customer.
    """
    def setCapacity(self, capacity):
        self.capacity = capacity

    """
    # This function is to set the route. Route in this case must be of type list and integer.
    # Test: True if route is list, False otherwise
    """
    def setRoute(self,route):
	if(isinstance(route,list)):
	        if len(self.route)==0:
	            self.route.extend(route)
	        else:
	            route.extend(self.route)
		    self.route = route
		return True
	else:
		return False

    """
    # Changing parent to its grandparent.
    # No testing needed as the condition must be met before calling this function.
    """
    def changeParent(self):
        # Change parent to the grandparent
        parentNode = self.parent
        newParent = parentNode.parent
        self.parent = newParent

        # remove the previous parent.
        parentNode.children.remove(self)
        # Add the child of the grandparent!
        newParent.children.append(self)

    """
    # Remove the node only if there is no children for this node
    # Test: ValueError is raised when children still exist.
    """
    def removeNode(self):
        # Can only remove node if it doesn't have any children
        if len(self.children) == 0:
            self.parent.children.remove(self)
            self.parent = None
	    return True
        else:
            raise ValueError('Unsuccessful! Children still exist!')

    def printNode(self):
	try:
		childrenName = [x.name for x in self.children]
		print "This node's name:",self.name
		print "Parent:",self.parent.name
		print "Children:", childrenName
		print "Capacity:",self.capacity
		#print "This node's memory:",self
		return True
	except:
		return False

    def printNodeAsATree(self,level=0):
        print '\t' * level + repr(self.name)
        for child in self.children:
            child.printNodeAsATree(level+1)


if __name__ == '__main__':
	# This line of codes below for purpose of testing
	print "******** Testing for class Node ********"

	# We will make 2 nodes. First is the root, second is the child of the root
	print "### First test the creation of class: ###\n"
	print '# input: Node("First Node", 1, 3) with first parameter as the nodes name, second parameter as x coord and third parameter as y coord #'
	thisNode = Node("First Node", 1, 3)
	print '- Output: Node name: '+str(thisNode.name)+'. Expected: First Node'
	print '- Output: Node x: '+str(thisNode.x)+ '. Expected: 1'
	print '- Output: Node y: '+str(thisNode.y)+ '. Expected: 3'

	print '\n'	

	print '# input: Node("SecondNode", 5, 7) #'
	secondNode = Node("SecondNode", 5, 7)
	print '- Output: Node name: '+str(secondNode.name)+'. Expected: SecondNode'
	print '- Output: Node x: '+str(secondNode.x)+ '. Expected: 5'
	print '- Output: Node y: '+str(secondNode.y)+ '. Expected: 7'

	print '\n'

	# We will make the SecondNode as the child of FirstNode.
	print '### Testing function addChild(child) with child as type of object Node ###'
	print '# Function is used to assign children and parent to the associated node. #'
	print '# In this test, we are going to assign secondNode as child of FirstNode. #'
	print '# It will return true if the child assignment is successful, false otherwise #'
	check = thisNode.addChild(secondNode)
	print '- Output: '+str(check)+'. Expected: True'
	print '- Check the child of firstNode: Output: '+str(thisNode.children[0].name)+'. Expected: SecondNode'
	print '- Check the parent of secondNode: Output: '+str(secondNode.parent.name)+'. Expected: First Node'
	
	print '\n'

	# We will remove SecondNode
	print '### Testing function removeNode() with node as type of object Node ###'
	print '# Function is used to remove the node only if it there is no children. #'
	print '# Return true if it is removed, an error message will be shown otherwise #'
	print '# First, let\'s try to remove firstNode. #'
	try:
		check = thisNode.removeNode()
	except Exception,e:
		check = e
	print '- Output: '+str(check)+'.\n-Expected: Unsuccessful! Children still exist!'

	print '# Removal of second node #'
	check = secondNode.removeNode()
	print '- Output: '+str(check)+'. Expected: True'
	print '- Check the child of firstNode: Output: '+str(thisNode.children)+'. Expected: []'

	print '\n'

	# Add another node
	print '### Testing function changeParent() ###'
	print '# Function is used to change parent to its grandparent if the parent is not root #'
	print '# Testing will be done by looking at the parent of the node. #'
	print '# To do this testing, we need to add the secondNode back as the child of firstNode and add another node as the child node of secondNode #'
	# Adding secondNode back to the child of firstNode
	thisNode.addChild(secondNode)
	# Adding the thirdNode
	print '# Adding a new node: Node(\'ThirdNode\',10,20) and let this node be the child of second node #'
	thirdNode = Node('ThirdNode',10,20)
	# Assign thirdNode as the child of secondNode
	secondNode.addChild(thirdNode)
	print '- First Node child(ren): '+str(thisNode.children[0].name)+'. Expected: SecondNode'
	print '- SecondNode child(ren): '+str(secondNode.children[0].name)+'. Expected: ThirdNode'
	print '- ThirdNode child(ren): '+str(thirdNode.children)+'. Expected: []'
	# Chaning third node parent
	print '# Changing parent of thirdNode #'
	thirdNode.changeParent()
	print '- First Node child(ren): '+ ', '.join([x.name for x in thisNode.children]) +'. Expected: SecondNode, ThirdNode'
	print '- SecondNode child(ren): '+str(secondNode.children)+'. Expected: []'
	print '- ThirdNode child(ren): '+str(thirdNode.children)+'. Expected: []'

	print '\n'

	# Set capacity test
	print '### TEsting function setCapacity(capacity) with capacity as integer value ###'
	print '# input: thirdNode.setCapacity(20) #'
	thirdNode.setCapacity(20)
	print "- Capacity of thirdNode. Output: "+str(thirdNode.capacity)+". Expected: 20"

	print '\n'

	# Set route test
	print '### Testing function setRoute(text) with text as list of integer ###'
	print '# Function will extend the new list before the older list. #'
	print '# Input: secondNode.setRoute([1,5,7]) #'
	secondNode.setRoute([1,5,7])
	print "- Route of secondNode. Output: "+str(secondNode.route)+". Expected: [1, 5, 7]"
	print '# Input: secodNode.setRoute([2,4,8]). This time, 2,4,8 should be extended the older list #'
	secondNode.setRoute([2,4,8])
	print "- Route of secondNode.\n- Output: "+str(secondNode.route)+". Expected: [2, 4, 8, 1, 5, 7]."

	print '\n******** End Testing for class Node ********\n'
