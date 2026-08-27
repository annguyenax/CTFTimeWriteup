import sys
sys.path.append(r"c:\users\admin\appdata\roaming\python\python313\site-packages")
from ortools.sat.python import cp_model
import time
import ast
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

with open(r'D:\download\CTFTimeWriteup\UIUCTF2026\crypto\Young Cryptography\files\out', 'r') as f:
    G = ast.literal_eval(f.readline().strip())
    AG = ast.literal_eval(f.readline().strip())
    GB = ast.literal_eval(f.readline().strip())
    iv = ast.literal_eval(f.readline().strip())
    ct = ast.literal_eval(f.readline().strip())

N = 64
n = 256

def my_prod(A, B):
    n = len(A)
    z = (0,) * n
    def f(a, b, c, x):
        return (max(b[0], c[0]) + x,) + tuple(
            min(b[k-1], c[k-1]) + max(b[k], c[k]) - a[k-1]
            for k in range(1, n)
        )
    r = [z] * (n + 1)
    for row in A + B:
        s = [z]
        for j, x in enumerate(row, 1):
            s.append(f(r[j-1], r[j], s[-1], x))
        r = s
    p = [[None] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        p[i][n] = r[i]
    C = [[0] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(n-1, i-1, -1):
            b = p[i][j+1]
            c = p[i+1][j] if i < j else b
            d = p[i+1][j+1]
            C[i][j] = C[j][i] = d[0] - max(b[0], c[0])
            p[i][j] = tuple(
                min(b[k], c[k]) +
                (max(b[k+1], c[k+1]) - d[k+1] if k+1 < n else 0)
                for k in range(n)
            )
    return C

def get_final_r(A, B):
    n = len(A)
    z = (0,) * n
    def f(a, b, c, x):
        return (max(b[0], c[0]) + x,) + tuple(
            min(b[k-1], c[k-1]) + max(b[k], c[k]) - a[k-1]
            for k in range(1, n)
        )
    r = [z] * (n + 1)
    for row in A + B:
        s = [z]
        for j, x in enumerate(row, 1):
            s.append(f(r[j-1], r[j], s[-1], x))
        r = s
    return r

rs_G = [sum(row) for row in G]
rs_AG = [sum(row) for row in AG]
rs_A = [rs_AG[i] - rs_G[i] for i in range(N)]

print("rs_A:", rs_A)

r_AG = get_final_r([[0]*N for _ in range(N)], AG)
target_r = r_AG

model = cp_model.CpModel()
A_vars = [[model.NewIntVar(0, 5, f"A_{i}_{j}") for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        model.Add(A_vars[i][j] == A_vars[j][i])
for i in range(N):
    model.Add(sum(A_vars[i]) == rs_A[i])

M = A_vars + G
z = [0 for _ in range(N)]
r = [z for _ in range(N + 1)]

print("Building model...")
t0 = time.time()
for i_row, row in enumerate(M):
    s_list = [z]
    for j_col, x in enumerate(row, 1):
        a_var = r[j_col-1]
        b_var = r[j_col]
        c_var = s_list[-1]
        
        d_vars = []
        max_b0_c0 = model.NewIntVar(0, 1000, "")
        model.AddMaxEquality(max_b0_c0, [b_var[0], c_var[0]])
        
        d0 = model.NewIntVar(0, 1000, "")
        if isinstance(x, int):
            model.Add(d0 == max_b0_c0 + x)
        else:
            model.Add(d0 == max_b0_c0 + x)
        d_vars.append(d0)
        
        for k in range(1, N):
            min_prev = model.NewIntVar(0, 1000, "")
            model.AddMinEquality(min_prev, [b_var[k-1], c_var[k-1]])
            
            max_curr = model.NewIntVar(0, 1000, "")
            model.AddMaxEquality(max_curr, [b_var[k], c_var[k]])
            
            dk = model.NewIntVar(0, 1000, "")
            if isinstance(a_var[k-1], int):
                model.Add(dk == min_prev + max_curr - a_var[k-1])
            else:
                model.Add(dk == min_prev + max_curr - a_var[k-1])
            d_vars.append(dk)
            
        s_list.append(d_vars)
    r = s_list

# Match r with target_r
for j in range(N + 1):
    for k in range(N):
        model.Add(r[j][k] == target_r[j][k])

print("Model built in", time.time() - t0)
solver = cp_model.CpSolver()
# Enable multi-threading for faster solve
solver.parameters.num_search_workers = 8
solver.parameters.max_time_in_seconds = 3600.0
print("Solving...")
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Found A_prime!")
    A_prime = [[solver.Value(A_vars[i][j]) for j in range(N)] for i in range(N)]
    AGB = my_prod(A_prime, GB)
    
    shared_secret = sha256(str(AGB).encode()).digest()[:16]
    cipher = AES.new(shared_secret, AES.MODE_CBC, iv)
    flag = unpad(cipher.decrypt(ct), 16)
    print("Flag:", flag.decode())
    with open('flag.txt', 'w') as f:
        f.write(flag.decode())
else:
    print("Not found")
