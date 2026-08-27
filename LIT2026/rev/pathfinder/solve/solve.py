grid = [[0 for _ in range(36)] for _ in range(36)]

for num_open in range(35, -1, -1):
    for num_close in range(35, -1, -1):
        if num_open < num_close:
            grid[num_open][num_close] = 0
        elif num_open == 35 and num_close == 35:
            grid[num_open][num_close] = 1
        else:
            val = 0
            if num_open < 35:
                val += grid[num_open+1][num_close]
            if num_close < 35 and num_open >= num_close + 1:
                val += grid[num_open][num_close+1]
            grid[num_open][num_close] = val

target = 0x128e740722b291ad
result = ""
num_open = 0
num_close = 0

for i in range(70):
    if num_open < 35:
        num_ways_if_open = grid[num_open + 1][num_close]
    else:
        num_ways_if_open = 0
        
    if target < num_ways_if_open:
        result += "("
        num_open += 1
    else:
        result += ")"
        target -= num_ways_if_open
        num_close += 1

print("Flag: LITCTF{" + result + "}")
