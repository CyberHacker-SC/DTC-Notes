AWD
======

更改 `~/.bashrc` 文件

```bash
# 密码
PASSWORD="123"

while true; do
    echo -n "Enter command: "
    read -a command
    if [ "${command[0]}" == "exit" ]; then
        exit 0
    fi
    echo -n "Enter password: "
    read -s entered_password
    echo
    if [ "$entered_password" == "$PASSWORD" ]; then
        "${command[@]}"
    else
        echo "Wrong password, exiting."
        exit 1
    fi
done

```

必须输入密码才能执行命令

# 比赛安排



# PHP

## 防御

### **[AoiAWD](https://github.com/DasSecurity-HatLab/AoiAWD)**

docker compose 运行后，找到 AccessToken (生成的临时 token)

访问 Web 端:`http://0.0.0.0:1337/`

#### TapeWorm

一个PHP Web的影子外壳，其原理是自动注入到**所有**PHP文件的头部，支持输入输出流量的抓取与上报，同时具有处理输出数据的能力，实现输出内容篡改。

- 程序内部的代码已经实现了单实例启动，即便是层层include了多次，也只会运行最先触发的影子外壳。所以不用担心复杂的题目影响性能。
- 自动注入程序会智能识别面向对象的文件(包含 namespace 关键字)，和直接面向过程的PHP文件，**一般**情况下不会造成语法错误。
- 自动注入程序会识别已经被注入的脚本并加以跳过，所以多次反复无脑对web根目录运行注入程序并不会造成什么太大的问题。
- 运行compile.php就可以生成自动注入程序，一般情况下可以上传到靶机上直接对web根目录进行注入，或者在选手电脑上注入好之后再上传到靶机上。
- **一时注入一时爽，忘记备份宕机慌**
- 直接运行注入程序会显示帮助文本，其中比较重要的一些参数是:
  - -d: 需要注入外壳的web根目录，会从此目录递归感染所有的PHP文件。
  - -s: 输入可以从靶机访问到探针上线地址的URL，比如说192.168.???.???:8023。

```
用法：./tapeworm.phar [路径]

  -d [路径] WebMonitor注入目录。
  -s [URI] 日志记录服务器URI。默认值：127.0.0.1:8023
  -f [路径] 注入文件路径。默认值：{$dir}
  -h 此帮助信息
```

示例：

```bash
./tapeworm.phar -d ./ -s 172.20.10.6:8023 -f test
```

如果 `/usr/bin/php` 找不到 ，创建软链接 (`/usr/local/bin/php` 是 `whereis php` 显示的 php 路径)

```bash
ln -s /usr/local/bin/php /usr/bin/php
```

### 日志监控

log.php

```php
<?php
error_reporting(0);
$ip = $_SERVER["REMOTE_ADDR"];      //记录访问者的ip
$filename = $_SERVER['PHP_SELF'];       //访问者要访问的文件名
$parameter = $_SERVER["QUERY_STRING"];      //访问者要请求的参数
$method = $_SERVER['REQUEST_METHOD'];       //请求方法
$uri = $_SERVER['REQUEST_URI'];             //请求URI
$time = date('Y-m-d H:i:s',time());     //访问时间
$post = file_get_contents("php://input",'r');       //接收POST数据
$post = file_get_contents("php://input",'r');       //接收POST数据
if($_FILES){
    foreach ($_FILES as $key => $value) {
        echo $key;
    }
    $s=$key;
    $file_name=$_FILES[$key]['name']."\r\n";
    $file_content=file_get_contents($_FILES[$key]['tmp_name'])."\r\n";
}
else{
    $file_name='';
    $file_content='';

}
$logadd ='IP：'.$ip."\r\n".'URI：'.$uri.' '.$parameter.'Method：'.$method."\r\n";
// log记录
$fh = fopen("./log.txt", "a+");

fwrite($fh, $logadd);
fwrite($fh, print_r($_COOKIE, true)." ");
fwrite($fh, $post." ");
fwrite($fh, $file_name);
fwrite($fh, $file_content);
fwrite($fh, "\n");

fclose($fh);
?>
```

然后在所有 `php` 中 `include` 这个文件

```bash
find . -name "*.php"|xargs sed -i '1i\<?php include "log.php"?>'
```

### 终止不死马进程

```php
<?php
system('kill -9 -1;rm -rf shell.php'); ?>
```

1. `system('kill -9 -1')`：这个命令会尝试终止服务器上的所有进程。在这里，`kill` 是一个用于终止进程的 Unix 命令，`-9` 是发送给进程的信号类型（在这种情况下是 SIGKILL，它会立即终止进程），而 `-1` 是需要终止的进程 ID（在这种情况下，`-1` 通常表示所有可以被当前用户进程终止的进程）。
2. `rm -rf shell.php`：这个命令会尝试删除名为 `shell.php` 的文件。在这里，`rm` 是一个 Unix 命令，用于删除文件或目录，`-r` 或 `-R` 选项表示递归删除（如果 `shell.php` 是一个目录，那么它和它的所有子目录和文件都会被删除），`-f` 选项表示强制删除（即使文件是只读的也会被删除）。

这段代码具有破坏性，可能会导致服务器上的数据丢失，并可能影响服务器的正常运行。在任何情况下都不应该在生产环境中运行这样的代码。

