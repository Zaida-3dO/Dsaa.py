class Tree:
    def __init__(self, value=None):
        self.__root = None
        if value is not None:
            self.initializeTree(TreeNode(value))

    @property
    def hasRoot(self):
        return self.__root is not None

    @property
    def root(self):
        return self.__root

    def initializeTree(self, root):
        self.__root = root

    def insertValue(self, value):
        node = TreeNode(value)
        if not self.hasRoot:
            self.initializeTree(node)
        else:
            self.__root.addChild(node)

    def display(self, tabs=1):
        if self.hasRoot:
            self.__root.display(0, set(), tabs)
        else:
            print('There are no nodes in the tree')


class TreeNode:
    def __init__(self, value):
        self.__value = value
        self.__parent = None
        self.__children = dict()
        self.__keyInParent = None

    def __setParent(self, parent):
        self.__parent = parent

    def __unsetParent(self):
        self.__parent = None

    def _setValue(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        for child in self.__children:
            yield self.__children[child]

    def getChildWithKey(self, childKey):
        return self.__children[childKey]

    @property
    def childrenCount(self):
        return len(self.__children)

    @property
    def hasParent(self):
        return self.parent is not None

    def hasChild(self, child):
        return child.__keyInParent in self.__children

    def hasChildWithKey(self, childKey):
        return childKey in self.__children

    def addChild(self, child):
        i = 0
        while i in self.__children:
            i += 1
        self.addChildWithKey(child, i)

    def addChildWithKey(self, child, childKey):
        if child.hasParent:
            child.__parent.removeChild(child)
        child.__parent = self
        child.__keyInParent = childKey
        self.__children[childKey] = child

    def removeChild(self, child):
        child.__parent = None
        del self.__children[child.__keyInParent]

    def removeChildWithKey(self, childKey):
        self.removeChild(self.__children[childKey])

    def _splitChildren(self):
        n = len(self.__children)
        n = n + 1 if n % 2 == 1 else n
        left, right = [], []
        i = 0
        for child in self.children:
            if i < n / 2:
                left.append(child)
            else:
                right.append(child)
            i += 1
        return left, right

    def display(self, level, lineLevels, tabs, topLines=False, isLastChild=False):
        left, right = self._splitChildren()
        if topLines:
            lineLevels.add(level - 1)
        nextTopLines = False
        for child in right:
            child.display(level + 1, lineLevels,tabs, nextTopLines)
            nextTopLines = True
        lineLevels.add(level - 1)
        TreeNode.printLineVerticals(lineLevels, level, tabs)
        print(('-' * ((4 * tabs) - 1)) + str(self.value))
        if isLastChild:
            lineLevels.remove(level - 1)
        nextTopLines = True
        for i in range(len(left)):
            child = left[i]
            child.display(level + 1, lineLevels,tabs, nextTopLines, i == (len(left) - 1))
            nextTopLines = True

    @staticmethod
    def printLineVerticals(lineLevels, level, tabs):
        for i in range(level):
            print(('\t ' * tabs), end='')
            if i in lineLevels:
                print('|', end='')
