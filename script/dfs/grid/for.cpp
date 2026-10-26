// グリッドdfs再帰なし

#include <iostream>
#include <vector>
#include <string>
#include <tuple>

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
    std::vector<std::vector<bool>> seen(H, std::vector<bool>(W, false));
    seen[sr][sc] = true;

    std::vector<std::pair<int, int>> que = {{sr, sc}};
    while (que.size()) {
        auto [r, c] = que[que.size()-1];
        que.pop_back();
        for (int i=0; i<4; ++i) {
            int nr = r+dr[i];
            int nc = c+dc[i];
            if (nr < 0 || nr >= H || nc < 0 || nc >= W) continue;
            if (grid[nr][nc] == '#') continue;
            if (seen[nr][nc]) continue;
            que.push_back({nr, nc});
            seen[nr][nc] = true;
        }
    }
}