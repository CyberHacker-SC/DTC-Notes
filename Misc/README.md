# Misc

- 脑洞：

- - 不排除 Misc 的 flag 是中文的情况，比如图片中隐藏了几个模糊的汉字。（有时候缩小了看得更清楚？）

  - 解到离 flag 最近的一步，{} 中是大写数字，把大写数字转为正规数字即可得到 flag

  - 有一道题，得到一串很乱的文本，按字频统计排序后即可得到 flag

  - 遇到过一道找两张图片不同的题，结果就是找 hex 的 text 部分，把两串明显像 flag 的特殊字符连起来解密处理

  - 看到两张图片，联想到图片盲水印提取

  - 遇到过一种打不开的 png，观察发现，图片中的 16 进制的每个字节 (16 进制的2位) 和 标准 png 的每个字节相加为一个定值 (题目中是 0x100)，所以通过下面的代码很容易求得原图片

  - ```python
    f1 = open("./1.png","rb")
    f2 = open("./2.png","wb")
    all_data = f1.read()
    lt = []
    for i in all_data:
        if i == 0:
            lt.append(i)
        else:
            lt.append(0x100 - i)
    f2.write(bytes(lt))
    f1.close()
    f2.close()
    ```

- macOS 的坑：

- - 遇到过一次解压输入密码后解压不了，这时换一个解压软件即可
  - 使用 hex friend 复制出来的文本格式有时候有问题（Mac 上肉眼看不见，用剪切板或粘贴在终端即可发现），这时 OCR 一次。

## 图片类型

- bitmap 格式的文件后缀是 bmp，TIFF 格式的后缀是 tif (这些类图片格式可以考虑直接改成 jpg 打开)
- png 图片可以先用 `pngcheck 1.png` 检查一下图片有没问题，打不开的图片也可能是宽高被修改了。png 还可以考虑 lsb 一键工具
- PS 中可以点击上方菜单栏的 窗口—信息 查看每个像素点的坐标
- 图片不一定只是图片，完全可以当成文件来做，例如用 strings 输出该文件的信息，可能有隐藏提示

### 二维码、条码识别
https://online-barcode-reader.inliteresearch.com/

有时候扫了二维码不一定能拿到 flag，遇到一道题，将 flag 藏在了 URL 的路径处，解开 base64 即可拿到 flag

### 查看 hex 中有无线索
html 的编码样子

类似 &#x66;&#x6c;&#x61;

使用 hex friend 复制出来的文本格式有时候有问题（Mac 上肉眼看不见，用剪切板或粘贴在终端即可发现），OCR 一次。

### 图片属性里有可能藏有东西

> macOS 像 Windows 一样查看图片的备注
```bash
exiftool -verbose 1.jpg
# 其中输出内容的 XPComment 就是图片备注
```

### 破解正确宽高

有时候因为图片宽高被修改了导致显示不全

```python
import binascii
import struct
import sys

file = input("图片的地址")
fr = open(file,'rb').read()
data = bytearray(fr[0x0c:0x1d])
crc32key = eval('0x'+str(binascii.b2a_hex(fr[0x1d:0x21]))[2:-1])
#原来的代码: crc32key = eval(str(fr[29:33]).replace('\\x','').replace("b'",'0x').replace("'",''))
n = 4095
for w in range(n):
    width = bytearray(struct.pack('>i', w))
    for h in range(n):
        height = bytearray(struct.pack('>i', h))
        for x in range(4):
            data[x+4] = width[x]
            data[x+8] = height[x]
        crc32result = binascii.crc32(data) & 0xffffffff
        if crc32result == crc32key:
            print(width,height)
            newpic = bytearray(fr)
            for x in range(4):
                newpic[x+16] = width[x]
                newpic[x+20] = height[x]
            fw = open(file+'.png','wb')
            fw.write(newpic)
            fw.close
            sys.exit()
```

### 图片取征 Stegsolve

