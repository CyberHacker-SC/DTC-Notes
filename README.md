CTF Run
======

[Web](Web/README.md)

[Misc](Misc/README.md)

[Crypto](Crypto/README.md)

[Reverse](Reverse/README.md)

[RDG](RDG/README.md)



## Flag 正则匹配

### 匹配类似 flag{asdas_sd2} 的字符串

#### 规范格式匹配

带前缀

```
flag\{[^}]*\}
```

不带前缀（匹配可能是其他前缀的 flag，如 `NSSCTF{d22cb234-3654-40d7-870a-8919fbe02855}`）

```regex
\w+\{[^}]*\}
```

#### 不规范格式匹配

带前缀，`{` 前面可以有空格，如 `flag{d22cb234-3654-40d7-870a-8919fbe02855}`

```
flag\s*\{[^}]*\}
```

不带前缀，匹配可能是其他前缀的 flag，`{` 前面可以有空格，如 `NSSCTF {d22cb234-3654-40d7-870a-8919fbe02855}`

```
\w+\s*\{[^}]*\}
```

### 匹配 flag 这几个字母后跟 {

可以匹配类似 `F|L|A|G {` 的字符串（即可匹配 `F|L|A|G {y0u_w1n_th1s_!!!}`）

```
[Ff].{0,3}?[Ll].{0,3}?[Aa].{0,3}?[Gg].{0,3}?\{
```

