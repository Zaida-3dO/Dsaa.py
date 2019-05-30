from tree import TreeNode, Tree


class BinarySearchTree(Tree):
    def __init__(self, value=None):
        super(BinarySearchTree, self).__init__()
        if value is not None:
            self.initializeTree(BstNode(value))

    def insertValue(self, value):
        node = BstNode(value)
        if not self.hasRoot:
            self.initializeTree(node)
        else:
            currentNode = self.root
            while currentNode != node:
                if node.value < currentNode.value:
                    if currentNode.hasLeftChild:
                        currentNode = currentNode.leftChild
                    else:
                        currentNode.leftChild = node
                        currentNode = node
                elif node.value > currentNode.value:
                    if currentNode.hasRightChild:
                        currentNode = currentNode.rightChild
                    else:
                        currentNode.rightChild = node
                        currentNode = node
                else:
                    currentNode = node

    def deleteValue(self, value):
        if not self.hasRoot:
            print('Node does not exist in tree!')
        else:
            currentNode = self.root
            while currentNode.value != value:
                if value < currentNode.value:
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


class BstNode(TreeNode):
    def __init__(self, value):
        super(BstNode, self).__init__(value)

    @property
    def leftChild(self):
        return self.getChildWithKey('leftChild')

    @leftChild.setter
    def leftChild(self, leftChild):
        self.addChildWithKey(leftChild, 'leftChild')

    @property
    def rightChild(self):
        return self.getChildWithKey('rightChild')

    @rightChild.setter
    def rightChild(self, rightChild):
        self.addChildWithKey(rightChild, 'rightChild')

    @property
    def hasRightChild(self):
        return self.hasChildWithKey('rightChild')

    @property
    def hasLeftChild(self):
        return self.hasChildWithKey('leftChild')

    @property
    def children(self):
        if self.hasLeftChild:
            yield self.leftChild
        if self.hasRightChild:
            yield self.rightChild

    def delete(self):
        if self.hasLeftChild:
            currentNode = self.leftChild
            while currentNode.hasRightChild:
                currentNode = currentNode.rightChild
            self._setValue(currentNode.value)
            currentNode.delete()
        elif self.hasRightChild:
            currentNode = self.rightChild
            while currentNode.hasLeftChild:
                currentNode = currentNode.leftChild
            self._setValue(currentNode.value)
            currentNode.delete()
        else:
            self.parent.removeChild(self)

    def _splitChildren(self):
        left, right = [], []
        if self.hasLeftChild:
            left.append(self.leftChild)
        if self.hasRightChild:
            right.append(self.rightChild)
        return left, right
