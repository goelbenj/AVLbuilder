from lab0_utilities import *

class Languages:
	def __init__(self):
		self.data_by_year = {}

	def build_trees_from_file(self, file_object):
		file_object.readline()
		for line in file_object:
			lineParse = line.strip().split(',')
			name = lineParse[1]
			year = int(lineParse[0])
			if (lineParse[2].isdigit() == True):
				count = int(lineParse[2])
				entry = LanguageStat(name,year,count)
				node = Node(entry)
				if (entry.year in self.data_by_year.keys()):
					tree = self.data_by_year[year]
					tree.balanced_insert(node)
					self.data_by_year[year] = tree
				else:
					tree = BalancingTree(node)
					self.data_by_year[year] = tree
		return self.data_by_year

	def query_by_name(self, language_name):
		dict = {}

		for i in self.data_by_year.keys():
			tree = self.data_by_year[i]
			status = False
			iter = tree.root
			while iter != None and not status:
				if(iter.val.name == language_name):
					status = True
				else:
					if(str(iter._val) < language_name):
						iter = iter.right
					else:
						iter = iter.left
			if(iter != None):
				dict[i] = iter.val.count

		return dict

	def query_by_count(self, threshold = 0):
		dict = {}

		for i in self.data_by_year.keys():
			languages_list = []
			tree = self.data_by_year[i]
			self.query_by_count_build_list(threshold, tree.root, languages_list)
			if(languages_list != []):
				dict[i] = languages_list
		return dict

	def query_by_count_build_list(self, threshold, root, langs):
		iter = root
		status = False
		self.post_order_recurse(iter, threshold, langs)

	def post_order_recurse(self, node, threshold, langs):
		if (node != None):
			self.post_order_recurse(node.left, threshold, langs)
			self.post_order_recurse(node.right, threshold, langs)
			if node.val.count > threshold:
				langs.append(node.val.name)


class BalancingTree:
	def __init__(self, root_node):
		self.root = root_node

	def balanced_insert(self, node, iter = None):
		iter = iter if iter else self.root
		self.insert(node, iter)
		self.balance_tree(node)


	def insert(self, node, iter = None):
		iter = iter if iter else self.root
		# insert at correct location in BST
		if node._val < iter._val:
			if iter.left is not None:
				self.insert(node, iter.left)
			else:
				node.parent = iter
				iter.left = node
		else:
			if iter.right is not None:
				self.insert(node, iter.right)
			else:
				node.parent = iter
				iter.right = node
		return


	def balance_tree(self, node):
		self.post_order_changes(self.root)
		current = node
		status = False
		while current != None and not status:
			currBalanceFactor = self.find_balance_factor(current)
			if (currBalanceFactor < -1 or currBalanceFactor > 1):
				status = True
			else:
				current = current.parent

		if (status and current != None):
			currBalanceFactor = self.find_balance_factor(current)
			if (currBalanceFactor > 1): #we know this to be right heavy
				curr_child = current.right
				bf_current_child = self.find_balance_factor(curr_child)
				# print(curr_child.parent is current)
				if (bf_current_child == 1):
					self.left_rotate(current)
				elif (bf_current_child == -1):
					self.right_rotate(curr_child)
					self.left_rotate(current)
				self.find_balance_factor(current)
				self.find_balance_factor(curr_child)
			elif (currBalanceFactor < -1): #we know this to be right heavy
				curr_child = current.left
				bf_current_child = self.find_balance_factor(curr_child)
				if (bf_current_child == -1):
					self.right_rotate(current)
				elif (bf_current_child == 1):
					self.left_rotate(curr_child)
					self.right_rotate(current)
				self.find_balance_factor(current)
				self.find_balance_factor(curr_child)
		self.post_order_changes(self.root)

	def post_order_changes(self, node):
		if (node != None):
			self.post_order_changes(node.left)
			self.post_order_changes(node.right)
			self.update_height(node)
			self.find_balance_factor(node)

	def pre_order_search(self, node):
		if (node != None):
			return(node)
			self.pre_order_search(node.left)
			self.pre_order_search(node.right)



	def update_height(self, node):
		node.height = 1 + max(self.height(node.left), self.height(node.right))


	def height(self, node):
		return node.height if node else -1


	def left_rotate(self, z):
		y = z.right
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y
		z.right = y.left
		if z.right is not None:
			z.right.parent = z
		y.left = z
		z.parent = y
		self.update_height(z)
		self.update_height(y)


	def right_rotate(self, z):
		y = z.left
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.right is z:
				y.parent.right = y
			elif y.parent.left is z:
				y.parent.left = y
		z.left = y.right
		if z.left is not None:
			z.left.parent = z
		y.right = z
		z.parent = y
		self.update_height(z)
		self.update_height(y)

	def find_balance_factor(self, node):
		height_right = self.height(node.right)
		height_left = self.height(node.left)
		balanceFactor = height_right - height_left
		node.bf = balanceFactor
		return balanceFactor

	def is_balanced(self):
		if self.root.bf > 1 or self.root.bf < -1:
			return False
		else:
			return True

	def to_print(self, node):
		if node:
			x = node.left._val if node.left else None
			y = node.right._val if node.right else None
			z = node.parent._val if node.parent else node is self.root
		print("Node {}, parent = {}, left = {}, right = {}, balance_factor {}".format(node._val, z, x, y, node.bf))
		print("node_height", node.height)
		self.to_print(node.left)
		self.to_print(node.right)
