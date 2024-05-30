IDENTIFIERS = ['int', 'float', 'string', 'double', 'bool', 'char']
OPERATORS = ['+', '-', '*', '/', '%', '==', '++', '--', '=', '+=', '-=', '*=', '/=']
SYMBOLS = ['(', ')', '[', ']', '{', '}', ',', ';', '>', '<', '!', '==']
RESERVED_WORDS = ['for', 'while', 'if', 'do', 'return', 'break', 'continue', 'end', 'else']

def is_reserved_word(word):
    return word in RESERVED_WORDS

def is_identifier(word):
    return word in IDENTIFIERS

def is_operator(char):
    return char in OPERATORS

def is_symbol(char):
    return char in SYMBOLS

def is_numeric(char):
    return char.isdigit()

def tokenize(code):
    tokens = []
    i = 0
    inside_list = False
    while i < len(code):
        char = code[i]

        if char.isspace():
            i += 1
            continue

        # Check for multi-character operators first
        if i < len(code) - 1:
            next_char = code[i + 1]
            two_char_operator = char + next_char
            if two_char_operator in OPERATORS:
                tokens.append(('OPERATOR', two_char_operator))
                i += 2
                continue

        if is_symbol(char):
            tokens.append(('SYMBOL', char))
            if char == '[':
                inside_list = True
            if char == ']':
                inside_list = False
            i += 1
            continue

        if is_operator(char):
            tokens.append(('OPERATOR', char))
            i += 1
            continue

        if is_numeric(char):
            start = i
            while i < len(code) and (code[i].isdigit() or code[i] == '.'):
                i += 1
            number = code[start:i]
            if inside_list:
                tokens.append(('VALUE IN THE LIST', number))
            else:
                tokens.append(('VALUE', number))
            continue

        if char.isalpha():
            start = i
            while i < len(code) and (code[i].isalpha() or code[i].isdigit() or code[i] == '_'):
                i += 1
            word = code[start:i]
            if is_reserved_word(word):
                tokens.append(('RESERVED_WORD', word))
            elif is_identifier(word):
                tokens.append(('IDENTIFIER', word))
            else:
                tokens.append(('VARIABLE', word))
            continue

        tokens.append(('UNKNOWN', char))
        i += 1

    return tokens
