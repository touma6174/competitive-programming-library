from collections import deque

H, W = map(int, input().split())
r, c = map(lambda x: int(x)-1, input().split())

grid = [list(input()) for _ in range(H)]
dist = [[-1] * W for _ in range(H)]

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

que = deque()
que.append((r, c))
dist[r][c] = 0

while que:
    r, c = que.popleft()
    for d in range(4):
        nr, nc = r+dr[d], c+dc[d]
        if not (0 <= nr < H and 0 <= nc < W):
            continue
        if grid[nr][nc] == "#":
            continue
        if dist[nr][nc] >= 0:
            continue
        que.append((nr, nc))
        dist[nr][nc] = dist[r][c] + 1
print(dist)