---
layout: post
title: 在阿里云ACE上部署Django应用
---

1. 将阿里云上的应用svn checkout到本地
    `svn co http://repo1.svn.ace.aliyun.com/svn/xxxx/xxx/1`

1. 在checkout下来的svn仓库中初始化git仓库

        git init
        git remote add origin ~/path/to/project/directory
        git fetch
        git checkout master

1.  设置ACE所需的环境
设置ACE的`index.py`文件. 在项目文件夹`ACEDjango`下的`wsgi.py`即是ACE所需的`index.py`, 我们需要将其拷贝到根目录中.

        git checkout -b deployment
        cp ACEDjango/wsgi.py index.py

    收集静态文件, 在`ACEDjango/settings.py`中设置`STATIC_ROOT`的位置为项目目录下的`static`目录中, 注意需要使用绝对路径.设置好路径后执行`python manage.py collectstatic`命令将项目内的静态文件都收集到该目录中.

    新建`requirements.txt`文件, 写入我们需要安装的python库, 在这里除了django以外我们还需要mysql-python用于mysql数据库的访问.

    此时的目录结构

    ├── ACEDjango
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── app.yaml
    ├── index.py
    ├── manage.py
    ├── polls
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── static
    │   ├── templates
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── requirements.txt
    └── static

1.  设置数据库
    接下来需要设置数据库用于访问, 在`ACEDjango/settings.py`中修改数据库相关设置如下：

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'XXXXX',
                'USER': 'XXXXX',
                'PASSWORD': 'XXXXXXXXXX',
                'HOST': 'XXXXX.mysql.rds.aliyuncs.com',
                'PORT': 3306,
            }
        }

    连接数据库所需的相关信息可以在ACE管理控制页面的扩展信息数据库页面中, 注意`NAME`一项不是数据库的实例名.
    在设置好数据库中参数后执行`python manage.py migrate`初始化数据库.

1. 上传代码并发布
    最后通过`svn commit`将项目代码上传到ACE中，并发布到网页上.
