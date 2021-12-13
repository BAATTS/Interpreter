import re
import sys

stack = []
input_arg = sys.argv[1]
out_arg = sys.argv[2]
text_file = open(input_arg, "r")
file = open(out_arg, "a")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[0]

    def parse(self):
        tree = self.expression()
        tree.preorder_print(tree)
        return tree

    def consume_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def expression(self):
        tree = self.term()
        while self.current_token.op == 'add':
            token = self.current_token
            self.consume_token()
            right = self.term()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def term(self):
        tree = self.factor()
        while self.current_token.op == 'sub':
            token = self.current_token
            self.consume_token()
            right = self.factor()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def factor(self):
        tree = self.piece()
        while self.current_token.op == 'div':
            token = self.current_token
            self.consume_token()
            right = self.piece()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def piece(self):
        tree = self.element()
        while self.current_token.op == 'mult':
            token = self.current_token
            self.consume_token()
            right = self.element()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def element(self):
        if self.current_token.type == 'Number':
            token = self.current_token
            self.consume_token()
            endNode = Node(None, token.value, None, None)
            endNode.type = 'Number'
            return endNode

        elif self.current_token.type == 'Identifier':
            token = self.current_token
            self.consume_token()
            endNode = Node(None, token.value, None, None)
            endNode.type = 'Identifier'
            return endNode

        if self.current_token.value == '(':
            self.consume_token()
            tree = self.expression()
            if self.current_token.value == ')':
                self.consume_token()
                return tree

    def statement(self):
        tree = self.baseStatement()
        while self.current_token.value == ';':
            token = self.current_token
            self.consume_token()
            right = self.baseStatement()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def baseStatement(self):
        if self.current_token.type == 'Identifier':
            tree = self.assignment()
            return tree
        elif self.current_token.value == 'if':
            tree = self.ifStatement()
            return tree
        elif self.current_token.value == 'while':
            tree = self.whileStatement()
            return tree
        elif self.current_token.value == 'skip':
            self.consume_token()
            return Node(None, self.current_token.value, None, None)
        else:
            print('Exception')

    def assignment(self):
        if self.current_token.type == 'Identifier':
            token1 = self.current_token
            temp = Node(None, token1.value, None, None)
            temp.type = 'Identifier'
            self.consume_token()
            if self.current_token.value == ':=':
                token = self.current_token
                self.consume_token()
                tree = self.expression()
                node = Node(temp, token.value, tree, None)
                node.type = 'Punctuation'
                return node
            else:
                print('Exception')
        else:
            print('Exception')

    def ifStatement(self):
        if self.current_token.value == 'if':
            temp = self.current_token
            self.consume_token()
            tree1 = self.expression()
            if self.current_token.value == 'then':
                self.consume_token()
                tree2 = self.statement()
                if self.current_token.value == 'else':
                    self.consume_token()
                    tree3 = self.statement()
                    if self.current_token.value == 'endif':
                        self.consume_token()
                        return Node(tree1, temp.value, tree2, tree3)
                    else:
                        print('Exception')
                else:
                    print('Exception')
            else:
                print('Exception')
        else:
            print('Exception')

    def whileStatement(self):
        if self.current_token.value == 'while':
            self.consume_token()
            tree1 = self.expression()
            if self.current_token.value == 'do':
                self.consume_token()
                tree2 = self.statement()
                if self.current_token.value == 'endwhile':
                    self.consume_token()
                    return Node(tree1, 'WHILE LOOP', tree2, None)
                else:
                    print('Exception')
            else:
                print('Exception')
        else:
            print('Exception')


class Node:
    def __init__(self, left, value, right, middle):
        self.value = value
        self.left = left
        self.right = right
        self.middle = middle
        self.type = None

    def print(self):
        print(self.value, ':')

    def preorder_print(self, tree, level=0):
        if tree is None:
            return
        else:
            for n in range(level):
                print("\t", end="", file=file)

            if tree.type is not None:
                print(tree.value, ':', tree.type, file=file)
            else:
                print(tree.value, file=file)
            if tree.left is not None:
                self.preorder_print(tree.left, level + 1)
            if tree.middle is not None:
                self.preorder_print(tree.middle, level + 1)
            if tree.right is not None:
                self.preorder_print(tree.right, level + 1)


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.op = None

    def info(self):
        print(self.value, " : ", self.type, file=file)


