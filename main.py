# Programmer: Jorge Zepeda
# Phase 1.2


import re
import sys


# Open the fie passed in and read line by line
def openfile():
    with open(sys.argv[1], 'r') as file:
        f = file.readlines()
        return f


# Detecting the identifiers
def identifiers(filewriter, token):
    identifiers_regex = "[a-zA-Z][a-zA-Z0-9]*"

    match = re.findall(identifiers_regex, token)

    if match:
        filewriter.write(match[0] + " :IDENTIFIER " + "\n")
        return match[0]
    else:
        return ''


# Detecting the numbers
def numbers(filewriter, token):
    numbers_regex = "[0-9]+"

    match = re.findall(numbers_regex, token)

    if match:
        filewriter.write(match[0] + " :NUMBER " + "\n")
        return match[0]
    else:
        return ''


# Detecting the symbols
def symbols(filewriter, token):
    symbols_regex = "\\+ | \\- | \\* | \\/ | \\( | \\) | \\:= | \\;"

    match = re.findall(symbols_regex, token)

    if match:
        filewriter.write(match[0] + " :SYMBOL " + "\n")
        return match[0]
    else:
        return ''


# Detecting the keywords
def keywords(filewriter, token):
    keywords_regex = "if|then|else|endif|while|do|endwhile|skip"

    match = re.fullmatch(keywords_regex, token)

    if match:
        filewriter.write(match[0] + " :KEYWORD" + "\n")
        return match[0]
    else:
        return ''


# Searches through all language
def search(filewriter, token):
    if keywords(filewriter, token) == '':
        identifiers(filewriter, token)
    numbers(filewriter, token)
    symbols(filewriter, token)


if __name__ == '__main__':
    file = openfile()
    filewriter = open(sys.argv[2], 'w')
    errorTokens = re.compile('[.@_!#$%^&<>?}{~]')

    for line in file:
        line = line.strip()
        filewriter.write("\n")
        filewriter.write("line: " + line + "\n")
        token_list = line.split(" ")

        for token in token_list:
            if errorTokens.search(token) is not None:
                search(filewriter, token)
                filewriter.write(f'ERROR TOKEN: "{errorTokens.search(token)[0]}"')
                filewriter.write("\n")
                break
            else:
                search(filewriter, token)

