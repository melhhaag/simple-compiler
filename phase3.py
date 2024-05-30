import re

class MemorySimulator:
    def __init__(self):
        self.variables = {}
        self.memory_trace = []

    def execute(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Handle variable declaration and initialization
            if token[0] == 'IDENTIFIER':
                var_type = token[1]
                if i + 1 < len(tokens) and tokens[i + 1][0] == 'VARIABLE':
                    var_name = tokens[i + 1][1]
                    if i + 2 < len(tokens) and tokens[i + 2][0] == 'OPERATOR' and tokens[i + 2][1] == '=':
                        if i + 3 < len(tokens) and tokens[i + 3][0] == 'SYMBOL' and tokens[i + 3][1] == '[':
                            # Handle array initialization
                            array_elements = []
                            j = i + 4
                            while j < len(tokens) and not (tokens[j][0] == 'SYMBOL' and tokens[j][1] == ']'):
                                if tokens[j][0] == 'VALUE':
                                    array_elements.append(int(tokens[j][1]))
                                j += 1
                            self.variables[var_name] = array_elements
                            self.memory_trace.append(f"{var_name} -> {array_elements}")
                            i = j  # Move index to the end of the array declaration
                        else:
                            # Handle normal variable initialization
                            initial_value = self.evaluate_expression(tokens[i + 3:])
                            self.variables[var_name] = initial_value
                            self.memory_trace.append(f"{var_name} -> {initial_value}")
                            i += 3  # Skip past the initialization
            # Handle array element assignment
            elif token[0] == 'VARIABLE' and i + 1 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == '[':
                var_name = token[1]
                if var_name in self.variables and isinstance(self.variables[var_name], list):
                    # Extract array index
                    index_expr = []
                    j = i + 2
                    while j < len(tokens) and tokens[j][0] != 'SYMBOL':
                        index_expr.append(tokens[j][1])
                        j += 1
                    index = eval(''.join(index_expr), {}, self.variables)
                    # Extract new value
                    if j + 2 < len(tokens) and tokens[j + 1][0] == 'OPERATOR' and tokens[j + 1][1] == '=':
                        new_value = self.evaluate_expression(tokens[j + 2:])
                        old_value = self.variables[var_name][index]
                        self.variables[var_name][index] = new_value
                        self.memory_trace.append(f"{var_name}[{index}] -> {old_value} -> {new_value}")
                        i = j + 2  # Skip past the assignment
            # Handle normal variable assignment
            elif token[0] == 'VARIABLE':
                var_name = token[1]
                if i + 1 < len(tokens) and tokens[i + 1][0] == 'OPERATOR' and tokens[i + 1][1] == '=':
                    new_value = self.evaluate_expression(tokens[i + 2:])
                    if var_name in self.variables:
                        old_value = self.variables[var_name]
                        self.variables[var_name] = new_value
                        self.memory_trace.append(f"{var_name} -> {old_value} -> {new_value}")
                    else:
                        self.variables[var_name] = new_value
                        self.memory_trace.append(f"{var_name} -> {new_value}")
                    i += 2  # Skip past the assignment
            # Handle loops (for simplicity, only handling 'for' loops in this example)
            elif token[0] == 'RESERVED_WORD' and token[1] == 'for':
                if i + 6 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == '(':
                    loop_var = tokens[i + 2][1]
                    loop_start = self.evaluate_expression([tokens[i + 4]])
                    loop_end = self.evaluate_expression([tokens[i + 8]])
                    loop_increment = 1  # Simplifying for this example

                    self.variables[loop_var] = loop_start
                    self.memory_trace.append(f"{loop_var} -> {loop_start}")

                    loop_body_start = i + 12  # Adjusting to ensure correct loop body start
                    loop_body_end = self.find_closing_brace(tokens, loop_body_start)

                    while self.variables[loop_var] < loop_end:
                        self.execute(tokens[loop_body_start:loop_body_end])
                        self.variables[loop_var] += loop_increment
                        self.memory_trace.append(f"{loop_var} -> {self.variables[loop_var]}")

                    i = loop_body_end  # Skip past the loop body
            i += 1
        return self.memory_trace

    def evaluate_expression(self, tokens):
        expression = ''
        for token in tokens:
            if token[0] in {'VARIABLE', 'VALUE', 'OPERATOR'}:
                expression += token[1]
            if token[0] == 'SYMBOL' and token[1] in {',', ';', ')', '}', ']'}:
                break
        try:
            result = eval(expression, {}, self.variables)
            if isinstance(result, int) or isinstance(result, float):
                return result
            return int(result) if result.isdigit() else result
        except:
            return expression  # Simplified for this example

    def find_closing_brace(self, tokens, start_index):
        open_braces = 0
        for i in range(start_index, len(tokens)):
            if tokens[i][0] == 'SYMBOL':
                if tokens[i][1] == '{':
                    open_braces += 1
                elif tokens[i][1] == '}':
                    open_braces -= 1
                    if open_braces == 0:
                        return i + 1  # Adjust to skip the closing brace
        return len(tokens)

# Example usage
if __name__ == "__main__":
    tokens = [
        ('IDENTIFIER', 'int'), ('VARIABLE', 'x'), ('OPERATOR', '='), ('SYMBOL', '['),
        ('VALUE', '1'), ('SYMBOL', ','), ('VALUE', '2'), ('SYMBOL', ','), ('VALUE', '3'), ('SYMBOL', ']'), ('SYMBOL', ';'),
        ('VARIABLE', 'x'), ('SYMBOL', '['), ('VALUE', '0'), ('SYMBOL', ']'), ('OPERATOR', '='), ('VALUE', '50'), ('SYMBOL', ';')
    ]

    memory_simulator = MemorySimulator()
    memory_trace = memory_simulator.execute(tokens)
    for trace in memory_trace:
        print(trace)
