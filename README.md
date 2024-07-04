# Pypi本地镜像服务器搭建


## 主要功能

- 全镜像同步(可以指定镜像源)
- 下载指定依赖包
- 定时同步 

## 快速开始
1. 安装依赖
```shell 
pip install schedule==1.2.2 pip2pi==0.8.2
```

2. 执行main.py
```shell
python main.py
```
此时可以看到packages目录下有所有的包和一个sample文件夹，如果需要在内网环境下使用，请把sample拷贝进内网机即可。


3.配置pypi索引服务器
可以使用python,也可以使用Nginx，Nginx配置可以查看[https://jhacker.cn/pypi_server](https://jhacker.cn/pypi_server)
```shell
#在下载目录里创建server服务，8080为端口号，可以随意设置：
cd packages
python -m http.server 8080
```
4.打开网页就可以看所有的包了
```html
http://localhost:8080/simple/
```
使用本地镜像服务器安装
```shell
pip install numpy -i http://localhost:8080/simple/
```

## 配置说明

- 具体配置文件可以查看config.json
- requirements.txt中内置了一些常用的依赖包，可以根据自己需求添加
- 如果想同步清华源全部依赖，可以执行```get_pypy_list.py```
- ```schedule_task.py```可以设置定时任务，每天/每周同步更新官方源

- **platform** 参数用于指定目标平台，以便下载与指定平台兼容的二进制包,以下是常见的配置内容：

|配置内容| 说明                                                  |
|--|-----------------------------------------------------|
|win32| Windows 32位系统                                       |
|win_amd64| Windows 64位系统（大多数人是这个）                              |
|win_arm64| Windows ARM64系统                                     |
|manylinux1_x86_64| 使用 manylinux1 标准构建的 Linux 64位系统（CentOS 5及更高版本兼容）    |
|manylinux2010_x86_64| 使用 manylinux2010 标准构建的 Linux 64位系统（CentOS 6及更高版本兼容） |
|manylinux2014_x86_64 | 使用 manylinux2014 标准构建的 Linux 64位系统（CentOS 7及更高版本兼容） |
|linux_i686| Linux 32位系统                                         |
|macosx_10_9_x86_64| macOS 10.9及更高版本的 Intel 64位系统                        |
|macosx_11_0_arm64| macOS 11.0及更高版本的 ARM64系统                            |

- **python_versions** 指的是python版本，只需要写大的版本号即可，如3.6、3.7、3.8、3.9等

