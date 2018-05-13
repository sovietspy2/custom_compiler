from sys import *

def open_file(filename):
    data = open(filename,"r").read()
    return data

def lex(filecontents):
    tok=""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            tok=""
        elif tok==""

def run():
    data = open_file(argv[1])
    lex(data)
run()