#### LSB
在 Stegsolve-Analyse-Data Extract 勾上右下角3个0，点 preview

#### 可能是图片宽高被修改了
- 1.可以在 Stegsolve-Analyse-File format 最上面查看图片的原始宽高
- 2.使用自动破解宽高的程序恢复(Python 脚本)

#### 合并多张图
如果有多张图，可以用 Stegsolve 合并(Image Combiner)

### 另一种图片隐写解法 zsteg (png, bpm)
> 主要用来检测 png 和 bpm (主要用于 LSB ?)
```bash
zsteg -a file
```

### 图片盲水印提取

在 ctf 容器中，进入 /programme/CTF/工具/Misc/BlindWaterMark ，运行

```bash
python3.6 bwmforpy3.py decode 1.png 2.png 3.png
```

1.png 是原图，2.png 是加了水印的图片 (如果不知道 1.png 和 2.png 的顺序，可以尝试互换顺序)，得到 3.png 是去除水印的图片

### jphs

有的图片(如部分 jpg)需要用 Jphswin 打开并输出为 txt 文件。Mac 使用的 win 11 虚拟机，文件在 `/Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Misc/Windows工具/Jphswin.exe`

使用方法，选择图片，点 Seek，然后空密码，输出为 txt (其实不一定是 txt，根据具体情况，把后缀改了)

### gif

#### 横向拼接
> 如果有很多图(gif)，可能是横向拼接起来的

图片拼接地址 http://www.atoolbox.net/Tool.php?Id=978

注意：有可能是按修改日期排序后拼接


#### 逐帧解析
注意: macOS 自带的逐帧解析可能有问题

- 1、使用stegsolve打开图片 
- 2、analyse-》frame browser，一帧一帧看
  
#### 逐帧查看（分割 gif）
```bash
convert cake.gif cake.png
```

#### 合并 gif
```bash
convert -delay 3 *.png output.gif 
# 上述命令可以将当前目录下的所有 *.png 文件合成并生成 output.gif 文件。其中在 output.gif 文件中，每帧的间隔时间可以通过 -delay 参数来设置。
```

#### 百度识图人物或其他

百度识图就算人物脸部不全，也可以识别试试

## 文件
- 不要相信任何后缀类型。遇到一道题，虽然后缀是 zip，但实际是 word，应该改为 docx 格式，所以 zip 后缀也不能相信。

- efi 是 Unix 的可执行文件

- evt 是 Windows 的日志文件（好像需要 win 7 ?）

- 文件名可能是一个隐藏提示。（如 91 可能是 base91）

### 查看文件类型
用 file 命令识别下是什么文件 (不能完全相信 file)
```bash
file 文件名
```

有时候图片的 hex 被修改了，file 命令显示不准确，需要手动改文件头部的 hex 为正确 hex。格式如下

| 格式类型 | 文件头标识                            | 文件尾标识                          |
| -------- | ------------------------------------- | ----------------------------------- |
| jpeg/jpg | FFD8                                  | FFD9                                |
| gif      | 47 49 46 38 39(37) 61(G I F 8 9(7) a) |                                     |
| png      | 89 50 4E 47 0D 0A 1A 0A               | 00 00 00 00 49 45 4E 44 AE 42 60 82 |
| bmp      | 42 4D (B M)                           |                                     |
| tiff     | 4D 4D 00 2A / 49 49 2A 00             |                                     |

| **文件类型**  | **文件标识**         |
| ------------- | -------------------- |
| zip/docx/xlsx | 50 4B 03 04          |
| RAR           | 52 61 72 21          |
| doc/xls       | D0 CF 11 E0          |
| pdf           | 25 50 44 46 2D 31 2E |

### Hex

右键查看 Hex，优先使用 010 Editor

遇到过一道题，flag 藏在 Hex 中，构成图形，如下:

![](static/img/hex_img.jpg)

### txt

