// https://github.com/touma6174/competitive-programming-library.git
#ifdef ONLINE_JUDGE
#pragma GCC target("avx2")
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
#endif
#include <atcoder/all>
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
#define rep(i, n) for (int i = 0; i < (int)(n); ++i)
#define rep2(i, s, n) for (int i = (s); i < (int)(n); ++i)
#define all(v) (v).begin(), (v).end()
inline void yn(bool x) { cout << (x ? "Yes" : "No") << "\n"; }
inline void YN(bool x) { cout << (x ? "YES" : "NO") << "\n"; }
constexpr char el = '\n';
constexpr int dr[4] = {-1, 0, 0, 1};
constexpr int dc[4] = {0, -1, 1, 0};
constexpr int dr8[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
constexpr int dc8[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
}
