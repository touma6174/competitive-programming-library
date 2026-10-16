# AtCoderのための 累積和・包除原理 完全攻略ガイド

競技プログラミング（特にAtCoder）で必須となる「累積和」と「包除原理」の基礎概念、実装テンプレート、および応用テクニックをまとめたリファレンスガイドです。

---

## 目次
1. [累積和 (Prefix Sum)](#1-累積和-prefix-sum)
2. [2次元累積和 (2D Prefix Sum)](#2-2次元累積和-2d-prefix-sum)
3. [いもす法 (Imos Method)](#3-いもす法-imos-method)
4. [包除原理 (Inclusion-Exclusion Principle)](#4-包除原理-inclusion-exclusion-principle)
5. [まとめと解法選択の目安](#5-まとめと解法選択の目安)

---

## 1. 累積和 (Prefix Sum)

### 概要
配列の区間和クエリを高速に処理するテクニック。前計算 $O(N)$ を行うことで、任意の区間 $[l, r)$ の和を **$O(1)$** で計算できます。

### 1次元累積和の公式
- 前計算: `S[i + 1] = S[i] + A[i]`
- 半開区間 $[l, r)$ の和: `S[r] - S[l]`

### C++ / Python 実装比較

#### C++17
```cpp
vector<long long> A = {3, 1, 4, 1, 5};
int N = A.size();
vector<long long> S(N + 1, 0);

for (int i = 0; i < N; ++i) {
    S[i + 1] = S[i] + A[i];
}

// 区間 [1, 4) の和を取得
long long sum_1_4 = S[4] - S[1];
```

#### Python 3
```python
A = [3, 1, 4, 1, 5]
N = len(A)
S = [0] * (N + 1)

for i in range(N):
    S[i + 1] = S[i] + A[i]

# 区間 [1, 4) の和を取得
sum_1_4 = S[4] - S[1]
```

---

## 2. 2次元累積和 (2D Prefix Sum)

### 概要
グリッドや2次元配列における長方形領域の総和を **$O(1)$** で求める手法です。

### 前計算と区間和取得の公式
- 前計算: `S[i+1][j+1] = A[i][j] + S[i][j+1] + S[i+1][j] - S[i][j]`
- 長方形領域 $[r_1, r_2) \times [c_1, c_2)$ の和:
  `S[r2][c2] - S[r1][c2] - S[r2][c1] + S[r1][c1]`

### Python 3 実装例
```python
H, W = len(grid), len(grid[0])
S = [[0] * (W + 1) for _ in range(H + 1)]

# 1. 前計算
for i in range(H):
    for j in range(W):
        S[i + 1][j + 1] = (
            grid[i][j] + S[i][j + 1] + S[i + 1][j] - S[i][j]
        )


# 2. クエリ取得: [r1, r2) x [c1, c2)
def query(r1, r2, c1, c2):
    return S[r2][c2] - S[r1][c2] - S[r2][c1] + S[r1][c1]
```

---

## 3. いもす法 (Imos Method)

### 概要
「区間 $[l, r)$ に値 $v$ を加算する」というクエリが多数与えられる場合、各クエリを $O(1)$ で処理し、最後に1次元累積和をとることで最終的な配列を $O(N + Q)$ で復元するテクニック。

### 1次元いもす法の手順
1. 配列 `B` を $0$ で初期化（サイズ $N + 1$）。
2. 区間 $[l, r)$ に $+v$ するクエリに対して:
   - `B[l] += v`
   - `B[r] -= v`
3. 最後に `B` の累積和をとる。

---

## 4. 包除原理 (Inclusion-Exclusion Principle)

### 概要
いくつかの条件集合 $A_1, A_2, \dots, A_n$ の和集合の要素数を求める際、「1つの集合のサイズを加算」「2つの交わりを減算」「3つの交わりを加算」…と交互に符号を変えて計算する数学的原理。

### 公式
$$ \left| \bigcup_{i=1}^n A_i \right| = \sum_{i=1}^n |A_i| - \sum_{1 \le i < j \le n} |A_i \cap A_j| + \sum_{1 \le i < j < k \le n} |A_i \cap A_j \cap A_k| - \dots $$

### 実装パターン（bit全探索）
条件の個数 $N$ が小さいとき（$N \le 20$ 程度）、bit全探索を使って包除原理を実装します。

#### Python 3 実装例（$1$ 以上 $M$ 以下の整数で、与えられた素数集合のいずれでも割り切れるものの個数）
```python
def count_multiples(M, primes):
    N = len(primes)
    ans = 0

    # 1 << N で 2^N 通りの部分集合を全探索
    for bit in range(1, 1 << N):
        popcount = 0
        lcm_val = 1
        possible = True

        for i in range(N):
            if (bit >> i) & 1:
                popcount += 1
                # 最小公倍数 (LCM) を計算
                import math

                lcm_val = (lcm_val * primes[i]) // math.gcd(lcm_val, primes[i])
                if lcm_val > M:
                    possible = False
                    break

        if not possible:
            continue

        # 要素数が奇数なら加算、偶数なら減算
        if popcount % 2 == 1:
            ans += M // lcm_val
        else:
            ans -= M // lcm_val

    return ans
```

---

## 5. まとめと解法選択の目安

| 手法 | 適用条件・特徴 | 計算量 |
|---|---|---|
| **1次元累積和** | 静的な配列の区間和を高速取得 | 前計算 $O(N)$ / クエリ $O(1)$ |
| **2次元累積和** | グリッドの長方形領域の和を取得 | 前計算 $O(HW)$ / クエリ $O(1)$ |
| **いもす法** | 区間加算クエリを一括処理（オフライン） | 前計算 $O(Q)$ / 復元 $O(N)$ |
| **包除原理** | 「少なくとも1つを満たす」「いずれも満たさない」条件の数え上げ | 条件数 $N$ に対し $O(2^N \times \text{処理})$ |
