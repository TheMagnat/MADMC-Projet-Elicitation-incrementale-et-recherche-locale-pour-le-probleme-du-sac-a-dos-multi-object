
import numpy as np

from copy import copy, deepcopy


class NodeIterator:

	def __init__(self, node):
		self.node = node
		self.i = 0
		self.childsIt = None

		self.iterators = []

	def __next__(self):

		while self.iterators:

			currentIt = self.iterators[-1]

			try:
				retInst, retSolu = next( currentIt )

			except StopIteration:
				self.iterators.pop()

			else:
				return (retInst, retSolu)



		if self.i == 0:
			retInst = self.node.instance
			retSolu = self.node.solution
		else:

			if self.childsIt is None:
				self.childsIt = iter( self.node.binToChild.values() )

			try:
				currentNode = next( self.childsIt )

			except StopIteration:
				raise StopIteration

			else:
				self.iterators.append( iter(currentNode) )

				retInst, retSolu = next( self.iterators[-1] )

		self.i += 1
		return (retInst, retSolu)




class Node:

	def __init__(self, solution, instance):
		self.solution = solution
		self.instance = instance
		self.binToChild = {}
		self.totalSize = 1

	def __len__(self):
		return self.totalSize

	def __iter__(self):
		return NodeIterator(self)


	def deepVerifyDominate(self, solution):
		"""
		Verify if dominate in depth

		Return:
			True if solution is not dominated
			False otherwise
		"""

		toReinsert = []
		toDelete = []


		binary = solution < self.solution

		for childBinary, childSolution in self.binToChild.items():

			arrChildBinary = np.array( childBinary )

			if all( arrChildBinary[binary] ):
				#CHANGER SENS ICI POUR MINIMISATION
				if (solution < childSolution.solution).sum() == 0:
					toReinsert.extend( childSolution.binToChild.values() )
					toDelete.append( childBinary )

				else:

					oldLen = len( childSolution )

					toReinsert.extend( childSolution.deepVerifyDominate(solution) )

					self.totalSize += len( childSolution ) - oldLen


		for elem in toDelete:

			#Change size
			self.totalSize -= len(self.binToChild[elem])

			del self.binToChild[elem]


		return toReinsert



	def deepVerifyDominated(self, solution):
		"""
		Verify if is dominated in depth

		Return:
			True if solution is not dominated
			False otherwise
		"""

		binary = solution < self.solution

		for childBinary, childSolution in self.binToChild.items():

			arrChildBinary = np.array( childBinary )

			if all( ~( arrChildBinary[~binary] )):
				if (solution > childSolution.solution).sum() == 0:
					return False

				if not childSolution.deepVerifyDominated(solution):
					return False


		return True


	def insert(self, solution, instance):

		#Maximisation #CHANGER SENS ICI POUR MINIMISATION
		binary = solution < self.solution

		toReinsert = []
		toDelete = []

		for childBinary, childSolution in self.binToChild.items():

			arrChildBinary = np.array( childBinary )

			#If at least 1 is less than solution binary, no need
			if all( arrChildBinary[binary] ):
				#Here can dominate

				#This remove same
				if any(arrChildBinary[~binary]):


					#CHANGER SENS ICI POUR MINIMISATION
					if (solution < childSolution.solution).sum() == 0:
						#Solution dominate child
						
						toReinsert.extend( childSolution.binToChild.values() )
						toDelete.append( childBinary )

					else:

						oldLen = len( childSolution )

						toreinsertnow = childSolution.deepVerifyDominate(solution)

						toReinsert.extend( toreinsertnow )

						self.totalSize += len( childSolution ) - oldLen

						#print("old:", oldLen, "new:", len( childSolution) )
						#print(toreinsertnow)

			else:

				if all( ~( arrChildBinary[~binary] )):


					#Here can be dominated
					#CHANGER SENS ICI POUR MINIMISATION
					if (solution > childSolution.solution).sum() == 0:
						#child dominate solution
						#Stop everything
						return False

					else:
						if not childSolution.deepVerifyDominated(solution):
							return False


		binary = tuple(binary)


		if binary not in self.binToChild:

			#Change size
			self.totalSize += 1

			self.binToChild[binary] = Node( solution, instance )

			for elem in toDelete:

				#Change size
				self.totalSize -= len(self.binToChild[elem])

				del self.binToChild[elem]

			self.reinsert(toReinsert)

			return True

		else:
			#solution is dominated 
			if (solution > self.binToChild[binary].solution).sum() == 0:
				return False

			#self.binToChild[binary] is dominated by solution
			elif (solution < self.binToChild[binary].solution).sum() == 0:

				#Delete current node at binary
				tempoInsert = self.binToChild[binary].binToChild.values()
				self.totalSize += 1 - self.binToChild[binary].totalSize # +1 because new node

				#Create new node and replace
				self.binToChild[binary] = Node( solution, instance )

				for elem in toDelete:

					#Change size
					self.totalSize -= len(self.binToChild[elem])

					del self.binToChild[elem]

				self.reinsert(tempoInsert)
				self.reinsert(toReinsert)

				return True

			else:

				oldLen = len(self.binToChild[binary])

				if self.binToChild[binary].insert( solution, instance ):

					self.totalSize += len(self.binToChild[binary]) - oldLen

					for elem in toDelete:

						#Change size
						self.totalSize -= len(self.binToChild[elem])
						#print("deleted", len(self.binToChild[elem]), len(list(self.binToChild[elem])))
						del self.binToChild[elem]

					self.reinsert(toReinsert)

					return True

				else:
					return False

	def reinsert(self, toReinsert):

		for nodeObject in toReinsert:

			self.insert(nodeObject.solution, nodeObject.instance)

			self.reinsert( nodeObject.binToChild.values() )



	def addChild(self, childSolution):

		binary = childSolution < self.solution

		if binary not in self.binToChild:
			self.binToChild[binary] = Node(childSolution)


	def print(self, indent=0):

		for key, value in self.binToChild.items():
			#print("\t"*indent + f"{key}: {value.solution}")
			print("\t"*indent + f"{key} {value.solution}:")
			value.print(indent+1)




