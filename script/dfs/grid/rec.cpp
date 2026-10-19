// dfs再帰あり

#include <iostream>
#include <vector>
#include <string>
#include <tuple>

constexpr int dr[4] = {0, -1, 1, 0};
constexpr int dc[4] = {-1, 0, 0, 1};
int H, W;
std::vector<std::string> grid(0);
std::vector<std::vector<bool>> seen(0, std::vector<bool>(0, false));

void dfs(int r, int c) {
    seen[r][c] = true;
    for (int i=0; i<4; ++i) {
        int nr = r+dr[i];
        int nc = c+dc[i];
        if (nr < 0 || nr >= H || nc < 0 || nc >= W) continue;
        if (grid[nr][nc] == '#') continue;
        if (seen[nr][nc]) continue;
        dfs(nr, nc);
    }
}

int main() {
    std::cin >> H >> W;
    int sr, sc;
    std::cin >> sr >> sc;
    sr -= 1;
    sc -= 1;
    grid.resize(H);
    seen.resize(H);
    for (int i=0; i<H; ++i) {
        std::cin >> grid[i];
        seen[i].resize(W);
    }

    dfs(sr, sc);
}