N, M = map(int, input().split())
S = int(input()) - 1

G = [[] for _ in range(N)]

for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    G[u].append(v)
    G[v].append(u)

que = [S]
seen = [False] * N

while que:
    u = que.pop()
    for v in G[u]:
        if seen[v]:
            continue
        que.append(v)
        seen[v] = True
