// グラフdfs再帰なし

#include <iostream>
#include <vector>

int main() {
    int N, M, S;
    std::cin >> N >> M >> S;
    --S;
    std::vector<std::vector<int>> G(N, std::vector<int>{});
    for (int i=0; i<M; ++i) {
        int u, v;
        std::cin >> u >> v;
        u -= 1;
        v -= 1;
        G[u].push_back(v);
        G[v].push_back(u);
    }
    
    std::vector<int> que = {S};
    std::vector<bool> seen(N, false);
    while (que.size()) {
        int u = que[que.size() - 1];
        que.pop_back();
        for (int v: G[u]) {
            if (seen[v]) continue;
            que.push_back(v);
            seen[v] = true;
        }
    }
}