# AtCoder Library for Python (ac-library-python) 完全攻略ガイド

AtCoder公式が提供する Python 向けライブラリ **`ac-library-python` (`atcoder`)** の正しく完全な仕様および豊富な使用例を網羅したリファレンスガイドです。

---

## 目次
1. [ac-library-python の導入と基本仕様](#1-ac-library-python-の導入と基本仕様)
2. [データ構造 (Data Structures)](#2-データ構造-data-structures)
3. [グラフアルゴリズム (Graph Algorithms)](#3-グラフアルゴリズム-graph-algorithms)
4. [数学・数論アルゴリズム (Math Algorithms)](#4-数学数論アルゴリズム-math-algorithms)
5. [文字列アルゴリズム (String Algorithms)](#5-文字列アルゴリズム-string-algorithms)

---

## 1. ac-library-python の導入と基本仕様

`ac-library-python` は Python の記法に最適化されたラッパーライブラリです。

```python
# 基本的なインポート形式
from atcoder.dsu import DSU
from atcoder.modint import ModContext, Modint
from atcoder.segtree import SegTree
```

---

## 2. データ構造 (Data Structures)

### 1. `atcoder.dsu.DSU` (Union-Find)
要素の結合と、2つの要素が同じグループに属するかを高速に判定します。

* **主なメソッド**:
  * `DSU(n)`: サイズ $n$ で初期化
  * `merge(a, b)`: $a$ と $b$ のグループを結合
  * `same(a, b)`: $a$ と $b$ が同じグループか判定
  * `leader(a)`: $a$ のグループの代表元（親）を返す
  * `size(a)`: $a$ が属するグループの要素数を返す
  * `groups()`: 全グループをリスト（`list[list[int]]`）として取得

* **使用例**:
```python
from atcoder.dsu import DSU

dsu = DSU(5)
dsu.merge(0, 1)
dsu.merge(2, 3)

print(dsu.same(0, 1))  # True
print(dsu.same(0, 2))  # False
print(dsu.size(0))  # 2
print(dsu.groups())  # [[0, 1], [2, 3], [4]]
```

### 2. `atcoder.fenwicktree.FenwickTree` (BIT)
単一要素の更新と、区間和の取得を $O(\log N)$ で行います。

* **主なメソッド**:
  * `FenwickTree(n)`: 長さ $n$ で初期化（全要素 0）
  * `add(p, x)`: `p` 番目の要素に `x` を加算
  * `sum(l, r)`: 半開区間 `[l, r)` の総和を取得

* **使用例**:
```python
from atcoder.fenwicktree import FenwickTree

ft = FenwickTree(5)
ft.add(1, 10)
ft.add(3, 20)

print(ft.sum(0, 4))  # 30 (10 + 20)
print(ft.sum(1, 3))  # 10
```

### 3. `atcoder.segtree.SegTree`
任意のモノイド（結合則を満たす演算と単位元）に対する区間更新・区間クエリを処理します。

* **主なメソッド**:
  * `SegTree(op, e, v_or_n)`: 演算 `op`、単位元 `e`、配列または要素数で初期化
  * `set(p, x)`: `p` 番目の値を `x` に変更
  * `get(p)`: `p` 番目の値を取得
  * `prod(l, r)`: 区間 `[l, r)` の演算結果を計算
  * `all_prod()`: 全区間 `[0, N)` の積を計算
  * `max_right(l, f)` / `min_left(r, f)`: 二分探索による条件 `f` を満たす最遠インデックスの取得

* **使用例（区間最小値 RMQ）**:
```python
from atcoder.segtree import SegTree

# RMQ: op = min, 単位元 = 無限大
st = SegTree(min, float("inf"), [5, 2, 8, 1, 9])

print(st.prod(0, 3))  # 2 (min(5, 2, 8))
st.set(1, 10)  # インデックス1を10に変更
print(st.prod(0, 3))  # 5 (min(5, 10, 8))

# 条件を満たす位置の二分探索 (値が3未満になる最遠位置)
print(st.max_right(0, lambda x: x >= 3))  # 2 (index 3 の 1 で条件崩れ)
```

### 4. `atcoder.lazysegtree.LazySegTree`
「区間更新」と「区間クエリ」の両方を $O(\log N)$ で行います。

* **使用例（区間加算・区間最小値取得）**:
```python
from atcoder.lazysegtree import LazySegTree

# 演算 op: min
op = min
e = float("inf")
# 作用 mapping: 区間値 + 加算値
mapping = lambda f, x: x + f
# 作用素の合成 composition: 加算値 + 加算値
composition = lambda f, g: f + g
# 単位作用素 id: 0
id_ = 0

lst = LazySegTree(op, e, mapping, composition, id_, [1, 2, 3, 4, 5])

# 区間 [1, 4) に 10 を加算
lst.apply_len(1, 4, 10)  # [1, 12, 13, 14, 5] に変更
print(lst.prod(0, 5))  # 1 (最小値)
print(lst.prod(1, 4))  # 12 (12, 13, 14 の最小値)
```

---

## 3. グラフアルゴリズム (Graph Algorithms)

### 1. `atcoder.scc.SCCGraph` (強連結成分分解)
有向グラフを強連結成分分解し、トポロジカルソート順で取得します。

* **使用例**:
```python
from atcoder.scc import SCCGraph

graph = SCCGraph(4)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 0)
graph.add_edge(2, 3)

scc = graph.scc()
print(scc)  # [[0, 1, 2], [3]]
```

### 2. `atcoder.maxflow.MFGraph` (最大流)
* **使用例**:
```python
from atcoder.maxflow import MFGraph

g = MFGraph(4)
g.add_edge(0, 1, 2)
g.add_edge(1, 2, 1)
g.add_edge(0, 2, 1)
g.add_edge(2, 3, 2)

print(g.flow(0, 3))  # 2
```

### 3. `atcoder.mincostflow.MCFGraph` (最小費用流)
* **使用例**:
```python
from atcoder.mincostflow import MCFGraph

g = MCFGraph(4)
# add_edge(from, to, capacity, cost)
g.add_edge(0, 1, 2, 1)
g.add_edge(1, 2, 1, 1)
g.add_edge(0, 2, 2, 3)
g.add_edge(2, 3, 2, 1)

# flow(s, t, flow_limit) -> (流量, 費用)
print(g.flow(0, 3, 2))  # (2, 6)
```

### 4. `atcoder.twosat.TwoSAT` (2-SAT)
* **使用例**:
```python
from atcoder.twosat import TwoSAT

# (x0 or x1) and (not x0 or x1)
ts = TwoSAT(2)
ts.add_clause(0, True, 1, True)
ts.add_clause(0, False, 1, True)

if ts.satisfiable():
    print("SATISFIABLE")
    print(ts.answer())  # [False, True] などの割り当て例
```

---

## 4. 数学・数論アルゴリズム (Math Algorithms)

### 1. `atcoder.modint.ModContext` & `atcoder.modint.Modint`
`ac-library-python` では `ModContext` コンテキストマネージャを使って $\bmod$ を動的に切り替えます。

* **使用例**:
```python
from atcoder.modint import ModContext, Modint

# 998244353 の文脈で計算
with ModContext(998244353):
    a = Modint(10**9 + 7)
    b = Modint(2)
    c = a * b
    print(c.val())  # 1755654

    # 累乗・逆元
    print((a**10).val())
    print(a.inv().val())

# 10^9+7 に切り替えて計算
with ModContext(10**9 + 7):
    x = Modint(10**9 + 6) + Modint(2)
    print(x.val())  # 1
```

### 2. `atcoder.math`
* **使用例**:
```python
import atcoder.math

# 累乗 (x^n mod m)
print(atcoder.math.pow_mod(2, 10, 1000))  # 24

# 逆元 (x * inv = 1 mod m)
print(atcoder.math.inv_mod(3, 7))  # 5 (3 * 5 = 15 ≡ 1 mod 7)

# 中国式余り定理 (CRT): x ≡ r_i (mod m_i)
r = [2, 3]
m = [3, 5]
rem, mod = atcoder.math.crt(r, m)
print(f"x ≡ {rem} (mod {mod})")  # x ≡ 8 (mod 15)

# floor_sum: sum_{i=0}^{n-1} floor((a*i + b) / m)
print(atcoder.math.floor_sum(6, 5, 3, 2))  # 8
```

### 3. `atcoder.convolution.convolution` (畳み込み)
* **使用例**:
```python
from atcoder.convolution import convolution

# 998244353 での多項式積
a = [1, 2, 3]
b = [4, 5, 6]
# (1 + 2x + 3x^2) * (4 + 5x + 6x^2)
res = convolution(a, b)
print(res)  # [4, 13, 28, 27, 18]
```

---

## 5. 文字列アルゴリズム (String Algorithms)

### `atcoder.string`
* **使用例**:
```python
import atcoder.string

s = "mississippi"

# Suffix Array (接尾辞配列)
sa = atcoder.string.suffix_array(s)
print("Suffix Array:", sa)

# LCP Array (最長共通接頭辞配列)
lcp = atcoder.string.lcp_array(s, sa)
print("LCP Array:", lcp)

# Z-algorithm (接頭辞一致長)
z = atcoder.string.z_algorithm("abracadabra")
print("Z-array:", z)
```