txt 文件有可能可以下滑，信息藏在最下面

### word
如果是 word 文件可能有隐藏文字

### 一个文件夹下一堆文件
用 VS Code 全局搜索关键词

### 查看 cat 输出乱码的文件
匹配二进制文件的 flag
```bash
strings webshell.pcapng | grep -E '.{1,10}\{.{1,50}\}.*'
# webshell.pcapng 为二进制文件
```

### 文件内部映像提取

#### binwalk
> 如果 binwalk 查到了内部映象却分离不了，应该尝试 foremost
>

**查照内部映像**
```bash
binwalk firmware.bin
```
注意:图片中有可能隐藏另一张图片

**文件自动提取**
```bash
binwalk -e firmware.bin
```

#### foremost

> 有时候用 binwalk 提取不了时，​可以用 foremost 提取。

**文件递归提取**
```bash
foremost -T ccc.pcap
```

### pcapng 格式

#### http 类型
>可以全局搜索文件后缀，右键追踪 http 流

**注入类**

可以通过观察 HTTP 包的长度判断哪些是注入成功的，拼接收到的 ascii 码即可

操作方法: 先筛选出 http (搜索 http 即可)，再按 http 导出，导出界面选择按 size 排序可能会看到连续的 flag

**SQL 盲注简单原理**

例如（下面的流量按时间顺序排序）

```python
LIMIT 0, 1),1,1) )>64 AND

LIMIT 0, 1),1,1))>96 AND

LIMIT 0, 1),1, 1) )>112 AND

LIMIT 0,1),1,1) )>104 AND

LIMIT 0, 1),1, 1) )>100 AND

LIMIT 0, 1),1,1))>102 AND

LIMIT 0, 1),1,1))>101 AND

LIMIT 0,1),2,1))>96 AND

LIMIT 0,1),2,1))>112 AND

LIMIT 0,1),2,1))>104 AND

LIMIT 0,1),2,1))>108 AND

LIMIT 0,1),2,1) )>106 AND

LIMIT 0, 1),2,1))>107 AND

LIMIT 0, 1),3,1))>96 AND

LIMIT 0, 1),3,1))>112 AND

LIMIT 0,1),3,1))>104 AND

LIMIt 0,1),3,1))>100 AND

LIMIt 0,1),3,1))>98 AND

LIMIT 0, 1),3, 1))>97 AND
```

数字的第3列代表猜的字段位数，`>`后面的数字是 Ascii 码。数字的第3列相同时，取最后一个 Ascii 码(如果后面有状态码，需要保证这一行的状态码是200而不是404)。将取得的 Ascci 码拼接好即是完整的字段。（可以用字典来拼接。一般依次猜数据库名、表名、列名等）

#### 键盘输入(USB)

**KBE**
```bash
python KBE.py
```

### cap 格式

可以根据此类型的文件破解 wifi 密码

使用 aircrack-ng，已经下载到了 Docker ctf 中

### aircrack-ng

根据 1.txt 密码表破解 wifi 密码，如
```bash
aircrack-ng -w 1.txt wifi.cap
```

补充：生成密码表，该数字开头的所有手机号
```bash
crunch 11 11 -t 1391040%%%% -o 1.txt
```

### 压缩文件

- 有的压缩文件只有内部的一个文件加密，可以手动试下其他文件能不能直接解压。
- 优先使用 unzip 命令解压，unzip 会自动解压上面提到的未加密文件。(但是遇到过编码不支持 unzip 的情况，所以不能只局限于 unzip)
- 如果 macOS 打不开压缩文件，尝试使用 Windows 虚拟机
- 直接用 binwalk 可以分离一个压缩包里未加密的文件

#### zip爆破

##### 破解伪加密
```bash
java -jar ZipCenOp.jar r  压缩包名
# (macOS jdk 17 上报错不用管，运行后用 unzip 解压即可，macOS 的解压软件有坑【最新测试全能解压不错】)
```

