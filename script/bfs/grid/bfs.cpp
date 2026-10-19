// dfs再帰なし

#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <queue>

constexpr int dr[4] = {0, -1, 1, 0};
constexpr int dc[4] = {-1, 0, 0, 1};

int main() {
    int H, W;
    std::cin >> H >> W;
    int sr, sc;
    std::cin >> sr >> sc;
    sr -= 1;
    sc -= 1;
    std::vector<std::string> grid(H);
    for (int i=0; i<H; ++i) {
        std::cin >> grid[i];
    }
    std::vector<std::vector<int>> dist(H, std::vector<int>(W, -1));
    dist[sr][sc] = 0;

    std::queue<std::pair<int, int>> que;
    que.push({sr, sc});
    while (que.size()) {
        auto [r, c] = que.front();
        que.pop();
        for (int i=0; i<4; ++i) {
            int nr = r+dr[i];
            int nc = c+dc[i];
            if (nr < 0 || nr >= H || nc < 0 || nc >= W) continue;
            if (grid[nr][nc] == '#') continue;
            if (dist[nr][nc] >= 0) continue;
            que.push({nr, nc});
            dist[nr][nc] = dist[r][c] + 1;
        }
    }

    for (int i=0; i<H; ++i) {
        for (int j=0; j<W; ++j) {
            std::cout << dist[i][j] << " ";
        }
        std::cout << "\n";
    }
}