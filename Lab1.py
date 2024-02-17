from numpy import random
class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def generate_string(self, start_symbol):
        gen_string = ""
        temp = random.choice(self.P[start_symbol])
        while temp != "":
            for i in temp:
                if i in self.VT:
                    gen_string += i
                    temp = temp.replace(i, "")
                else:
                    temp = temp.replace(i, random.choice(self.P[i]))
        return gen_string

    def generate_valid_strings(self, start_symbol, num_strings):
        valid_strings = []
        for _ in range(num_strings):
            valid_strings.append(self.generate_string(start_symbol))
        return valid_strings

class DFA():
    def __init__(self, VN, VT, P, nameFinalState):
        self.startState = "S"
        self.nonTerm = VN

        self.transictions = {}
        for i in P:
            for j in P[i]:
                term = ""
                perehod = ""
                for letter in j:
                    if(letter in VN):
                        term = letter
                    else:
                        perehod = letter
                #check if State is not in dict
                if i not in self.transictions:
                    self.transictions[i] = {}
                
                if term == "":
                    term = nameFinalState
                self.transictions[i][perehod] = term
                    
        print(self.transictions)
        self.P = P
        self.finalState = nameFinalState

    def checkString(self, string):
        currentTransitions = self.startState
        for i in range(0, len(string)):
            if string[i] not in self.transictions[currentTransitions]:
                return False
            currentTransitions = self.transictions[currentTransitions][string[i]]
            if currentTransitions == self.finalState and i!=len(string)-1:
                return False

        if currentTransitions == self.finalState:
            return True
        else:
            return False


VN = ["S", "I", "J", "K"] # non-terminal(circles)
VT = ["a", "b", "c", "e", "n", "f", "m"] # perehodi
# Start symbol S
# Add final state
# if non-terminal 
P = {
    "S": ["cI"],
    "I": ["bJ", "fI", "eK"],
    "J": ["nJ", "cS"],
    "K": ["nK", "m"]
}

grammar = Grammar(VN, VT, P)
print(grammar.generate_valid_strings("S", 5))
finite = DFA(VN, VT, P, "FINAL")

check_examples = ['bcnm', 'cbccbccbnccffbccbccbnnnnccem', 'cbccfbccbnnnnnccffffemm', 'cennnnm', 'cbccbccfbccennnm']
for i in check_examples:
    print(f"{i} = {finite.checkString(i)}")