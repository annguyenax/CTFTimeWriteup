code = '++++++++++[>+++++>+++++++++++>++++++++>+++++++<<<<-]>>>----.---.+++++++++++.>---.<.>+++.<<+++++++++++++.-------.-----------.----------.+++++.+++++.-----.-----.+++++++++++++++++++.+++.------.++++++++++.>+++++++++++.<<.+.+.>-------.--------.+++++++++++++.>++.+++.+++++++++++.<<.>>------.<<-.>++++++.'

tape = [0] * 30000
ptr = 0
out = ''
i = 0
loops = {}
stack = []
for idx, c in enumerate(code):
    if c == '[': stack.append(idx)
    elif c == ']':
        start = stack.pop()
        loops[start] = idx
        loops[idx] = start

while i < len(code):
    c = code[i]
    if c == '>': ptr += 1
    elif c == '<': ptr -= 1
    elif c == '+': tape[ptr] = (tape[ptr] + 1) % 256
    elif c == '-': tape[ptr] = (tape[ptr] - 1) % 256
    elif c == '.': out += chr(tape[ptr])
    elif c == '[':
        if tape[ptr] == 0: i = loops[i]
    elif c == ']':
        if tape[ptr] != 0: i = loops[i]
    i += 1

print('FLAG:', out)
