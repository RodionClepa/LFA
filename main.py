from numpy import random

class FA():
    def __init__(self, startState, listStates, alphabet, transitions, finalState):
        if startState not in listStates:
            raise Exception("startState is not present in listStates")
        self.startState = startState
        self.listStates = listStates
        self.alphabet = alphabet
        self.transitions = transitions
        self.finalState = finalState
    
    def determine_DFA_or_NDFA(self):
        for i in self.transitions:
            for symbol in self.transitions[i]:
                if len(self.transitions[i][symbol])>1:
                    return "NDFA"
        return "DFA"
    
    def convert_NDFA_to_DFA(self):
        state_table = {}
        newState = [(self.startState, )]
        alreadyMet = [self.finalState]
        while newState:
            current_state = newState[0]
            if current_state not in state_table:
                state_table[current_state] = {}
            
            trnsFnct = {}
            trnsFnct[current_state] = {}
            for symbol in self.alphabet:
                for state in current_state:
                    # In case if state doesnt have any transitions
                    if state not in self.transitions:
                        if symbol not in state_table[current_state]:
                            state_table[current_state][symbol] = ""
                        else:
                            # To skip state without transitions
                            if state in self.transitions:
                                state_table[current_state][symbol] = tuple(sorted(set(
                                    tuple(state_table[current_state][symbol]) + tuple(self.transitions[state][symbol])
                                    )))
                        continue
                
                    if symbol not in self.transitions[state]:
                        if symbol not in state_table[current_state]:
                            state_table[current_state][symbol] = ""
                    else:
                        if symbol not in state_table[current_state]:
                            state_table[current_state][symbol] = tuple(sorted(self.transitions[state][symbol]))
                        else:
                            state_table[current_state][symbol] = tuple(sorted(set(
                                tuple(state_table[current_state][symbol]) + tuple(self.transitions[state][symbol])
                                )))

            alreadyMet.append(newState[0])
            newState.pop(0)
            # Append new states un met state
            for passState in state_table:
                for symbol in state_table[passState]:
                    combState = state_table[passState][symbol]
                    if combState not in alreadyMet and combState !="":
                        newState.append(combState)
            
        self.transitions = state_table
        print(self.transitions)

                    
# transitions = {'q0': {'a': ['q1']}, 'q1': {'b': ['q1', 'q2']}, 'q2': {'a': ['q4'], 'b':['q3']}, 'q3': {'a': ['q1']}}


class Grammar():
    def __init__(self, finite):
        self.VN = finite.listStates
        self.VT = finite.alphabet
        self.S = finite.startState
        self.P = {}
        trns = finite.transitions
        for sender in trns:
            if sender not in self.P:
                self.P[sender] = []
            for symbol in trns[sender]:
                for destinator in trns[sender][symbol]:
                    if destinator == finite.finalState:
                        terminal = symbol
                    else:
                        terminal = symbol + destinator
                    
                    self.P[sender].append(terminal)
        
    def printAllInfo(self):
        print(f"VN = {self.VN}")
        print(f"VT = {self.VT}")
        print(f"S = {self.S}")
        print(f"P = {self.P}")
        
    def generate_string(self):
        gen_string = ""
        temp = random.choice(self.P[self.S])
        while temp != "":
            foundState = ""
            for i in self.P:
                if i in temp:
                    foundState = i
            temp = temp.replace(foundState, "")
            gen_string += temp
            if foundState != "":
                temp = random.choice(self.P[foundState])
            else:
                break
        return gen_string

    def generate_valid_strings(self, start_symbol, num_strings):
        valid_strings = []
        for _ in range(num_strings):
            valid_strings.append(self.generate_string())
        return valid_strings
    
    def is_regular(self):
        for i in self.P:
            if len(self.P[i])>2:
                return False
            for production in self.P[i]:
                for nonTerm in self.VN:
                    symbols = production.replace(nonTerm, "")
                if symbols == "":
                    return False
        return True
    
    def is_context_free(self):
        for i in self.P:
            non_terminal = i
            for j in self.VN:
                non_terminal = non_terminal.replace(j, "")
            if non_terminal != "":
                return False
        return True

    def is_context_sensitive(self):
        for non_terminal in self.P:
            for production in self.P[non_terminal]:
                if len(non_terminal) > len(production):
                    return False
        return True

    def check_chomsky(self):
        if self.is_regular() is True:
            return "Type 3"
        elif self.is_context_free() is True:
            return "Type 2"
        elif self.is_context_sensitive() is True:
            return "Type 1"
        else:
            return "Type 0"
        

listStates = ["q0","q1","q2","q3","q4"] # states
alphabet = ["a","b"] # alphabet
finalState = "q4" # final state
startState = "q0"
transitions = {'q0': {'a': ['q1']}, 'q1': {'b': ['q1', 'q2']}, 'q2': {'a': ['q4'], 'b':['q3']}, 'q3': {'a': ['q1']}}

# listStates = ['S', 'I', 'J', 'K'] # states
# alphabet = ['a', 'b', 'c', 'e', 'n', 'f', 'm'] # alphabet
# finalState = "FINAL" # final state
# startState = "S"
# transitions = {'S': {'c': ['I']}, 'I': {'b': ['J'], 'f': ['I'], 'e': ['K', 'FINAL']}, 'J': {'n': ['J'], 'c': ['S']}, 'K': {'n': ['K'], 'm': ['FINAL']}}

finite = FA(startState, listStates, alphabet, transitions, finalState)
gramm = Grammar(finite)
print("Converted from FA to Grammar")
gramm.printAllInfo()
print("Test String")
print(gramm.generate_valid_strings("q0", 5))

print(f"NDFA or DFA -- {finite.determine_DFA_or_NDFA()}")
print("NDFA to DFA result:")
finite.convert_NDFA_to_DFA()

print(f"Chomsky {gramm.check_chomsky()}")