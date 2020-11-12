class FA:
    def __init__(self, fileName):
        # sequence = a sequence that has to be checked
        # Q = finite set of states
        # E = finite alphabet
        # F = set of final states
        # q0 = initial state
        # D(elta) = transition function
        self.__sequence = None
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
            self.__sequence = file.readline().strip()
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
        print("6. Check sequence")
        print("7. Validate FA")
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
            elif menuCommand == "6":
                self.checkSequence()


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

    def validateFA(self):
        valid = True
        if self.__q0 in self.__Q:
            valid = valid and True

        for state in self.__F:
            if state in self.__Q:
                valid = valid and True

        for transition in self.__Q:
            if transition[0] in self.__Q and transition[2] in self.__Q and transition[1] in self.__E:
                valid = valid and True

        if valid is True:
            print("FA is valid")
        else:
            print("FA is not valid")


    def checkSequence(self):
        print("We check if the sequence: " + self.__sequence + " is accepted by the FA")
        setOfStates = self.__Q
        state = self.__q0[0]
        derivations, result = state, state
        for i in range(len(self.__sequence) - 1):
            for transition in self.__D:

                if transition[0] == state and transition[2] == self.__sequence[i+1]:
                    state = transition[2]
                    derivations = str(derivations) + " =" + str(transition[1]) + "> " + str(state)
                    result = str(result) + str(state)
                    break
            #print('-----')


        if result == self.__sequence and result[len(result)-1] in self.__F:
            print("The sequence can be formed with the following derivations:")
            print(derivations)
        else:
            print("The sequence is not accepted by the FA")

