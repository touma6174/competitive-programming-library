// 無向グラフの隣接リスト

#include <iostream>
#include <vector>

int main() {
    int N, M;
    std::cin >> N >> M;
    std::vector<std::vector<int>> G(N, std::vector<int>{});
    for (int i=0; i<N; ++i) {
        int u, v;
        std::cin >> u >> v;
        u -= 1;
        v -= 1;
        G[u].push_back(v);
        G[v].push_back(u);
    }
}