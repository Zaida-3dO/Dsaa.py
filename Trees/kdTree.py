from binaryTree import BstNode, BinarySearchTree


class KDTree(BinarySearchTree):
    def __init__(self, k, value=None):
        super(KDTree, self).__init__()
        self.__k = k
        if value is not None:
            self.initializeTree(KdNode(value, self.__k, 0))

    def insertValue(self, value):
        if len(value) < self.__k:
            print('Can\'t insert this value to a {}-Dimensional Tree; insufficient dimensions'.format(self.__k))
        elif not self.hasRoot:
            self.initializeTree(KdNode(value, self.__k, 0))
        else:
            node = KdNode(value, self.__k)
            currentNode = self.root
            while currentNode != node:
                if node.isEqualTo(currentNode):
                    currentNode = node
                elif node.isLeftOf(currentNode):
                    if currentNode.hasLeftChild:
                        currentNode = currentNode.leftChild
                    else:
                        currentNode.leftChild = node
                        currentNode = node
                else:
                    if currentNode.hasRightChild:
                        currentNode = currentNode.rightChild
                    else:
                        currentNode.rightChild = node
                        currentNode = node

    def deleteValue(self, value):
        if len(value) < self.__k or not self.hasRoot:
            print('Node does not exist in tree!')
        else:
            currentNode = self.root
            node = KdNode(value, -1)
            while not currentNode.isEqualTo(node):
                if node.isLeftOf(currentNode):
                    if currentNode.hasLeftChild:
                        currentNode = currentNode.leftChild
                    else:
                        print('Node does not exist in tree!')
                        return
                else:
                    if currentNode.hasRightChild:
                        currentNode = currentNode.rightChild
                    else:
                        print('Node does not exist in tree!')
                        return
            currentNode.delete()


class KdNode(BstNode):
    def __init__(self, value, k, activeK=None):
        super(KdNode, self).__init__(value)
        self.__activeDimension = activeK
        self.__k = k

    @property
    def leftChild(self):
        return self.getChildWithKey('leftChild')

    @leftChild.setter
    def leftChild(self, leftChild):
        leftChild.__activeDimension = self.__activeDimension + 1
        if leftChild.__activeDimension >= self.__k:
            leftChild.__activeDimension = 0
        self.addChildWithKey(leftChild, 'leftChild')

    @property
    def rightChild(self):
        return self.getChildWithKey('rightChild')

    @rightChild.setter
    def rightChild(self, rightChild):
        rightChild.__activeDimension = self.__activeDimension + 1
        if rightChild.__activeDimension >= self.__k:
            rightChild.__activeDimension = 0
        self.addChildWithKey(rightChild, 'rightChild')

    @property
    def hasRightChild(self):
        return self.hasChildWithKey('rightChild')

    @property
    def hasLeftChild(self):
        return self.hasChildWithKey('leftChild')

    def isEqualTo(self, node):
        for i in range(self.__k):
            if self.value[i] != node.value[i]:
                return False
        return True

    def isLeftOf(self, parentNode):
        return self.value[parentNode.__activeDimension] <= parentNode.value[parentNode.__activeDimension]

    def delete(self):
        if self.hasLeftChild:
            node = self.leftChild.__searchEstNode(self.__activeDimension, False)
            self._setValue(node.value)
            node.delete()
        elif self.hasRightChild:
            node = self.rightChild.__searchEstNode(self.__activeDimension, True)
            self._setValue(node.value)
            node.delete()
        else:
            self.parent.removeChild(self)

    # TODO optimize
    def __searchEstNode(self, k, smallest):
        estNode = self
        turnKey = 'leftChild' if smallest else 'rightChild'
        if self.__activeDimension == k:
            if self.hasChildWithKey(turnKey):
                child = self.getChildWithKey(turnKey).__searchEstNode(k, smallest)
                if smallest:
                    if child.value[k] <= estNode.value[k]:
                        estNode = child
                else:
                    if child.value[k] >= estNode.value[k]:
                        estNode = child
            else:
                return estNode
        else:
            for child in self.children:
                estChild = child.__searchEstNode(k, smallest)
                if smallest:
                    if estChild.value[k] <= estNode.value[k]:
                        estNode = estChild
                else:
                    if estChild.value[k] >= estNode.value[k]:
                        estNode = estChild
        return estNode
