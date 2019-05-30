class TreeConsole:
    def __init__(self):
        self.kdt = None
        self.k = None

    def mainMenu(self):
        print('Enter a value from [1-4] to run the associated command: Enter any other key to Quit')
        print('1. Display')
        print('2. Insert')
        print('3. Delete')
        print('4. Reset')
        print('*. Exit')
        inp = input()
        if inp == 1:
            print()
            print('::::{}-K D TREE::::'.format(self.k))
            print()
            self.kdt.display()
        elif inp == 2:
            val = []
            for i in range(self.k):
                print('Enter value at dimension {}:'.format(i), end='')
                val.append(input())
            tuple(val)

