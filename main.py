transations = {
    "open_parenthesis": ["numbers", "open_parenthesis"],
    "math_operation": ["numbers", "open_parenthesis"],
    "close_parenthesis": ["math_operation", "close_parenthesis"],
    "numbers": ["numbers", "close_parenthesis", "math_operation"],
    "START": ["open_parenthesis", "numbers"]
}

data = {
    "open_parenthesis":["(", "["],
    "close_parenthesis":[")", "]"],
    "math_operation": ["+", "-", "*", "/", "%", "^"],
    "numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

def check_equation(equation):
    seq_parenthesis = []
    category_mapping = ["START"]
    failed_on = ""
    valid_tokens = []
    for symbol in equation:
        # Adding parenthesis in stack
        if symbol in data["open_parenthesis"]:
            if symbol == "(":
                seq_parenthesis.append(")")
            elif symbol == "[":
                seq_parenthesis.append("]")
        # Check if we have oppend parenthesis
        elif symbol in data["close_parenthesis"]:
            try:
                if (symbol == ")" and seq_parenthesis[-1] == ")") or (symbol == "]" and seq_parenthesis[-1] == "]"):
                    seq_parenthesis.pop()
                else:
                    print(f"ERROR: brackets were not closed in correct order, parenthesis stack {seq_parenthesis}")
                    print(f"Failed on symbol {failed_on}")
                    return False # Mismatched opening and closing parenthesis
            except IndexError:
                print(f"ERROR: not enough open parenthesis, parenthesis stack {seq_parenthesis}")
                print(f"Failed on symbol {failed_on}")
                return False # Mismatched opening and closing parenthesis
        # Finding current category
        for category in data:
            if symbol in data[category]:
                current_category = category
                break
        # Check if category doesnt break any rule
        if current_category in transations[category_mapping[-1]]:
            category_mapping.append(current_category)
        else:
            # print(category_mapping)
            # print(current_category)
            print(f"ERROR: a transitions weren't respected, last category - {category_mapping[-1]}, current - {current_category}")
            print(f"Failed on symbol {failed_on}")
            return False

        valid_tokens.append(symbol)
        failed_on += symbol
    if len(seq_parenthesis) != 0:
        print(f"ERROR: not all brackets were closed, parenthesis stack {seq_parenthesis}")
        # print(seq_parenthesis)
        print(f"Failed on symbol {failed_on}")
        return False
    print(valid_tokens)
    return True

test_equation = ["1+2+3", "2*(3+4)", "2*(3+4", "[(6+3)*2*(7/2)]+[[(6-3)/3+(2-1)]+3]", "2*3/(4-1)", "5*(6-2)/3+7", "8^2-4*3", "(9+3)/(2-1)", "10*(11-2)/(5+3)", "2*(3+4))", "3+(4*5", "6*7++8", "9^2*/3", "(10+11)*12]", "13+(14-15))", "[(2+4*[5^2]])"]

for i in test_equation:
    print(f"{i} - {check_equation(i)}")
    print("----------------------------------------------------------")