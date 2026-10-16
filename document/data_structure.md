# AtCoderのためのデータ構造 完全攻略ガイド

競技プログラミング（特にAtCoder）で頻出するデータ構造、各データ構造の得意分野、クエリの計算量、およびAtCoder Library (ACL) の活用方法をまとめた完全リファレンスガイドです。

---

## 目次
1. [標準データ構造（STL）の使い分け](#1-標準データ構造stlの使い分け)
2. [Union-Find (DSU)](#2-union-find-dsu)
3. [Fenwick Tree (Binary Indexed Tree / BIT)](#3-fenwick-tree-binary-indexed-tree--bit)
4. [セグメント木 (Segment Tree)](#4-セグメント木-segment-tree)
5. [遅延評価セグメント木 (Lazy Segment Tree)](#5-遅延評価セグメント木-lazy-segment-tree)
6. [文字列用データ構造（Trie木 / Suffix Array）](#6-文字列用データ構造trie木--suffix-array)
7. [データ構造選択のフローチャート](#7-データ構造選択のフローチャート)

---

## 1. 標準データ構造（STL）の使い分け

| データ構造 | C++ クラス | 検索・アクセス | 挿入・削除 | 主な用途・特徴 |
|---|---|---|---|---|
| **動的配列** | `std::vector` | $O(1)$ | 末尾: $O(1)$ | 基本データ構造。前計算やDPテーブルに |
| **両端キュー** | `std::deque` | $O(1)$ | 先頭・末尾: $O(1)$ | 0-1 BFS やスライド最小値 |
| **優先度付きキュー** | `std::priority_queue` | 根: $O(1)$ | $O(\log N)$ | ダイクストラ法、貪欲法で最大・最小を常時取得 |
| **平衡二分探索木** | `std::set` / `std::multiset` | $O(\log N)$ | $O(\log N)$ | 順序付き集合の管理。`lower_bound` で探索 |
| **連想配列** | `std::map` | $O(\log N)$ | $O(\log N)$ | 任意型のキーと値の保持。座標圧縮にも活用 |
| **ハッシュテーブル** | `std::unordered_map` | 平均 $O(1)$ | 平均 $O(1)$ | 高速だが最悪ケース $O(N)$ に注意 (Hack回避が必要な場合あり) |

---

## 2. Union-Find (DSU)

### 概要
要素のグループ（素集合）の併合と、2つの要素が同じグループに属するかどうかの判定を高速に行う構造。

### 主なクエリと計算量
- **`merge(u, v)`**: $u$ と $v$ の属するグループを統合する。
- **`same(u, v)`**: $u$ と $v$ が同じグループか判定する。
- **計算量**: 1クエリあたり **$O(\alpha(N))$**（アッカーマン関数の逆関数。実質 $O(1)$）。

### 応用テクニック
- **重み付き Union-Find**: 頂点間のポテンシャル差（距離関係）を管理。
- **Undo可能 Union-Find**: 過去の状態に1ステップ戻す（可変木やオフライン動的連結性）。
- **ACL 対応**: `atcoder::dsu`

---

## 3. Fenwick Tree (Binary Indexed Tree / BIT)

### 概要
配列の一点加算と区間和取得を軽量かつ高速に行える構造。

### 主なクエリと計算量
- **一点加算 (`add(i, x)`)**: $O(\log N)$
- **区間和取得 (`sum(l, r)`)**: $O(\log N)$
- **空間計算量**: $O(N)$（セグメント木の約 $1/2 \sim 1/4$ のメモリと高速な定数倍）

### 定番の用途
- **転倒数（Inversion Number）の計算**: 幾つ隣り合う要素を入れ替えればソートできるかのカウント。
- **平面走査**: 2次元問題を1次元走査＋BITに落とし込む。
- **ACL 対応**: `atcoder::fenwicktree<T>`

---

## 4. セグメント木 (Segment Tree)

### 概要
完全二分木を用いて、配列の一点更新と任意の区間クエリ（最小値、最大値、GCD、和など）を処理する構造。

### 乗る代数構造（モノイド）
演算 $\cdot$ が**結合律** $(a \cdot b) \cdot c = a \cdot (b \cdot c)$ を満たし、**単位元** $e$ が存在すること。

### 主なクエリと計算量
- **一点更新 (`set(i, x)`)**: $O(\log N)$
- **区間取得 (`prod(l, r)`)**: $O(\log N)$
- **二分探索 (`max_right / min_left`)**: 区間上で条件を満たす最大の右端/左端を $O(\log N)$ で取得。

### 代表的な用途
- **RMQ (Range Minimum Query)**: 区間最小値取得。
- **Point Update Range Sum**: 一点更新・区間和取得。
- **ACL 対応**: `atcoder::segtree<S, op, e>`

---

## 5. 遅延評価セグメント木 (Lazy Segment Tree)

### 概要
「区間更新」や「区間加算」といった**区間全体に対する一括操作**を、実際に必要になるまで評価を遅延させることで高速化させた構造。

### 乗る代数構造（作用素付きモノイド）
モノイド $S$ に対し、作用素の集合 $F$ が**写像の合成**および**分配律**を満たすこと。

### 主なクエリと計算量
- **区間更新・作用 (`apply(l, r, f)`)**: $O(\log N)$
- **区間取得 (`prod(l, r)`)**: $O(\log N)$

### 代表的な用途
- **RUQ (Range Update Query)**: 区間代入 ＋ 区間最小値取得。
- **RAQ (Range Add Query)**: 区間加算 ＋ 区間和取得。
- **ACL 対応**: `atcoder::lazysegtree<S, op, e, F, mapping, composition, id>`

---

## 6. 文字列用データ構造（Trie木 / Suffix Array）

### 1. Trie木 (トライ木)
- **概要**: 文字列のプレフィックス（接頭辞）を木構造で管理する構造。
- **クエリ**: 挿入・検索が文字列長 $L$ に対し $O(L)$。
- **応用**: 辞書順検索、XORの最大値を求める「Binary Trie」。

### 2. Suffix Array (接尾辞配列)
- **概要**: 文字列 $S$ のすべての接尾辞（Suffix）を辞書順にソートした開始位置の配列。
- **計算量**: 構築 $O(|S|)$ (SA-IS法など) または $O(|S| \log |S|)$。
- **応用**: LCP Array（最長共通接頭辞配列）と組み合わせて、任意部分文字列の出現数や長さを高速処理。
- **ACL 対応**: `atcoder::suffix_array`, `atcoder::lcp_array`

---

## 7. データ構造選択のフローチャート

### 【要素のグループ分け・連結性の管理がしたい】
- Union-Find (atcoder::dsu)

### 【クエリが「一点更新」＆「区間取得」のみ】

- 演算が「加算」のみで、実装を軽くしたい
BIT (atcoder::fenwicktree)
- 任意モノイド（RMQ, 区間GCD等
セグメント木 (atcoder::segtree)

### 【クエリに「区間更新」や「区間加算」が含まれる】
- 遅延評価セグメント木 (atcoder::lazysegtree)

### 【要素が動的に挿入/削除され、全体のk番目や直近の値が知りたい】
- std::set + lower_bound
- Binary Trie
