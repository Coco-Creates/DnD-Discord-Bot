import re
import enum
import sys
import operator
import random
import dddatabase
import math


class Node:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.children = []

    def append_number(self, value):
        if sys.maxsize / 10 - value > self.value:
            self.value = self.value * 10 + value


class TokenType(enum.Enum):
    NUM = 0
    PLUS = 1
    MINUS = 2
    MULT = 3
    DIV = 4
    LPAR = 5
    RPAR = 6
    DIE = 7
    END = 8


class ModifierType(enum.IntEnum):
    STR = 0
    DEX = 1
    CON = 2
    WIS = 3
    INT = 4
    CHA = 5


operations = {
    TokenType.PLUS: operator.add,
    TokenType.MINUS: operator.sub,
    TokenType.MULT: operator.mul,
    TokenType.DIV: operator.truediv
}

mappings = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULT,
    '/': TokenType.DIV,
    '(': TokenType.LPAR,
    ')': TokenType.RPAR,
    'd': TokenType.DIE}

modifiers = {
    'STR': ModifierType.STR,
    'DEX': ModifierType.DEX,
    'CON': ModifierType.CON,
    'WIS': ModifierType.WIS,
    'INT': ModifierType.INT,
    'CHA': ModifierType.CHA
}


def score_to_modifier(score):
    return math.floor((score - 10) / 2)


def token_mapping(user, command):
    tokens = []
    stats = None

    x = 0
    while x < len(command):
        character = command[x]
        if character in mappings:
            token_type = mappings[character]
            token = Node(token_type)
            tokens.append(token)
        elif re.match(r'\d', character):
            if len(tokens) > 0 and tokens[-1].token_type == TokenType.NUM:
                tokens[-1].append_number(int(character))
            else:
                token = Node(TokenType.NUM, value=int(character))
                tokens.append(token)
        elif character.isalpha() and x < len(command) - 2:
            mod_str = command[x] + command[x+1] + command[x+2]
            if mod_str in modifiers:
                if stats is None:
                    stats = dddatabase.fetch_character(user.id)
                mod = int(modifiers[mod_str])
                stat_value = stats[mod]
                token = Node(TokenType.NUM, value=score_to_modifier(stat_value))
                tokens.append(token)
                x += 2
            else:
                raise Exception('Invalid token: {}'.format(command))
        else:
            raise Exception('Invalid token: {}'.format(command))
        x += 1
    tokens.append(Node(TokenType.END))
    return tokens


def match(tokens, token):
    if tokens[0].token_type == token:
        return tokens.pop(0)
    else:
        raise Exception('Invalid syntax on token {}'.format(tokens[0].token_type))


def parse_e(tokens):
    left_node = parse_e2(tokens)

    while tokens[0].token_type in [TokenType.PLUS, TokenType.MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens))
        left_node = node

    return left_node


def parse_e2(tokens):
    left_node = parse_e3(tokens)

    while tokens[0].token_type in [TokenType.MULT, TokenType.DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens))
        left_node = node

    return left_node


def parse_e3(tokens):
    left_node = parse_e4(tokens)

    while tokens[0].token_type == TokenType.DIE:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e4(tokens))
        left_node = node

    return left_node


def parse_e4(tokens):
    if tokens[0].token_type == TokenType.NUM:
        return tokens.pop(0)

    match(tokens, TokenType.LPAR)
    expression = parse_e(tokens)
    match(tokens, TokenType.RPAR)

    return expression


def parse(user, command):
    tokens = token_mapping(user, command)
    ast = parse_e(tokens)
    match(tokens, TokenType.END)
    return ast


def compute(node):
    if node.token_type == TokenType.NUM:
        return node.value

    left_result = compute(node.children[0])
    right_result = compute(node.children[1])

    if node.token_type == TokenType.DIE:
        roll_value = 0
        for x in range(left_result):
            roll_value += random.randint(1, right_result)
        return roll_value
    else:
        operation = operations[node.token_type]
        return operation(left_result, right_result)
