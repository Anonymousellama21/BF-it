import re

def brackets_matched(string, open='[', close=']'):
    depth = 0
    for c in string:
        if c == open:
            depth += 1
        elif c == close:
            if depth == 0:
                return False
            depth -= 1

    return (depth == 0)


def minify(code):
    old_code = ""

    while old_code != code:
        old_code = code

        code = code.replace("><", "")
        code = code.replace("<>", "")
        code = code.replace("+-", "")
        code = code.replace("-+", "")

        code = code.replace("][-]", "]")

        code = code.replace("[]", "") #TODO: check if this is safe. it may break something like a for(;;) depending on how that compiles


        i = 0
        while not code[i] in "<>":
            i += 1
        match_start = i
        match_middle = 0
        while i < len(code):
            while i < len(code) and not code[i] in "<>":
                i += 1

            if i == len(code):
                break

            if brackets_matched(code[match_start+1:i]) and code[i] == "<>"[code[match_start]=='<']:
                match_middle = i
            else:
                match_start = i
                i += 1
                continue

            i += 1

            while not code[i] in "<>":
                i += 1

            if i == len(code):#FIXME: maybe misses something on the end
                break

            if brackets_matched(code[match_middle+1:i]) and code[i] == code[match_start]:
                print(code[match_middle+1:i] + code[match_start] + code[match_start+1:match_middle])
                code = code[:match_start] + code[match_middle+1:i] + code[match_start] + code[match_start+1:match_middle] + code[i+1:]

                i = 0
                while not code[i] in "<>":
                    i += 1
                continue

            else:
                match_start = i
                i += 1

    return code

def strip_unnecessary(code):

    #remove code from the last print to the end

    safe_end = len(code)

    i = len(code)-1
    depth = 0
    while i >= 0:
        if code[i] == ']':
            depth += 1
            i -= 1
            continue

        elif code[i] == '[':
            depth -= 1
            i -= 1
            continue

        elif code[i] == '.':
            break

        if depth == 0:
            safe_end = i

        i -= 1

    code = code[:safe_end]


    #remove code from the beginning

    dot_count = 0

    i = 0
    depth = 0
    while i < len(code):
        if code[i] == '[':
            depth += 1
        elif code[i] == ']':
            depth -= 1

        if depth == 0:

            if code[i] == '.':
                dot_count += 1

            #end at the first io
            if code[i] in ",+-":
                break

        i += 1

    code = "."*dot_count + code[i:]

    return code
