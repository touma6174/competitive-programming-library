# dfs再帰なし

H, W = map(int, input().split())
sr, sc = map(lambda x: int(x)-1, input().split())

grid = [list(input()) for _ in range(H)]
seen = [[False] * W for _ in range(H)]

dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]

que = [(sr, sc)]
seen[sr][sc] = True

while que:
    r, c = que.pop()
    for d in range(4):
        nr, nc = r+dr[d], c+dc[d]
        if not (0 <= nr < H and 0 <= nc < W):
            continue
        if grid[nr][nc] == "#":
            continue
        if seen[nr][nc]:
            continue
        que.append((nr, nc))
        seen[nr][nc] = True