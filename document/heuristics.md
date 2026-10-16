# AtCoder Heuristic Contest (AHC) 最適化アルゴリズム完全攻略ガイド

競技プログラミング（特に AHC や Marathons 系のコンテスト）で頻出となる「ヒューリスティック探索・局所探索・メタヒューリスティクス」の主要アルゴリズム、評価関数の作り方、および実装テンプレートをまとめたリファレンスガイドです。

---

## 目次
1. [ヒューリスティック問題（AHC）の解法選択チャート](#1-ヒューリスティック問題ahcの解法選択チャート)
2. [山登り法 (Hill Climbing)](#2-山登り法-hill-climbing)
3. [焼き鈍し法 (Simulated Annealing)](#3-焼き鈍し法-simulated-annealing)
4. [ビームサーチ (Beam Search)](#4-ビームサーチ-beam-search)
5. [評価関数の作成と高速化のコツ](#5-評価関数の作成と高速化のコツ)

---

## 1. ヒューリスティック問題（AHC）の解法選択チャート

```
【問題の性質と構造】
  ├─ 1ステップずつ状態を確定・選択していく（ゲーム・パズル・構築系）
  │    └── 状態空間が広い / 評価値に先読みが必要 ──> ビームサーチ (Beam Search)
  │
  └─ 状態全体を「遷移（近傍操作）」によって少しずつ改善していく（配置・割り当て・順序系）
       ├─ 最適解の近くで局所解（ハマり）に陥りにくい ──> 山登り法
       └─ 局所解（ローカルオプティマ）を抜け出したい ──> 焼き鈍し法 (Simulated Annealing)
```

---

## 2. 山登り法 (Hill Climbing)

### 概要
現在の状態から「近傍操作（少しだけ状態を変える操作）」を行い、**スコアが良くなる場合のみ**状態を更新する最もシンプルで基礎的な手法です。

### 特徴
- **メリット**: 実装が非常に簡単、高速。
- **デメリット**: 途中でスコアが改善しなくなる「局所解（ローカルオプティマ）」にハマるとそこから抜け出せない。

---

## 3. 焼き鈍し法 (Simulated Annealing)

### 概要
山登り法を拡張し、**「スコアが悪化する遷移」も確率的に許容する**ことで局所解から脱出できるようにした手法です。探索の序盤は悪化を許容し（高温度）、終盤にかけて徐々に許容率を下げていきます（低温度）。

### 遷移受容確率の公式
スコアを最大化する場合、現在のスコアを $S_{new}$、直前のスコアを $S_{old}$、現在の温度を $T$ とすると、スコア悪化量 $\Delta S = S_{new} - S_{old}$ に対し、遷移を受け入れる確率は以下で定義されます。

$$ P = \exp\left(\frac{S_{new} - S_{old}}{T}\right) \quad (\Delta S < 0 \text{ のとき}) $$

※ スコア最小化問題の場合は $\exp\left(\frac{S_{old} - S_{new}}{T}\right)$

### C++ 実装テンプレート

```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <chrono>

using namespace std;

// 高精度タイマー
struct Timer {
    chrono::high_resolution_clock::time_point start_time;
    Timer() { start_time = chrono::high_resolution_clock::now(); }
    double progress(double time_limit) const {
        auto now = chrono::high_resolution_clock::now();
        double elapsed = chrono::duration_cast<chrono::microseconds>(now - start_time).count() * 1e-6;
        return elapsed / time_limit;
    }
};

int main() {
    constexpr double TIME_LIMIT = 1.95; // 制限時間 (秒)
    Timer timer;
    mt19937 rng(42);
    uniform_real_distribution<double> dist_01(0.0, 1.0);

    // 初期解の構築
    // State state = init();
    double current_score = 0.0; // eval(state);
    double best_score = current_score;

    constexpr double T0 = 2000.0; // 初期温度
    constexpr double T1 = 10.0;   // 最終温度
    double temperature = T0;

    long long iter_count = 0;

    while (true) {
        double progress = timer.progress(TIME_LIMIT);
        if (progress >= 1.0) break;

        // 現在の温度の更新 (指数的または線形冷却)
        temperature = T0 * pow(T1 / T0, progress);

        // 1. 近傍操作の適用（状態の変更）
        // auto change = apply_neighbor(state);
        double new_score = 0.0; // eval_diff(state, change);

        double score_diff = new_score - current_score; // 最大化問題

        // 2. 遷移判定
        if (score_diff >= 0 || exp(score_diff / temperature) > dist_01(rng)) {
            // 遷移受容: 状態を確定
            current_score = new_score;
            if (new_score > best_score) {
                best_score = new_score;
            }
        } else {
            // 遷移拒否: 状態を元に戻す (ロールバック)
            // rollback(state, change);
        }
        iter_count++;
    }

    return 0;
}
```

---

## 4. ビームサーチ (Beam Search)

### 概要
各ターン（ステップ）ごとに、評価値が高い上位 $B$ 個（ビーム幅）の状態のみを保持し、次のステップへと同時に展開していく貪欲法の拡張探索手法です。

### 特徴
- **メリット**: 深さ優先探索のように1つのパスに固執せず、幅優先探索のように探索空間が爆発しない。
- **データ構造**: 各ステップの候補を保持・ソートするために優先度付きキュー（`priority_queue`）やソート済みリストを用います。

---

## 5. 評価関数の作成と高速化のコツ

### 1. 差分計算 (Incremental Evaluation)
- AHC で最もスコアに直結するテクニックです。
- 1回の近傍操作で「状態全体をゼロから再評価」すると $O(N)$ かかる処理を、**変更された部分の差分だけを計算して $O(1)$ や $O(\log N)$ で評価値を更新する**ことで、ループ回数を数十〜数百倍に増やすことができます。

### 2. 状態のロールバック構造
- 近傍操作が拒否された場合に、軽量に元の状態へ復元できる設計にします。
  - **変更履歴を持っておき逆操作を適用する**
  - **変更箇所が少ない場合は値を直接書き戻す**

### 3. 温度パラメータ設定の目安
- **初期温度 $T_0$**: 悪い遷移（期待される典型的なスコア悪化量）を 50%〜80% 程度の確率で受容する温度に設定。
- **最終温度 $T_1$**: ほとんど悪化遷移を受け入れず、山登り法と同等になる温度（ごく僅かな悪化のみ受容）に設定。
