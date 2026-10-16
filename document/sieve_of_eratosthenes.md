# エラトステネスの篩（Sieve of Eratosthenes）完全攻略ガイド

指定された範囲内の素数を高速かつ一括で全列挙するための代表的なアルゴリズム「エラトステネスの篩」についての解説とPythonによる実装例です。

---

## 目次
1. [エラトステネスの篩とは](#1-エラトステネスの篩とは)
2. [アルゴリズムの仕組み](#2-アルゴリズムの仕組み)
3. [計算量](#3-計算量)
4. [Pythonでの基本実装](#4-pythonでの基本実装)
5. [応用テクニック・実戦での使い方](#5-応用テクニック実戦での使い方)

---

## 1. エラトステネスの篩とは

指定された整数 $N$ 以下の素数をすべて列挙するためのアルゴリズムです。
1つずつ素数判定を行うと $O(N \sqrt{N})$ の時間がかかりますが、エラトステネスの篩を使うことで **$O(N \log \log N)$** という驚異的な速さで一括取得できます。

競技プログラミングや数論処理で「$N$ 以下の素数テーブル」を作成する際の標準的な手法です。

---

## 2. アルゴリズムの仕組み

1. **初期化**: 長さ $N + 1$ の配列（またはテーブル）を用意し、すべて `True`（素数候補）にする。$0$ と $1$ は素数ではないため `False` にする。
2. **探索と振り落とし**: $p = 2$ から順に見ていき、`True` のまま残っている数（＝素数）を見つけたら、その倍数（$p \times 2, p \times 3, \dots$）をすべて `False`（合成数）に変える。
3. **範囲の最適化**: 振るい落とす処理は $\sqrt{N}$ までループすれば十分（$p \times p > N$ となったら倍数の判定を打ち切ってよい）。

---

## 3. 計算量

* **時間計算量**: $O(N \log \log N)$
  * 実質的に $O(N)$ に近い非常に高速な動作をします。
* **空間計算量**: $O(N)$
  * サイズ $N + 1$ のブール配列（Flagテーブル）を保持するためのメモリ領域が必要です。

---

## 4. Pythonでの基本実装

### 基本的な実装パターン
```python
def sieve_of_eratosthenes(n: int) -> list[int]:
    """n 以下の素数リストを返す"""
    if n < 2:
        return []
    
    # is_prime[i] が True なら i は素数候補
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            # p*p 未満の倍数はすでに以前の素数によってふるい落とされているため p*p からスタート
            for multi in range(p * p, n + 1, p):
                is_prime[multi] = False
                
    # True のまま残っているインデックスを素数として抽出
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes

# 使用例
print(sieve_of_eratosthenes(30))
# 出力: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

---

## 5. 応用テクニック・実戦での使い方

### 1. 判定クエリの高速化（$O(1)$ 判定）
リストとして素数を返すだけでなく、`is_prime` 配列そのものを保持しておくと、$x$ が素数かどうかを $O(1)$ で判定できます。

```python
is_prime = [True] * (10**6 + 1)
is_prime[0] = is_prime[1] = False
for p in range(2, 1000 + 1):
    if is_prime[p]:
        for multi in range(p * p, 10**6 + 1, p):
            is_prime[multi] = False

# 高速判定
print(is_prime[997])  # True
print(is_prime[1000]) # False
```

### 2. 高速素因数分解 (SPF: Smallest Prime Factor)
篩の過程で「その数を割り切る最小の素数 (SPF)」を記録しておくと、$N$ 以下の任意の数に対する素因数分解を **$O(\log N)$** で行えるようになります。

```python
def build_spf(n: int) -> list[int]:
    """最小素因数 (Smallest Prime Factor) のテーブルを構築"""
    spf = list(range(n + 1))
    for p in range(2, int(n**0.5) + 1):
        if spf[p] == p:  # p が素数の場合
            for multi in range(p * p, n + 1, p):
                if spf[multi] == multi:
                    spf[multi] = p
    return spf

def factorize(x: int, spf: list[int]) -> list[int]:
    """SPF を用いた高速素因数分解 O(log X)"""
    factors = []
    while x > 1:
        factors.append(spf[x])
        x //= spf[x]
    return factors

# 使用例
MAX_N = 100000
spf = build_spf(MAX_N)

print(factorize(60, spf))  # 出力: [2, 2, 3, 5]
print(factorize(999, spf)) # 出力: [3, 3, 3, 37]
```

### 3. 区間エラトステネスの篩
$N$ が大きく（例: $N = 10^{12}$）、特定の区間 $[L, R]$（幅 $R - L \le 10^6$）に含まれる素数だけを求めたい場合に用いられる変種手法です。$\sqrt{R}$ までの素数を使って区間内の合成数を篩い落とします。
