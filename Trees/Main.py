from kdTree import KDTree


class TreeConsole:
    def __init__(self):
        self.kdt = None
        self.k = None
        self.hasTree = False

    def mainMenu(self):
        print('Enter a value from [1-4] to run the associated command: Enter any other key to Quit')
        print('1. Display')
        print('2. Insert')
        print('3. Delete')
        print('4. Reset')
        print('*. Exit')
        inp = input()
        if inp == '1':
            print()
            print('::::{}-K D TREE::::'.format(self.k))
            print()
            self.kdt.display(self.k+1)
            print('\n')
        elif inp == '2':
            val = []
            for i in range(self.k):
                print('Enter value at dimension {}:'.format(i), end='')
                val.append(input())
            print('Adding {} to tree'.format(str(tuple(val))))
            self.kdt.insertValue(tuple(val))
            print('Operation Completed')
        elif inp == '3':
            val = []
            for i in range(self.k):
                print('Enter value at dimension {}:'.format(i), end='')
                val.append(input())
            print('Deleting {} from tree'.format(str(tuple(val))))
            self.kdt.deleteValue(tuple(val))
            print('Operation Completed')
        elif inp == '4':
            print('Are you sure, this will delete all nodes in the current tree. Press 1. to confirm')
            if input() == '1':
                self.kdt = None
                self.k = None
                self.hasTree = False
        else:
            print('Press 1. to close the app. Any other key to continue')
            if input() == '1':
                return True
        return False

    def initializeTree(self):
        print('Create a new KD Tree.')
        print('To create a new KD Tree you need to specify \'K\'. This is the number of dimensions on each node')
        print('Enter K: ', end='')
        k = int(input())
        self.kdt = KDTree(k)
        self.k = k
        self.hasTree = True


x = TreeConsole()
running = True
while running:
    if x.hasTree:
        running = not x.mainMenu()
    else:
        x.initializeTree()
