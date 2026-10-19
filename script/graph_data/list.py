# 無向グラフの隣接リスト

N, M = map(int, input().split())

G = [[] for _ in range(N)]

for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    G[u].append(v)
    G[v].append(u)