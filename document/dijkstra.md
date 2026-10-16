# AtCoderのための ダイクストラ法 完全攻略ガイド

競技プログラミング（特にAtCoder）で頻出となる「ダイクストラ法 (Dijkstra's Algorithm)」の基本概念、計算量、実装テンプレート、および他アルゴリズムとの使い分けをまとめたリファレンスガイドです。

---

## 目次
1. [ダイクストラ法とは](#1-ダイクストラ法とは)
2. [アルゴリズムの仕組みと計算量](#2-アルゴリズムの仕組みと計算量)
3. [実装テンプレート (C++ / Python)](#3-実装テンプレート-c--python)
4. [BFS / 0-1 BFS / ダイクストラ法の使い分け](#4-bfs--0-1-bfs--ダイクストラ法の使い分け)
5. [注意点（負の辺・定数倍高速化）](#5-注意点)

---

## 1. ダイクストラ法とは

グラフ上の単一の始点から、他のすべての頂点への**最短距離**を求めるアルゴリズムです。

- **適用条件**: 辺の重み（移動コスト）がすべて **非負（0以上）** であること。
- **データ構造**: 優先度付きキュー（`std::priority_queue` / `heapq`）を使用して効率化します。

---

## 2. アルゴリズムの仕組みと計算量

### 手順
1. **初期化**: 始点の距離を `0`、それ以外の全頂点の距離を `INF`（無限大）に設定します。
2. **最小値の取り出し**: 優先度付きキューから、現在判明している距離が最も近い未確定の頂点 `u` を取り出します。
3. **緩和 (Relaxation)**: 頂点 `u` から伸ばせる隣接頂点 `v` に対し、`dist[u] + cost(u, v) < dist[v]` であれば距離を更新し、キューに追加します。
4. **繰り返し**: キューが空になるまで上記を繰り返します。

### 計算量
- **時間計算量**: **$O((V + E) \log V)$** （$V$: 頂点数、$E$: 辺の数）
- **空間計算量**: **$O(V + E)$** （隣接リストと距離配列）

---

## 3. 実装テンプレート (C++ / Python)

### C++17

```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;

struct Edge {
    int to;
    long long cost;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, start;
    if (!(cin >> N >> M >> start)) return 0;

    vector<vector<Edge>> G(N);
    for (int i = 0; i < M; ++i) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        G[u].push_back({v, w});
        // G[v].push_back({u, w}); // 無向グラフの場合はこの行を追加
    }

    vector<long long> dist(N, INF);
    // (距離, 頂点) のペアを昇順（最小ヒープ）で管理
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        // 記録されている距離より大きい場合は不要な要素としてスキップ
        if (d > dist[u]) continue;

        for (const auto& edge : G[u]) {
            if (dist[u] + edge.cost < dist[edge.to]) {
                dist[edge.to] = dist[u] + edge.cost;
                pq.push({dist[edge.to], edge.to});
            }
        }
    }

    return 0;
}
```

### Python 3

```python
import heapq
import sys


def main():
    input = sys.stdin.read
    data = input().split()

    if not data:
        return

    N = int(data[0])
    M = int(data[1])
    start = int(data[2])

    G = [[] for _ in range(N)]
    idx = 3
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx + 1])
        w = int(data[idx + 2])
        idx += 3
        G[u].append((v, w))
        # G[v].append((u, w)) # 無向グラフの場合はこの行を追加

    INF = float("inf")
    dist = [INF] * N
    pq = []

    dist[start] = 0
    heapq.heappush(pq, (0, start))  # (距離, 頂点) の順で格納

    while pq:
        d, u = heapq.heappop(pq)

        # 記録されている距離より大きい場合は不要な要素としてスキップ
        if d > dist[u]:
            continue

        for v, cost in G[u]:
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                heapq.heappush(pq, (dist[v], v))


if __name__ == "__main__":
    main()
```

---

## 4. BFS / 0-1 BFS / ダイクストラ法の使い分け

| アルゴリズム | 辺のコスト | データ構造 | 計算量 |
|---|---|---|---|
| **通常の BFS** | すべて $1$（定数） | `queue` / `deque` | $O(V + E)$ |
| **0-1 BFS** | $0$ または $1$ | `deque` | $O(V + E)$ |
| **ダイクストラ法** | 任意の非負実数・整数 ($\ge 0$) | `priority_queue` / `heapq` | $O((V + E) \log V)$ |

---

## 5. 注意点

- **負の辺がある場合**: ダイクストラ法は正しく動作しません（無限ループや誤解を出力する原因になります）。負の辺が含まれる場合は **ベルマン・フォード法 ($O(VE)$)** を使用します。
- **横着消去 (Lazy Deletion)**: キューから取り出した距離 `d` が最新の `dist[u]` より大きい場合、`continue` で無視する処理が性能上極めて重要になります。
