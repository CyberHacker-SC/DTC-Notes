# Linux 相关笔记（非 CTF）

# Docker

## 常用命令

```
#查看所有镜像
docker images


#查看所有容器
docker ps -a


#构建 Dockerfile
docker build --tag 想创建的镜像名称 .


#创建并启动一个容器实例（实例化一个镜像）
docker run -itd --name 自定义名称 镜像id /bin/bash
例如
docker run -itd --name ubuntu-test ubuntu /bin/bash
-i 交互式操作。
-t 终端。
-v /src/webapp:/usr/share/nginx/html 将主机的目录挂载到容器中
ubuntu: ubuntu 镜像。
/bin/bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash。
附加参数
-p 端口映射，例如 -p 5000:5000
--net=container:NAME_or_ID 指定。指定与某个容器实例共享网络。
--net=host 制定容器使用宿主机的网络
-e X=Y 添加环境变量，键 X 的值为 Y
--restart=always 当 docker 重启时，容器自动启动


#启动已创建的容器实例
docker start 容器id


#进入容器
docker exec -it 实例id /bin/bash


#退出容器
exit


#停止容器
docker stop 实例id


#重启容器
docker restart 实例id


#删除容器
docker rm -f 实例id


#删除镜像
docker image rm 镜像id


#导出容器
docker export 实例id > ubuntu.tar
上面ubuntu为文件名


#导入容器到镜像
cat ubuntu.tar | docker import - test/ubuntu:v1
上面ubuntu.tar是文件名


#将文件从docker容器拷贝到宿主机（反之亦然）
例如
docker cp mycontainer:/opt/testnew/file.txt /opt/test/


#查看容器运行情况
docker logs -f -t --tail 日志数量 实例id
```

# 科学上网

## v2ray

### 搭建

```bash
docker run -itd --restart=always --name v2ray -p 443:443 -p 80:80 -v $HOME/.caddy:/root/.caddy  pengchujin/v2ray_ws:0.11 cybersp1.thunderbolt.plus V2RAY_WS 0890b53a-e3d4-4726-bd2b-52574e8588c4
```

将 `0890b53a-e3d4-4726-bd2b-52574e8588c4` 这串 uuid 更换为自己的

### 设置另一台服务器反向代理

Caddyfile

```
cybersp4.thunderbolt.plus
{
  log ./caddy.log

	# v2ray 使用路径
  reverse_proxy /one https://cybersp3.thunderbolt.plus {
  	header_up Host {http.reverse_proxy.upstream.hostport}
  }
  
  # 使用反代网站伪装
  reverse_proxy /* https://ctf-wiki.org {
  	header_up Host {http.reverse_proxy.upstream.hostport}
  }
}
```

运行

```bash
docker run -itd --name reverse_v2ray --restart=always -p 443:443 -p 80:80 \
    -v $PWD/Caddyfile:/etc/caddy/Caddyfile \
    -v caddy_data:/data \
    caddy:2.7
```

- `$PWD` 会自动获取当前目录的路径
- 需要在宿主机创建一个 `caddy_data` 空目录