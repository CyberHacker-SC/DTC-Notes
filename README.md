CTF Run
======

[Web](Web/README.md)

[Misc](Misc/README.md)

[Crypto](Crypto/README.md)

[Reverse](Reverse/README.md)

[RDG](RDG/README.md)



## Flag 正则匹配

### 匹配类似 flag{asdas_sd2} 的字符串

带前缀

```
flag\{[^}]*\}
```

不带前缀

```regex
\w+\{[^}]*\}
```

### 匹配 flag 这几个字母后跟 {

可以匹配类似 `F|L|A|G {` 的字符串（即可匹配 `F|L|A|G {y0u_w1n_th1s_!!!}`）

```
[Ff].{0,3}?[Ll].{0,3}?[Aa].{0,3}?[Gg].{0,3}?\{
```

