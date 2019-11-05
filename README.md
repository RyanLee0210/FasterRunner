# FasterRunner

## 介绍

> 基于HttpRunner V1.0的Web系统项目

### 项目结构

```
└── FasterRunner    # 系统后端Django项目
    ├── docker-compose.md
    ├── Dockerfile    # FasterRunner镜像docker脚本文件
    ├── FasterRunner    # 根项目及配置模块
    ├── fastrunner    # 主功能模块
    ├── fastuser    # 用户管理模块
    ├── LICENSE
    ├── manage.py
    ├── nginx.conf
    ├── README.md
    ├── requirements.txt    # Django项目所需依赖
    ├── start.sh    # celery启动脚本
    ├── templates    # 报告模板文件
    └── uwsgi.ini

```

### 相关技术：

- Django：一个使用 Python 编写的Web 应用程序框架。
- Celery：是一个使用Python编写的异步任务的调度工具。

## 项目说明：

#### 目录说明

- `FasterRunner/`目录下是根项目目录，其中`setting.py`文件配置数据库连接、后台邮件账户、消息服务器连接等信息；并包含一些注册的应用模块；
- `fastrunner/`目录下是主要功能模块，接口测试的主要功能均在这个模块app中，对httprunner做二次封装，并主要提供http api供`FasterWeb`去调用；
- `requirements.txt`是项目文件依赖配置文件，手动开发调试时需要使用pip安装此依赖库。
- `start.sh`是docker容器运行时，会调用此脚本，启动celery相关进程，包括worker及beat进程；

## 项目开发编译和运行

```bash
第一步： 安装好mysql，创建setting.py中配置的数据库，并配置用户名和密码保证本项目可连接mysql指定的数据库；
第二步：创建数据库表和初始化数据；
# make migrations for fastuser、fastrunner
python3 manage.py makemigrations fastrunner fastuser
# migrate for database
python3 manage.py migrate fastrunner
python3 manage.py migrate fastuser
python3 manage.py migrate djcelery
第三步：启动django后台服务：
python3 manage.py runserver 0.0.0.0:8000

第四步：转向FasterWeb部署，成功后可通过web访问来验证此后台服务是否成功运行；

# 可选（主要是定时任务功能调试，Windows10可能存在兼容问题，建议在linux环境下调试此功能）
第五步：安装rabbitmq服务，用户名密码与setting.py中配置一致；
第六步：启动worker和beat进程；
# start celery worker
celery multi start w1 -A FasterRunner -l info --logfile=./logs/worker.log
# start celery beat
nohup python3 manage.py celery beat -l info > ./logs/beat.log 2>&1 &
```