class QuadTree:

	def __init__(self, nbCriteria):
		self.nbCriteria = nbCriteria
		self.root = None

	def __len__(self):

		if self.root is None:
			return 0

		return len(self.root)

	def __iter__(self):
		return iter(self.root)

	def bulkInsert(self, instancesAndSolutions):
		for instance, solution in instancesAndSolutions:
			self.insert( solution, instance )

	def reinsert(self, toReinsert):
		for nodeObject in toReinsert:

			self.insert(nodeObject.solution, nodeObject.instance)

			self.reinsert( nodeObject.binToChild.values() )

	def insert(self, solution, instance):

		if self.root is None:
			self.root = Node( solution, instance )
			return True

		else:

			#Solution is dominated by root
			if (solution > self.root.solution).sum() == 0:
				return False

			#self.root is dominated by solution
			elif (solution < self.root.solution).sum() == 0:

				tempoInsert = self.root.binToChild.values()

				self.root = Node( solution, instance )

				self.reinsert(tempoInsert)

				return True

			else:
				return self.root.insert( solution, instance )




	def print(self):

		print(f"{self.root.solution}:")
		self.root.print(1)

	def test(self):

		l = []
		for elem in self:

			l.append(elem[1])

		l = np.array(l)

		dominated = set()

		for i, elem in enumerate(l):
			for j, elem2 in enumerate(l[i+1:]):
				if all(elem >= elem2):
					print(elem, "dominate", elem2)
					dominated.add( tuple(elem2) )

				elif all(elem <= elem2):
					print(elem2, "dominate", elem)
					dominated.add( tuple(elem) )

		print(dominated)
		print(len(dominated))


if __name__ == '__main__':
	

	exemple = [(np.array([1, 0, 1]), np.array([10, 10, 10])), (np.array([1, 0, 1]), np.array([5, 5, 23])), (np.array([1, 0, 1]), np.array([6, 16, 22])), (np.array([1, 0, 1]), np.array([14, 18, 6])), (np.array([1, 0, 1]), np.array([9, 8, 18])), (np.array([1, 0, 1]), np.array([3, 25, 16])), (np.array([1, 0, 1]), np.array([11, 15, 9])), (np.array([1, 0, 1]), np.array([40, 16, 7]))]

	newElem = (np.array([7, 20, 24]), np.array([1, 0, 1]))

	newElem2 = (np.array([11, 11, 11]), np.array([1, 0, 1]))

	newElem3 = (np.array([13, 14, 9]), np.array([1, 0, 1]))

	newElem4 = (np.array([12, 15, 9]), np.array([1, 0, 1]))

	newElem5 = (np.array([14, 19, 6]), np.array([1, 0, 1]))


	test = QuadTree(3)


	test.bulkInsert(exemple)

	ok = deepcopy(test)

	test.insert(*newElem)
	test.insert(*newElem2)
	test.insert(*newElem3)
	test.insert(*newElem4)
	test.insert(*newElem5)

	#exemple = exemple + [1, -2, 3]

	#test.bulkInsert(exemple)

	test.print()
	print(len(test))

	ok.print()
	print(len(ok))

	# for elem in test:
	# 	print(elem)

