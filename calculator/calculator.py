import string
from collections import deque


# TODO: multi bracket support
def bracket_partition(input_str):
    input_list = input_str.split()
    # Numbers or single operators
    while not all(c in string.digits or len(elem) == 1 for elem in input_list for c in elem):
        for i, elem in enumerate(input_list):
            if len(elem) == 1 or all(c in string.digits for c in elem):
                continue
            elif any(c in {"(", ")"} for c in elem):
                input_list = input_list[:i] + [elem[0], elem[1]] + input_list[i + 1:]
                break
            else:
                print("Invalid expression")
                raise ValueError
    return input_list


def reverse_polish_notation(input_str):
    def higher_equal_precedence(operator_1, operator_2):
        high_precedence = {"*", "/"}
        return (operator_1 in high_precedence) >= (operator_2 in high_precedence)

    def brackets_check(string_):
        bracket_stack = deque()
        for elem in string_:
            if elem == "(":
                bracket_stack.append(elem)
            elif elem == ")":
                if len(bracket_stack) == 0:
                    return False
                bracket_stack.pop()
        if len(bracket_stack) != 0:
            return False
        return True

    if not brackets_check(input_str):
        print("Invalid expression")
        raise ValueError

    operator_stack = []
    output_queue = deque()

    input_list = bracket_partition(input_str)

    for token in input_list:
        OPERATORS = {"+", "-", "*", "/"}
        if all(c in string.digits for c in token):
            output_queue.append(token)

        elif token in OPERATORS:
            while (
                    len(operator_stack) > 0 and
                    higher_equal_precedence(operator_stack[-1], token) and
                    operator_stack[-1] != "("
            ):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)

        elif token == "(":
            operator_stack.append(token)

        elif token == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            if operator_stack[-1] == "(":
                operator_stack.pop()
            while len(operator_stack) > 0:
                output_queue.append(operator_stack.pop())

    while len(operator_stack) > 0:
        output_queue.append(operator_stack.pop())
    return " ".join(output_queue)


def calculate(rpn_string):
    def reduce_list(list_, start, end, value):
        return list_[:start] + [value] + list_[end + 1:]

    operators = {"+", "-", "*", "/", "(", ")"}
    rpn_list = rpn_string.split()
    while True:
        if len(rpn_list) == 2:
            print("Invalid expression")
            raise ValueError
        if len(rpn_list) == 1:
            return rpn_list[0]

        min_operator_index = min(i for i, char in enumerate(rpn_list) if char in operators)

        first_num_index = min_operator_index - 2
        first_num_value = int(rpn_list[first_num_index])
        second_num_index = min_operator_index - 1
        second_num_value = int(rpn_list[second_num_index])

        if rpn_list[min_operator_index] == "+":
            result = first_num_value + second_num_value
            rpn_list = reduce_list(rpn_list, first_num_index, min_operator_index, result)
        elif rpn_list[min_operator_index] == "-":
            result = first_num_value - second_num_value
            rpn_list = reduce_list(rpn_list, first_num_index, min_operator_index, result)
        elif rpn_list[min_operator_index] == "*":
            result = first_num_value * second_num_value
            rpn_list = reduce_list(rpn_list, first_num_index, min_operator_index, result)
        elif rpn_list[min_operator_index] == "/":
            result = first_num_value / second_num_value
            rpn_list = reduce_list(rpn_list, first_num_index, min_operator_index, result)


class Calculator:
    def __init__(self):
        self.var_dictionary = dict()
        self.known_operators = {"+", "-", "*", "/", "(", ")"}

    def change_var_dictionary(self, key, value):
        if not all(c in string.ascii_lowercase for c in key):
            print("Invalid identifier")
            raise KeyError
        self.var_dictionary[key] = value

    def read_var_dictionary(self, key):
        if key in self.var_dictionary:
            return self.var_dictionary[key]
        else:
            print("Unknown variable")
            raise KeyError

    def get_values(self, string_):
        elem_list = bracket_partition(string_)
        for i, n in enumerate(elem_list):
            # If it's bracket
            if n == "(" or n == ")":
                continue
            # If it's an operator
            elif all(c in self.known_operators for c in n):
                # Only + and - operators
                if n.count("+") + n.count("-") == len(n):
                    elem_list[i] = "+" if n.count("-") % 2 == 0 else "-"
                elif len(n) != 1:
                    print("Invalid expression")
                    raise ValueError
                continue
            # If it's a number
            elif all(c in string.digits for c in n):
                continue
            # If it's a variable name
            elif all(c.lower() in string.ascii_lowercase for c in n):
                elem_list[i] = str(self.read_var_dictionary(n))
            # If it's neither
            else:
                print("Invalid identifier")
                raise KeyError
        return " ".join(elem_list)

    def process_input(self):
        input_ = input().strip()
        if len(input_) == 0:
            return
        if input_.startswith("/"):
            if input_ == "/exit":
                print("Bye!")
                exit()
            if input_ == "/help":
                print("The program calculates the sum or the difference of given numbers")
                print("""Type:
                    /exit to finish execution of the programme
                    a + b to sum integer numbers a and b
                    a - b to subtract integer numbers a and b""")
                return
            else:
                print("Unknown command")
                return
        # Get variable's value
        if all(c.lower() in string.ascii_lowercase for c in input_):
            print(self.read_var_dictionary(input_))
            return
        # Perform a calculation
        if "=" not in input_:
            input_str = self.get_values(input_)
            rpn_string = reverse_polish_notation(input_str)
            print(calculate(rpn_string))
            return
        # Change or create a variable
        else:
            if input_.count("=") > 1:
                print("Invalid expression")
                raise ValueError

            equal_sign_index = input_.index("=")
            var_name = input_[:equal_sign_index].strip()
            var_value = self.get_values(input_[equal_sign_index + 1:].strip())
            var_value = calculate(reverse_polish_notation(var_value))
            self.change_var_dictionary(var_name, var_value)
            return


calc = Calculator()
while True:
    try:
        calc.process_input()
    except KeyError:
        continue
    except ValueError:
        continue
