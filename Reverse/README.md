# Reverse

> 做逆向的第一步可以先用 strings 观察下封装方式。比如发现过 PyInstaller 的打包

## 环境

### macOS
#### ida64
按 f5 反编译，只能反编译 64 位
#### ida pro
不能用中文输入法

## ida
可以点 search-search text 来全局搜索

## Python

### PyInstaller 打包的 exe 逆向

#### python-exe-unpacker

```bash
python python_exe_unpack.py -i [malware.exe]
```

### pyc 反编译为 py

如果用 file 命令查到文件是类似格式

```bash
python 3.7 byte-compiled
```

则将文件后缀改为 pyc

在 ctf 容器中，输入

```bash
uncompyle6 -o test.py test.pyc
# 意思是将 pyc 反编译为 py
```




