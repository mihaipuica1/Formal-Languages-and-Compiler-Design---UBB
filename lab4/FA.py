class FA:
    def __init__(self, fileName):
        # Q = finite set of states
        # E = finite alphabet
        # F = set of final states
        # q0 = initial state
        # D(elta) = transition function
        self.__Q = None
        self.__E = None
        self.__F = None
        self.__q0 = None
        self.__D = []
        self.__fileName = fileName


    def getFAfromFile(self):
        with open(self.__fileName) as file:
            # the first strip() gets rid of the newline at the end of the line
            # the split('=')[1] splits the line in the lhs and rhs and only keeps the rhs(states or alphabet)
            # the split(',') splits the states/alphabet into a separate list
            self.__Q = file.readline().strip().split('=')[1].split(',')
            self.__E = file.readline().strip().split('=')[1].split(',')
            self.__F = file.readline().strip().split('=')[1].split(',')
            self.__q0 = file.readline().strip().split('=')[1].split(',')
            # since there can be more transitions (will be specified in the documentation), this will read 'D='
            # but it only indicates what will appear in the file after this
            file.readline()

            # getting through all the transitions
            for line in file:
                triple = line.strip().split('=')[0].replace('(', '').replace(')', '').split(',')
                triple.append(line.strip().split('=')[1])
                self.__D.append(triple)

    def menu(self):
        print("1. Print set of states")
        print("2. Print the alphabet")
        print("3. Print the set of final states")
        print("4. Print the initial state")
        print("5. Print the transitions")
        while True:
            menuCommand = input()
            if menuCommand == "1":
                print("The set of states is: " + str(self.__Q))
            elif menuCommand == "2":
                print("The finite alphabet is: " + str(self.__E))
            elif menuCommand == "3":
                print("The set of final states is: " + str(self.__F))
            elif menuCommand == "4":
                print("The initial state is: " + str(self.__q0))
            elif menuCommand == "5":
                print("The transitions are:")
                for triple in self.__D:
                    transition = "(" + triple[0] + "," + triple[1] + ")=>" + triple[2]
                    print(transition)

    def getQ(self):
        return self.__Q

    def getE(self):
        return self.__E

    def getF(self):
        return self.__F

    def getq0(self):
        return self.__q0

    def getD(self):
        return self.__D