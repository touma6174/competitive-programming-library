#include <iostream>
#include <vector>

int N, M;
std::vector<std::vector<int>> G(0, std::vector<int>{});
std::vector<bool> seen(0, false);

void dfs(int u) {
    seen[u] = true;
    for (int v: G[u]) {
        if (seen[v]) continue;
        dfs(v);
    }
}

int main() {
    int S;
    std::cin >> N >> M >> S;
    --S;
    G.resize(N);
    for (int i=0; i<M; ++i) {
        int u, v;
        std::cin >> u >> v;
        u -= 1;
        v -= 1;
        G[u].push_back(v);
        G[v].push_back(u);
    }
    seen.resize(N);

    seen[S] = true;
    dfs(S);
}