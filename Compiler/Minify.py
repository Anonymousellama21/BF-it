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

    return depth == 0


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
        while i < len(code) and (match := re.search(r"<([\-\+\[\]]+)>([\-\+\[\]]+)<", code[i:])):
            if brackets_matched(match.group(1)) and brackets_matched(match.group(2)):
                code = code[:i + match.start()] + match.group(2) + "<" + match.group(1) + code[i + match.end():]
                i += match.end() - 2

            else:
                i += match.end()

    return code
