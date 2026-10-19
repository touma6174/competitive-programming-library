// 無向グラフの隣接行列

#include <iostream>
#include <vector>

int main() {
    int N, M;
    std::cin >> N >> M;
    std::vector<std::vector<bool>> G(N, std::vector<bool>(N, false));
    for (int i=0; i<N; ++i) {
        int u, v;
        std::cin >> u >> v;
        u -= 1;
        v -= 1;
        G[u][v] = true;
        G[v][u] = true;
    }
}