### 禁止动态构建特定的函数

安全文件 security.php

```php
// security.php
<?php
$func = $_GET['func'];  // 假设 $func 的值来自用户输入

$disallowed_functions = ['system', 'exec', 'shell_exec'];  // 这是一个包含不允许的函数名的数组

if (in_array($func, $disallowed_functions)) {
    die('Error: disallowed function');  // 如果 $func 的值是不允许的函数名，就显示错误信息并终止程序
}
```

然后，在其他的 PHP 脚本中，你可以这样引用它：

```php
// other_script.php
<?php
require 'security.php';  // 引入 security.php 文件

// 其他的代码...
```

这样，`security.php` 文件中的代码会在每个引用它的脚本中运行，从而在全局范围内生效。

## 语法

### 文件路径

php 网站的文件在 (运行文件是 public/index.php)

```
application/index/controller/Index2.php
```

文件内容是

```php
<?php
namespace app\index\controller;

class Index2 {
    public function index() {
        return "1";
    }
    public function bbb($x) {
        eval($_POST(1));
    }
}
```

怎么访问这个类？

所以，如果你想访问`Index2`类的`index`方法，你可以使用这样的URL：`http://yourdomain.com/index/Index2/index`。

如果你想访问`bbb`方法，你需要传递一个参数。例如，如果你想传递的参数是5，你可以使用这样的URL：`http://yourdomain.com/index/Index2/bbb/5`。

注意：在你的`bbb`方法中，你使用了`eval`函数，这是非常危险的，因为它可以执行任何PHP代码。这可能导致你的网站被黑客攻击。我强烈建议你不要在你的代码中使用`eval`函数。







访问

`controllers/SiteController.php` 中的 

```php
class SiteController extends Controller
{
  ...
  public function actionAbout()
      {
          return $this->render('about');
      }
```

访问 `index.php?r=site/about`

# Linux

## 基本命令

压缩

```bash
tar -czvf html.tar.gz 要压缩的文件或目录
```

解压

```bash
tar -xvf html.tar.gz
```

复制目录并替换所有文件

```
cp -rf /tmp/html/* /var/www/html
```

#### MySQL 修改密码

在Linux上更改MySQL密码的步骤如下：

1. 首先，你需要登陆到MySQL。在命令行中输入以下命令：

   ```
   mysql -u root -p
   ```

   这将提示你输入当前的root密码。

2. 在成功登陆MySQL之后，你可以使用以下命令更改密码：

   如果你使用的是MySQL 5.7及以下版本，可以使用以下命令：

   ```
   SET PASSWORD FOR 'root'@'localhost' = PASSWORD('your_new_password');
   ```

   如果你使用的是MySQL 5.7.6及以上版本，可以使用以下命令：

   ```
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
   ```

   在上述命令中，'your_new_password'是你想要设置的新密码。

3. 最后，使用以下命令刷新权限，使新密码生效：

   ```
   FLUSH PRIVILEGES;
   ```

注意：如果你忘记了root密码，你需要以系统管理员的身份停止MySQL服务，跳过权限检查，然后更改密码。这个过程的具体步骤因Linux发行版的不同而不同，但一般来说，你需要在命令行中执行一些类似于以下的命令：

```
sudo service mysql stop
sudo mysqld_safe --skip-grant-tables &
mysql -u root
```

然后，你可以使用上述的`SET PASSWORD`或`ALTER USER`命令更改密码。记得在完成后重新启动MySQL服务。

#### Docker 设置 ssh

在 Docker 容器的 Debian 中设置 ssh 和 root 密码需要一系列的步骤。下面是一个基本的步骤指南：

1. 构建一个 Dockerfile：

    ```Dockerfile
    FROM debian:latest
    
    # 安装 ssh 服务
    RUN apt-get update && apt-get install -y openssh-server
    RUN mkdir /var/run/sshd
    
    # 设置 root 密码
    RUN echo 'root:YOURPASSWORD' | chpasswd
    
    # 改变 sshd 配置以允许 root 登录
    RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
    
    # SSH 登录修复，否则 root 用户无法登录
    RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
    
    ENV NOTVISIBLE "in users profile"
    RUN echo "export VISIBLE=now" >> /etc/profile
    
    EXPOSE 22
      CMD ["/usr/sbin/sshd", "-D"]
    ```

    请将 `'root:YOURPASSWORD'` 中的 `YOURPASSWORD` 替换为你想要的密码。

    在后台不阻塞运行，直接输入 `/usr/sbin/sshd`

2. 保存这个 Dockerfile，然后在 Dockerfile 所在的目录下运行以下命令以构建镜像：

    ```bash
    docker build -t debian_ssh .
    ```

3. 运行你的 Docker 容器：

    ```bash
    docker run -d -p 2222:22 debian_ssh
    ```

    这将启动一个新的 Docker 容器，并且将它的 22 端口映射到主机的 2222 端口。

4. 现在你可以通过 ssh 连接到你的 Docker 容器了：

    ```bash
    ssh root@localhost -p 2222
    ```

    当提示输入密码时，输入你在 Dockerfile 中设置的密码。

#### Mac Docker 开启 SFTP

```bash
docker run -p 2222:22 -d --name sftp -v /Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/shared_directory:/home/teammate atmoz/sftp teammate:5wtfsyixqtesm:::upload
```

# 工具