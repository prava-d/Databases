'''
B+ Tree implementation
'''

class BPlusNode:

	order = 3

	def __init__(self, iL):
		self.isLeaf = iL
		self.parent = None
		self.keys = []
		self.pointers = [None,None,None,None]
		self.nextNode = None
		self.nodeIdx = None
		self.numKeys = 0

	def printKeys(self):
		for key in self.keys():
			print("\n",key


   def splitIncludeMedian(self):
		#splitting the node when the node has the maximum number of keys.
		if numKeys = 3:
			medianIndex = 1
			splitNode1 = BPlusNode(self.il)
			splitNode1.parent = self.parent
			splitNode1.keys = self.keys[0:1]

			splitNode2 = BPlusNode(self.il)
			splitNode1.parent = self.parent
			splitNode1.keys = self.keys[2]

		return splitNode1, splitNode2

	def splitExcludeMedian(self):
			#splitting the node when the node has the maximum number of keys.
		if numKeys = 3:
				medianIndex = 1
				splitNode1 = BPlusNode(self.il)
				splitNode1.parent = self.parent
				splitNode1.keys = self.keys[0]

				splitNode2 = BPlusNode(self.il)
				splitNode1.parent = self.parent
				splitNode1.keys = self.keys[2]

		return splitNode1, splitNode2

	def add(self, inputval):
		if self.keys is None:
			self.keys.append(inputval)
			return

		#if the node is already full then the node has to be split to accomodate the key value that is being added.
		if len(self.keys) == self.order:

			leftNode, rightNode = self.split(self)

			if self.isLeaf:
				minOfRightNode = rightNode[0]
				parent = self.parent
				parent.add(minOfRightNode)

			else:


			if inputval > keys[2]:
				promote(keys[2])
			else:
				promote(inputval)
	   		return

		 index = 0
		 for key in self.keys:
			 if index == self.numKeys - 1:
				  self.keys.append(inputval)
				  return
			 if inputval > key:
				 self.keys =  self.keys[index:] + [key] + self.keys[:index]
				 return
			index++
		 numKeys++


	def promote(self, inputval):
		if self.parent:
			self.parent.add(inputval)
			return 1
		else:
			return 0 #deal with this in the tree class


class Tree:

	self.store = Storage()

	def __init__(self):
		self.root = BPlusNode(0)
		self.i0 = BPlusNode(1)
		self.i1 = BPlusNode(1)
		self.i2 = BPlusNode(1)

		self.root.nodeIdx = self.store.addNode(self.root)
		self.i0.nodeIdx = self.store.addNode(self.i0)
		self.i1.nodeIdx = self.store.addNode(self.i1)
		self.i2.nodeIdx = self.store.addNode(self.i2)

		self.i0.nextNode = self.i1
		self.i1.nextNode = self.i2

	def findPosForInsert(self,inputval):

		pass

	def create(self, inputval):
		pass

	def read(self, inputval):
		pass

	def update(self, inputval, newinputval):
		pass

	def delete(self, inputval):
		pass


class Storage:

	self.data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	self.treeNodes = []

	def __init__(self):
		pass

	def addNode(n):
		self.treeNodes.append(n)
		return len(treeNodes) - 1

root = Node(10)
print(root)
