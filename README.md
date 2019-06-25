# Manager
美食管理服务端
### 部署服务端过程：

> 1.根据自己的操作系统按教程安装docker 参考：[docker安装与部署加速说明](Tech/16341023_docker.md)

> 2.获取镜像：
docker pull zfr0411/myrepository:myapp

> 3.启动镜像service服务，并设置端口映射：
docker run -itd -p X(未被占用的端口):5000 - -name mycontainer - -privileged zfr0411/myrepository:myapp init   

> 4.查看容器ID：docker ps -a。

> 5.进入mycontainer容器：docker exec -ti ID /bin/bash

> 6.cd到指定目录：cd root/myapp/test

> 7.执行命令运行程序：
  使用 uwsgi --ini uwsgi.ini 启动多进程
  使用 python3 manager.py runserver 启动单进程项目
