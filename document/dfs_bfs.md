# AtCoderのための DFS / BFS 重点攻略ガイド

競技プログラミング（特にAtCoder）のABC・ARC帯で最も差がつく「深さ優先探索 (DFS)」と「幅優先探索 (BFS)」に絞り込んだ完全解説・パターン別リファレンスです。

---

## 目次
1. [DFSとBFSの基本比較](#1-dfsとbfsの基本比較)
2. [深さ優先探索 (DFS) のパターンと実装](#2-深さ優先探索-dfs-のパターンと実装)
3. [幅優先探索 (BFS) のパターンと実装](#3-幅優先探索-bfs-のパターンと実装)
4. [応用・派生アルゴリズム](#4-応用派生アルゴリズム)
5. [問題分類と解法選択チェックリスト](#5-問題分類と解法選択チェックリスト)

---

## 1. DFSとBFSの基本比較

| アルゴリズム | 構造 | 主なデータ構造 | 主な用途・得意分野 | 計算量 |
|---|---|---|---|---|
| **深さ優先探索 (DFS)** | 縦に深く | スタック / 再帰関数 | 連結成分カウント、行き止まりチェック、木の探索 | $O(V + E)$ |
| **幅優先探索 (BFS)** | 横に広く | キュー (`std::queue`) 先入れ先出し / FIFO | **重みなしグラフ・グリッドの最短距離** | $O(V + E)$ |
| **0-1 BFS** | コスト順 | 両端キュー (`std::deque`) | **辺の重みが $0$ か $1$ の最短距離** | $O(V + E)$ |

---

## 2. 深さ優先探索 (DFS) のパターンと実装

### 1. グリッド上の連結成分カウント（島Countingなど）
- **ポイント**: 探索済みマスを記録する `seen` 配列（または直接マップを塗りつぶす）を利用し、未訪問のマスからのみDFSを開始する。

```python
import sys

# 再帰深度の上限を変更（DFSで必須）
sys.setrecursionlimit(10**6)

H, W = 0, 0
grid = []
seen = []

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]


def dfs(h: int, w: int) -> None:
    seen[h][w] = True

    for dir_idx in range(4):
        nh = h + dx[dir_idx]
        nw = w + dy[dir_idx]

        # 範囲外チェック
        if nh < 0 or nh >= H or nw < 0 or nw >= W:
            continue
        # 壁チェック
        if grid[nh][nw] == "#":
            continue
        # 訪問済みチェック
        if seen[nh][nw]:
            continue

        dfs(nh, nw)


# --- 使用例 ---
# H, W = map(int, input().split())
# grid = [input() for _ in range(H)]
# seen = [[False] * W for _ in range(H)]
# dfs(start_h, start_w)
```

```cpp
int H, W;
vector<string> grid;
vector<vector<bool>> seen;

int dx[4] = {1, 0, -1, 0};
int dy[4] = {0, 1, 0, -1};

void dfs(int h, int w) {
    seen[h][w] = true;
    for (int dir = 0; dir < 4; ++dir) {
        int nh = h + dx[dir];
        int nw = w + dy[dir];
        if (nh < 0 || nh >= H || nw < 0 || nw >= W) continue;
        if (grid[nh][nw] == '#') continue; // 壁
        if (seen[nh][nw]) continue; // 訪問済み
        dfs(nh, nw);
    }
}
```

### 2. 二部グラフ判定
- **ポイント**: 頂点を2色（1 と -1）で塗り分けられるか判定する。隣接頂点が同じ色なら二部グラフではない。
- **実装方法**: DFSで頂点を塗り分けながら、隣接頂点の色をチェックする。
- **使用例**: グラフに奇数長のサイクルが含まれるかを判定する問題、マッチング問題の前処理など。
- **問題例**: [ABC 472 - E - Odd Cycle](https://atcoder.jp/contests/abc472/tasks/abc472_e)

---

## 3. 幅優先探索 (BFS) のパターンと実装

### 1. グリッド上の最短経路 (基本テンプレート)
- **ポイント**: 始点からの距離を保持する `dist` 配列を用意し、未訪問（`dist == -1`）のマスに順次最短距離を設定していく。

```python
from collections import deque

# 入力受取・変数定義（例）
# H, W = map(int, input().split())
# grid = [input() for _ in range(H)]

dist = [[-1] * W for _ in range(H)]
que = deque()

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

# スタート地点の初期化
dist[start_h][start_w] = 0
que.append((start_h, start_w))

while que:
    h, w = que.popleft()  # 先頭から取り出し (O(1))

    for dir_idx in range(4):
        nh = h + dx[dir_idx]
        nw = w + dy[dir_idx]

        # 範囲外チェック
        if nh < 0 or nh >= H or nw < 0 or nw >= W:
            continue
        # 壁チェック
        if grid[nh][nw] == "#":
            continue

        # 未訪問判定
        if dist[nh][nw] == -1:
            dist[nh][nw] = dist[h][w] + 1
            que.append((nh, nw))
```

```cpp
vector<vector<int>> dist(H, vector<int>(W, -1));
queue<pair<int, int>> que;

dist[start_h][start_w] = 0;
que.push({start_h, start_w});

while (!que.empty()) {
    auto [h, w] = que.front();
    que.pop();

    for (int dir = 0; dir < 4; ++dir) {
        int nh = h + dx[dir];
        int nw = w + dy[dir];
        if (nh < 0 || nh >= H || nw < 0 || nw >= W) continue;
        if (grid[nh][nw] == '#') continue;

        if (dist[nh][nw] == -1) {
            dist[nh][nw] = dist[h][w] + 1;
            que.push({nh, nw});
        }
    }
}
```

### 2. 0-1 BFS
- **概要**: 移動コストが $0$ と $1$ の2種類混在するグリッド・グラフで使用。
- **実装ルール**: コスト $0$ の移動は **`push_front`**、コスト $1$ の移動は **`push_back`** を使用する。

---

## 4. 応用・派生アルゴリズム

### 1. 復元処理（最短経路のパス復元）
- 各頂点（マス）に「どこから来たか」を保持する `prev` 配列を書き込むことで、ゴールから逆トラバースして経路を再現する。

### 2. 多始点BFS (Multi-source BFS)
- **概要**: 複数のスタート地点（例: 複数のモンスターから最も近い安全地帯など）からの最小距離を一度に求める。
- **実装方法**: 最初（`while` ループ開始前）に**すべての始点をキューに入れて距離 $0$ にセット**してから探索を開始する。

### 3. グリッドの拡張BFS (状態持ちBFS)
- **概要**: 「鍵を持っているか」「向き変更回数」など、位置 $(h, w)$ 以外の情報も状態に組み込む。
- **配列定義例**: `dist[h][w][has_key]` のように次元を1つ増やして管理する。

---

## 5. 問題分類と解法選択チェックリスト

```
【問題文に「最小手数」「最短距離」のキーワードがあるか？】
  ├─ Yes ─┬─ 辺のコストがすべて等しい (1) ──> 通常の BFS
  │       ├─ 辺のコストが 0 または 1 ──> 0-1 BFS
  │       └─ 辺のコストが正の実数/整数 ──> ダイクストラ法
  │
  └─ No  ─┬─ 連結か判定 / 連結成分の個数 ──> DFS または BFS (どちらでも可)
          ├─ 条件を満たす全ルートの探索 / バックトラック ──> DFS
          └─ サイクル検出 / 二部グラフ判定 ──> DFS
```
