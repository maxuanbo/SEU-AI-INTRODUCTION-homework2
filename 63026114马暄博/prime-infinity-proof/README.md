# 素数无穷性的构造性证明

> 课程作业提交版：对“任意给定自然数 $n$，都存在素数 $p>n$”的证明、自我反思与计算验证。

## 结论

对任意自然数 $n$，都存在素数 $p$，使得

$$
p > n.
$$

程序验证：输入 $n=100$，输出 $p=101$；且 $101$ 是素数、$101>100$。

---

## 仓库结构

```text
prime-infinity-proof/
├── README.md
├── .gitignore
├── report/
│   ├── prime-infinity-proof-A4.pdf    # 4 页 A4 报告
│   └── prime-infinity-proof-A4.docx   # 可编辑报告
├── results/
│   └── verification_output.txt        # 完整运行记录
└── src/
    └── prime_greater_than.py          # 验证脚本
```

---

## 1. 欧几里得的经典论证

欧几里得《几何原本》第九卷命题 20 的现代表述是：

> 素数比任何指定的素数集合都多。

论证的核心不是“再找一个素数”，而是把任意有限清单当作已经穷尽了全部素数，再构造一个清单无法解释的对象：

1. 设 $p_1,p_2,\dots,p_k$ 是全部素数；
2. 构造 $N=p_1p_2\cdots p_k+1$；
3. $N>1$，所以 $N$ 必有素因子 $q$；
4. 每个 $p_i$ 都整除乘积，却不整除 $N$，因此 $q\ne p_i$；
5. 这与“清单包含全部素数”矛盾。

因此素数不可能只有有限多个。

---

## 2. 形式化构建

### 定理

$$
\forall n\in\mathbb{N},\ \exists p\in\mathbb{P},\ p>n.
$$

### 证明

固定任意自然数 $n$。

**情形一：$n<2$。**  
取 $p=2$。因为 $2$ 是素数，且 $2>0,2>1$，结论成立。

**情形二：$n\ge 2$。**  
令

$$
S_n=\{p\in\mathbb{P}:p\le n\}=\{p_1,p_2,\dots,p_k\}.
$$

因为 $2\in S_n$，所以 $k\ge 1$。构造

$$
N=p_1p_2\cdots p_k+1.
$$

于是 $N\ge 3>1$。由“每个大于 1 的整数都有素因子”，存在素数 $q$ 使得

$$
q\mid N.
$$

对每个 $i=1,\dots,k$，有

$$
N\equiv 1\pmod{p_i},
$$

所以 $p_i\nmid N$，从而 $q\ne p_i$。这说明

$$
q\notin S_n.
$$

而 $S_n$ 已包含所有不超过 $n$ 的素数，因此必有

$$
q>n.
$$

综上，任意自然数 $n$ 都存在严格大于它的素数。$\square$

> 证明的关键改进：这里只假设有界集合 $S_n$ 有限，并没有假设全体素数有限，因此不存在循环论证。

---

## 3. 自我反思

| 检查点 | 结论 | 说明 |
|---|---|---|
| $N$ 能被某个 $p_i$ 整除吗？ | 不能 | $N\equiv1\pmod{p_i}$，带余除法给出的余数是 1，不是 0 |
| $N$ 一定大于 1 吗？ | 一定 | 清单含 2，乘积至少为 2，因此 $N\ge3$ |
| $N$ 本身一定是素数吗？ | 不一定 | 例如 $2\cdot3\cdot5\cdot7\cdot11\cdot13+1=30031=59\times509$；证明只需要 $N$ 的某个素因子 $q$，不能把 $N$ 直接当作素数 |
| 是否预设了“全体素数有限”？ | 没有 | 只使用 $S_n=\{p\le n\}$ 有限，这是有界集合 |
| $q$ 会不会仍等于某个 $p_i$？ | 不会 | 若 $q=p_i$，则 $p_i\mid N$ 且 $p_i\mid$ 乘积，于是 $p_i\mid1$，矛盾 |
| $q$ 一定严格大于 $n$ 吗？ | 一定 | $q$ 是素数且不在 $S_n$ 中，而 $S_n$ 已包含所有不超过 $n$ 的素数 |
| $n=0$ 或 $n=1$ 怎么办？ | 单独处理 | 取 $p=2$，因为 $2>0,2>1$ |

审计结论：整除性、$N>1$、非循环性与边界情形均已闭合。唯一需要修正的常见表述是：

- ❌ “$N$ 一定是素数”
- ✅ “$N$ 有一个素因子 $q$，且 $q$ 在清单之外”

---

## 4. 计算验证

脚本从 $n+1$ 开始逐个检查，返回第一个素数。素性判定使用精确试除法，只检查到 $\lfloor\sqrt{c}\rfloor$。

### 运行

Windows PowerShell：

```powershell
python .\src\prime_greater_than.py 100
```

macOS / Linux：

```bash
python3 src/prime_greater_than.py 100
```

### 输出

```text
=== Direct search ===
n                = 100
p                = 101
p - n            = 1
is_prime(p)      = True
p > n            = True

=== Euclid construction for n = 10 ===
primes <= 10     = [2, 3, 5, 7]
N                = 2 * 3 * 5 * 7 + 1 = 211
N mod p_i        = [1, 1, 1, 1]
prime factor q   = 211
q > 10           = True

=== Regression checks ===
n=      0  p=       2  gap=  2  verified
n=      1  p=       2  gap=  1  verified
n=      2  p=       3  gap=  1  verified
n=      3  p=       5  gap=  2  verified
n=     10  p=      11  gap=  1  verified
n=    100  p=     101  gap=  1  verified
n=   1000  p=    1009  gap=  9  verified
n=  10000  p=   10007  gap=  7  verified
n=1000000  p= 1000003  gap=  3  verified
ALL CHECKS PASSED
```

完整记录见 [`results/verification_output.txt`](results/verification_output.txt)。

---

## 运行环境

- Python 3.12.14
- 仅使用标准库：`argparse`、`math`
- 无第三方依赖

---

## 报告

- [A4 PDF 报告](report/prime-infinity-proof-A4.pdf)
- [A4 DOCX 可编辑版](report/prime-infinity-proof-A4.docx)

报告共 4 页，包含知识检索、形式化证明、自我反思、代码验证与运行结果。