##### 暴力破解 

###### zipCrack

- 建议用 fcrackzip 替代

优先使用下一个工具 fcrackzip

```bash
git clone https://github.com/luckman666/zipCrack.git
cd zipCrack
python zipcrack.py -f  file.zip -d password.txt
# 注意:已经在 M1 Mac 的 /Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Misc/压缩包破解/zipCrack 处做了备份
```

###### fcrackzip

- 如果密码正确但破解过程失败了，可能是因为压缩包在之前的使用中损坏了

```bash
fcrackzip  -b -c 'aA1' -l 1-10 -u 文件名
```
```
-b 使用暴力算法
-D 使用字典破解
-B 查看当前机器破解速度
-v 显示更多信息
-p 使用字符串作为初始密码
-l 设置密码长度（1-10）
-u 不打印错误密码

-c指定字符集，字符集格式只能为 -c 'aA1!:' 
a 表示小写字母[a-z]
A 表示大写字母[A-Z]
1 表示阿拉伯数字[0-9]
! 感叹号表示任意特殊字符[!:$%&/()=?{[]}+*~#]
: 表示包含冒号之后的字符（不能为二进制的空字符），例如  a1:$%  表示 字符集包含小写字母、数字、$字符和%百分号

192837465  --->         [1]
a123  --->              [a1]
A123  --->              [A1]
Q123we  --->            [aA1]
Q123we!?  --->          [aA1:!?]
Qwe!?123  --->          [aA1:!?]
Qwe$%^&*(123  --->      [aA1!]
```
破解3位纯数字
```bash
fcrackzip -b -c 1 -l 3 -v file.zip
```

还可以指定密码字典来破解

1.先生成密码字典

- (1) 生成某个数值范围的密码字典

  ```python
  def main():
      text = ''
      for i in range(19900000, 20000000):
          text += str(i) + '\n'
          
      with open('passwords.txt', 'w') as f:
          f.write(text)
  
  
  if __name__ == '__main__':
      main()
  ```

  

- (2) 指定密码位数生成字典

  ```python
  def main():
      num = 9 # 一共多少位数
      prefix = '372' # 前缀(前缀后面的部分则覆盖 num 位数的所有数值)
      
      text = ''
      for i in range(0, 10 ** (num - (len(prefix)) + 1) ):
          i = str(i)
          left = '0' * (num - (len(prefix)) - len(i))
          text += prefix + left + i + '\n'
      
      with open('passwords.txt', 'w') as f:
          f.write(text)
  
  
  if __name__ == '__main__':
      main()
  ```

  

2.指定用这个字典破解

```
fcrackzip -v -D -p passwords.txt -u flag.zip
```

### .dat 文件

开源的微信 Dat 文件(.dat)解码器 http://github.com/PiaoZhenJia/WeChatDatFileDecoder

### GPS 数据流

先将 txt 转为 kml 格式 https://www.gpsvisualizer.com/map_input

再用 VS Code 打开 kml 文件，使用 Geo Data Viewer 插件可以绘制地图轨迹

## 文本

### 大小写隐写

遇到过一道题，一串文本里基本是小写字母，此时提取大写字母组合起来就是 flag 。示例代码

```python
def main():
    text = 'i was always Fond of visiting new scenes'
    flag = ''
    for i in text:
        if i.isupper():
            # 小写字母是 i.islower()
            flag += i
    print(flag)
    

if __name__ == '__main__':
    main()
```

### Zero-Width 隐写 (0宽隐写)

示例内容如：

