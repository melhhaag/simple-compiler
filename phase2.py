def semantic_analysis(tokens):
    errors = []
    i = 0
    operators = {'+', '-', '*', '/', '=', '==', '!=', '>', '<', '>=', '<=', '+=', '-=', '*=', '/='}
    brace_stack = []
    declared_variables = set()

    while i < len(tokens):
        token = tokens[i]

        if token[0] == 'VARIABLE':
            if token[1] not in declared_variables:
                if i == 0 or tokens[i - 1][0] != 'IDENTIFIER':
                    errors.append(f"Variable {token[1]} must have an identifier before it")
                else:
                    declared_variables.add(token[1])
            
        if token[0] == 'IDENTIFIER':
            if i + 1 < len(tokens) and tokens[i + 1][0] == 'VARIABLE':
                declared_variables.add(tokens[i + 1][1])

        if token[0] == 'VALUE':
            if i + 1 < len(tokens) and (tokens[i + 1][0] != 'SYMBOL' or tokens[i + 1][1] not in {',', ';', ']', ')'}):
                errors.append(f"Number {token[1]} must be followed by a valid symbol")

        if token[0] == 'RESERVED_WORD' and token[1] in {'for', 'while', 'if'}:
            if i + 1 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == '(':
                i += 1
                while i + 1 < len(tokens) and not (tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == ')'):
                    i += 1
                if i + 1 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == ')':
                    i += 1
                    if i + 1 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == '{':
                        brace_stack.append('{')
                        i += 1
                    else:
                        while i + 1 < len(tokens) and tokens[i + 1][0] != 'SYMBOL':
                            i += 1
                else:
                    errors.append(f"Expected ')' after condition in {token[1]}")
            else:
                errors.append(f"Expected '(' after {token[1]}")

        if token[0] == 'RESERVED_WORD' and token[1] == 'do':
            if i + 1 < len(tokens) and tokens[i + 1][0] == 'SYMBOL' and tokens[i + 1][1] == '{':
                brace_stack.append('{')
                i += 1
            else:
                errors.append(f"Expected '{{' after 'do' statement")
            i += 1
            while i < len(tokens) and not (tokens[i][0] == 'RESERVED_WORD' and tokens[i][1] == 'while'):
                i += 1
            if i >= len(tokens) or tokens[i][0] != 'RESERVED_WORD' or tokens[i][1] != 'while':
                errors.append("Expected 'while' after 'do' block")
            i += 1
            if i < len(tokens) and tokens[i][0] == 'SYMBOL' and tokens[i][1] == '(':
                i += 1
                while i < len(tokens) and not (tokens[i][0] == 'SYMBOL' and tokens[i][1] == ')'):
                    i += 1
                if i < len(tokens) and tokens[i][0] == 'SYMBOL' and tokens[i][1] == ')':
                    i += 1
                else:
                    errors.append("Expected ')' after 'while' condition")
            else:
                errors.append("Expected '(' after 'while' in 'do-while' loop")
            if i < len(tokens) and tokens[i][0] == 'SYMBOL' and tokens[i][1] == ';':
                i += 1
            else:
                errors.append("Expected ';' after 'while' condition in 'do-while' loop")

        if token[0] == 'SYMBOL':
            if token[1] == '{':
                brace_stack.append('{')
            elif token[1] == '}':
                if brace_stack:
                    brace_stack.pop()
                else:
                    errors.append("Unmatched '}' found")

        i += 1

    if brace_stack:
        errors.append("Unmatched '{' found")

    return errors
