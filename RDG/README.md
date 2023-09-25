# RDG 防御实战

# 基本命令备用

查看进程的运行目录，例如

```	bash
ps -ef | grep java
```

下载

```bash
sz + 文件名
```

上传

```
rz
```

提交压缩包的格式

```bash
tar zcvf update.tar.gz update.sh file1 file2
```

覆盖

```bash
cp -rf b/* a
```



# 常见漏洞修复

## Java

### Tomcat

#### ajp 文件包含漏洞

Apache Tomcat的AJP协议有一些已知的漏洞，其中包括CVE-2020-1938（也被称为Ghostcat）。以下是一些修复这些漏洞的一般步骤：

1. **升级Tomcat版本**：这是最直接的解决方案。对于CVE-2020-1938，Apache已经在9.0.31、8.5.51和7.0.100版本中修复了这个问题。你只需要下载并安装这些版本或更高版本的Tomcat即可。

2. **禁用AJP协议**：如果你的应用不使用AJP协议，可以选择禁用它。在`conf/server.xml`文件中找到AJP Connector相关的配置，然后将其注释掉或者删除。例如，你可能会看到像这样的配置：

    ```xml
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
    ```

    你可以将其注释掉，像这样：

    ```xml
    <!-- <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" /> -->
    ```

3. **限制AJP Connector的访问**：如果你需要使用AJP协议，但是又想保护你的系统不受到这个漏洞的影响，你可以限制哪些IP地址可以访问AJP Connector。在`conf/server.xml`文件中找到AJP Connector相关的配置，然后添加`address`属性。例如，如果你只想让本机可以访问，你可以这样配置：

    ```xml
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" address="localhost" />
    ```

4. **设置`requiredSecret`属性**：在Tomcat 9.0.31、8.5.51和7.0.100版本中，Apache引入了一个新的`requiredSecret`属性，可以用来为AJP协议设置一个必需的秘密。这可以防止未经授权的AJP协议请求。你可以在`conf/server.xml`文件中找到AJP Connector相关的配置，然后添加`requiredSecret`属性。例如：

    ```xml
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" requiredSecret="your_secret" />
    ```

这些步骤可以帮助你修复Apache Tomcat的AJP协议漏洞。然而，你还应该保持对新的安全漏洞的关注，并定期更新你的系统和软件，以保持最高的安全性。