class Evaluator:
    def __init__(self):
        self.stack = []
        self.root = None

    def printEval(self):
        print("\nEVALUATION\n", file=file)

        print("\nOutput:", int(self.stack[0].value), file=file)

        print("\n\n", file=file)

    def eval(self, root):
        self.stack.append(root)
        print(self.stack[0].value)
        if len(self.stack) >= 3:
            while len(self.stack) >= 3 and self.stack[-1].type == "Number" and self.stack[-2].type == "Number" and \
                    self.stack[
                        -3].type == "Punctuation":
                num1 = self.stack.pop()
                num2 = self.stack.pop()
                punct = self.stack.pop()

                if punct.value == '+':
                    result = int(num2.value) + int(num1.value)
                    node = Node(None, result, None, None)
                    node.type = "Number"
                    self.stack.append(node)

                elif punct.value == '-':
                    result = int(num2.value) - int(num1.value)
                    node = Node(None, result, None, None)
                    node.type = "Number"
                    self.stack.append(node)

                elif punct.value == '*':
                    result = int(num2.value) * int(num1.value)
                    node = Node(None, result, None, None)
                    node.type = "Number"
                    self.stack.append(node)

                elif punct.value == '/':
                    if int(num1.value) == 0:
                        print("Exception: Division by zero")
                        return
                    result = int(num2.value) / int(num1.value)
                    node = Node(None, result, None, None)
                    node.type = "Number"
                    self.stack.append(node)

        if root.left is None:
            return
        self.eval(root.left)
        if root.right is None:
            return
        self.eval(root.right)


number_tokens = re.compile("^[0-9]+$")
identifier_tokens = re.compile("^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*$")
punctuation_tokens = re.compile("^(\+|\-|\*|/|\)|\(|:=|;)$")
keyword_tokens = re.compile("^(if|then|else|endif|while|do|endwhile|skip)$")


def main():
    token_list = []
    for line in text_file:
        line = line.strip(' ')
        print("Line:", line, file=file)
        words = line.split()
        for token in words:
            temp = []
            string = ''
            for char in token:
                temp.append(char)
                holder = string.join(temp)
                id_result = re.match(identifier_tokens, holder)
                num_result = re.match(number_tokens, holder)
                punc_result = re.match(punctuation_tokens, holder)
                key_result = re.match(keyword_tokens, holder)
                if (id_result is None) & (num_result is None) & (punc_result is None) & (key_result is None) & (
                        len(holder) != 1):
                    back = token[len(holder) - 1:]
                    front = token[0:len(holder) - 1]
                    words.insert(words.index(token), front)
                    words.insert(words.index(token), back)
                    words.remove(token)
                    break
        for token in words:
            num_result = re.match(number_tokens, token)
            id_result = re.match(identifier_tokens, token)
            punc_result = re.match(punctuation_tokens, token)
            key_result = re.match(keyword_tokens, token)

            if key_result is not None:
                token_list.append(Token(token, "keyword"))
            elif id_result is not None:
                token_list.append(Token(token, "Identifier"))
            elif num_result is not None:
                token_list.append(Token(token, "Number"))
            elif punc_result is not None:
                if token == '+':
                    tok = Token(token, "Punctuation")
                    tok.op = 'add'
                    token_list.append(tok)
                elif token == '-':
                    tok = Token(token, "Punctuation")
                    tok.op = 'sub'
                    token_list.append(tok)
                elif token == '*':
                    tok = Token(token, "Punctuation")
                    tok.op = 'mult'
                    token_list.append(tok)
                elif token == '/':
                    tok = Token(token, "Punctuation")
                    tok.op = 'div'
                    token_list.append(tok)
                elif token == '(':
                    tok = Token(token, "Punctuation")
                    tok.op = 'leftP'
                    token_list.append(tok)
                elif token == ')':
                    tok = Token(token, "Punctuation")
                    tok.op = 'rightP'
                    token_list.append(tok)
                elif token == ':=':
                    tok = Token(token, "Punctuation")
                    tok.op = 'equal'
                    token_list.append(tok)
                elif token == ';':
                    tok = Token(token, "Punctuation")
                    tok.op = 'semi'
                    token_list.append(tok)

            else:
                print("Error reading:'", token, "'", file=file)
                break

    print("Tokens:", file=file)
    for token in token_list:
        token.info()
    print("\n", file=file)

    print("\nAST\n", file=file)

    parser_obj = Parser(token_list)
    tree = parser_obj.parse()

    holder = Evaluator()
    holder.root = tree
    holder.eval(tree)
    holder.printEval()

    text_file.close()
    file.close()


if __name__ == '__main__':
    main()
