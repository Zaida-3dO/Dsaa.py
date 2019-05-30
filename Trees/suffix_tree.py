from tree import TreeNode, Tree


class SuffixTree(Tree):
    def __init__(self, text):
        self.__text = text + '$'
        self.__root = RootNode(self)
        self.__has_leaf_count = False

    @property
    def root(self):
        return self.__root

    @property
    def text_length(self):
        return len(self.__text)

    @property
    def has_leaf_count(self):
        return self.__has_leaf_count

    def letter_at(self, index):
        return self.__text[index]

    def is_same_letter(self, index1, index2):
        return self.__text[index1] == self.__text[index2]

    # returns the substring from start to end, [start and end inclusive], can handle end == None
    def get_substring(self, start, end):
        if end is None:
            return self.__text[start:]
        else:
            return self.__text[start:end + 1]

    def updated(self):
        self.__has_leaf_count = False

    # Makes calling no_of_child_leaves execute faster
    def count_leaves(self):
        self.__root.no_of_child_leaves
        self.__has_leaf_count = True


class SuffixNode(Node):
    def __init__(self, start, end=None):
        if end is not None:
            assert start <= end, 'start int: {} cannot be greater than end int: {}'.format(start, end)

        super(SuffixNode, self).__init__((start, '#' if end is None else end))

        self.__end = end
        self.__key = None
        self.__tree = None
        self.__start = start
        self.__child_leaves = 1
        self.__suffix_link = None
        self.__before_start = None
        self.__children_keys = dict()

    @property
    def has_suffix_link(self):
        return self.__suffix_link is not None

    @property
    def suffix_link(self):
        return self.__suffix_link

    @suffix_link.setter
    def suffix_link(self, suffix_link):
        self.__suffix_link = suffix_link

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def has_tree(self):
        return self.__tree is not None

    @start.setter
    def start(self, start):
        if self.__end is not None:
            assert start <= self.__end, 'start int: {} cannot be greater than end int: {}'.format(start, self.__end)

        key = self.__tree.letter_at(start) if self.has_tree else None

        if self.has_parent:
            assert key not in self.parent.__children_keys, 'Duplicate key: {} found in Node {}'.format(key, self.parent)
            del (self.parent.__children_keys[self.key])
            self.parent.__children_keys[key] = self

        self.__key = key
        self.__start = start
        self._set_value((self.__start, self.__end))

    @end.setter
    def end(self, end):
        assert end >= self.__start, 'start int: {} cannot be greater than end int: {}'.format(self.__start, end)
        self.__end = end
        self._set_value((self.__start, self.__end))

    @property
    def get_string(self):
        assert self.has_tree, 'To get string, Node must be attached to a tree'
        return self.__tree.get_substring(self.__start, self.__end)

    @property
    def length(self):
        if self.__end is None:
            assert self.has_tree, 'To get length of unending branch, you need to be connected to a Tree'
            return self.__tree.text_length - self.__start
        else:
            return (self.__end - self.__start) + 1

    @property
    def is_root(self):
        return self.__start == -1

    @property
    def is_leaf(self):
        return self.children_count == 0

    @property
    def no_of_child_leaves(self):
        if not self.__tree.has_leaf_count:
            if self.is_leaf:
                self.__child_leaves = 1
            else:
                sum_leaves = 0
                for child in self.children:
                    sum_leaves += child.no_of_child_leaves
                self.__child_leaves = sum_leaves
        return self.__child_leaves

    @property
    def key(self):
        return self.__key

    @property
    def real_length(self):
        if self.is_root:
            return 0
        length = (self.length + self.__before_start)
        if self.__end is None:
            length -= 1
        return length

    def has_child_with_key(self, key):
        return key in self.__children_keys

    def get_child_with_key(self, key):
        return self.__children_keys[key]

    def add_child(self, child):
        assert self.has_tree, 'Parent must already be connected to a tree before adding children'
        child.__tree = self.__tree
        child.__key = self.__tree.letter_at(child.__start)
        assert child.key not in self.__children_keys, \
            'The specified key, \'{}\' already exists under the specified node {}'.format(child.key, self)
        if self.is_root:
            child.__before_start = 0
        else:
            child.__before_start = self.__before_start + self.length
        super(SuffixNode, self).addChild(child)
        self.__children_keys[child.key] = child
        self.__tree.updated()

    def remove_child(self, child):
        assert child.key in self.__children_keys, 'Node {} is not a child of {}'.format(child, self)
        super(SuffixNode, self).removeChild(child)
        del (self.__children_keys[child.key])
        self.__tree.updated()

    def __str__(self):
        return self.get_string


class RootNode(SuffixNode):
    def __init__(self, tree):
        super(RootNode, self).__init__(-1)
        self._SuffixNode__tree = tree
