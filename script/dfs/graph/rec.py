# dfs再帰あり
# 低速、TLE可能性あり

import sys
sys.setrecursionlimit(10**6)

def dfs(u):
    seen[u] = True
    for v in G[u]:
        if seen[v]:
            continue
        dfs(v)

N, M = map(int, input().split())
S = int(input()) - 1

G = [[] for _ in range(N)]

for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    G[u].append(v)
    G[v].append(u)

seen = [False] * N
dfs(S)