```
dd师父父鸭❤️，想找一个男师父来宠我辽 ٩(๑‌‌‌‌‍‬‌﻿•ㅂ•)۶。要求如下鸭🌸，国赛三等奖及以上吖（重点，画圈圈），给窝包flag和jio‌‌‌‌‍﻿‍‌本辣种（开心❤️(≧▽≦‌‌‌‌‍‬‍‬)。
不要有战队的那种师父父o╰(‌‌‌‌‍﻿‌﻿*´︶`*)╯，因为有战队的话窝怕你队友会生我的气鸭💦（点点头qaq‌‌‌‌‍‬‬‌）
如果实在不行有战队的师父父窝也不介意的辣QVQ🌸！你就把你队友当成玩玩的就行叭✨，你每天陪窝更多就行啦‌‌‌‌‍‬﻿﻿~ ‌‌‌‌‍﻿‍﻿（害羞羞地扯了扯你的衣服袖子 (*๓´╰╯`๓)
另外另外🎉！窝占有欲非常强o💦（叉腰并且理直气壮！）所以希望你只有我一个可耐耐的徒徒辣（开心地看着你 (*‌‌‌‌‍﻿‬﻿≧▽≦) 所以你不能有别的徒徒鸭⭐‌‌‌‌‍‌﻿﻿，要不然我会炒鸡炒鸡桑心的o‌‌‌‌‍‍‌‌呜呜呜（突然委屈巴巴地看着你）
当然辽（突然开心地笑✨），你也不能散养窝鸭(๑•ູ॒॒̀‌‌‌‌‍‍﻿﻿•̀‌‌‌‌‍‬‬‍ູ॒॒•ູ॒॒̀•ູ॒॒̀•́๑)，所以窝希望你最好每天都替窝做题~窝一直在旁边打游戏辣种叭❤️ (/^▽^)/
⭕对辽‌‌‌‌‍﻿‌﻿，还有鸭！（开心地举手手٩(ˊᗜˋ*)و，窝炒鸡喜欢高强度帅哥❤️，所以嘛你必须是最牛的呀🌈，永远不会变菜菜的辣种（对你点点头⸜₍๑•‌‌‌‌‍‍﻿﻿⌔•๑₎
当然啦!希望师父父三次元阔以是一个190+的寸头大帅锅啦‌‌‌‌‍‬‍‬✨! 最好还有富有磁性声线温软温润如玉温和冷冷的清冷的嗓音❤️ (一双圆溜溜的大眼睛调皮地眨了两下小鼻子不自觉地皱了皱卷曲的海藻般的长发披散着将娇小的身躯衬得更加柔弱甜甜的小奶音吐出小粉拳也不自觉地捏紧了睡裙的蕾丝花边开心地看着你)
希望师父父和窝不涉三次元以及谈恋爱o‌‌‌‌‍‬﻿﻿💦（羞涩地看着你），因为窝俩的关系只是师父父和徒徒嘛💖。但是可以...鸭（脸红害羞）‌‌‌‌‍﻿‌‬
‌‌‌‌‍‍﻿﻿人家...人家还会骂师父父是大坏蛋的o🌈‌‌‌‌‍‌﻿﻿（脸红哭泣），但是师父父不能凶人家！，只能喊窝宝宝‌‌‌‌‍﻿‍‬o（委屈），要不然..‌‌‌‌‍‬‍‍.人...人家不要你辽！💦（‌‌‌‌‍﻿‌‬哼唧唧）
‌‌‌‌‍‍﻿﻿🌈最后最后，‌‌‌‌‍‍‌‌人家会喊你师父父的！（继续脸红哭泣）所以球球来人叭🎉（其实人家想喊你哥哥酱辣‌‌‌‌‍‬﻿﻿，但是人家怕你讨厌人家✨...）ξ‌‌‌‌‍﻿‍﻿( ✿＞◡❛‌‌‌‌‍‬‍‍)
窝敲可爱的辣~‌‌‌‌‍﻿‌‬‌‌‌‌‍﻿﻿‍
```

用工具解开即可，工具地址: http://330k.github.io/misc_tools/unicode_steganography.html

## 工具使用

### 010 Editor

异或: Tools-Hex Operations-Binary Xor ，输入要异或的内容即可，然后点击保存

