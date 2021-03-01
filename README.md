# 基于 Flask 的论坛


**地址：** 
- https://www.dili361.xyz/

**测试账号：** 
- 用户名：`abc` 
- 密码：`123`


**简介**
-
- 实现用户登录，注册，找回密码，发帖回帖，个人主页，站内信和更改头像等功能。
- 使用 `MySQL` 存储数据，基于 `SQLAlchemy` 实现 `ORM` 。
- 基于 `Redis` 实现 `Session` `CSRF token` 在多进程下的数据共享。
- 对个人主页基于 `Redis` 进行了缓存优化，利用 `Join` 语句解决了查询数据库过程中的 `N+1` 问题。
- 应用 `Jinja2` 模板继承复用 `HTML` 页面通用元素，提高开发效率。
- 使用 `JavaScript` 脚本实现 `Markdown` 渲染和语法高亮。
- 使用 `nginx` 反向代理静态资源，`Supervisor` 进行进程守护，`Gunicorn` 实现多worker负载均衡，`gevent` 开启协程提高并发性能。
- 基于 `Celery` 和 `Redis` 实现消息队列，处理高并发请求并保证数据安全。
- 编写 `Shell` 脚本，在 `Linux` 服务器上实现一键部署。


**功能演示**
- 
- 注册/登录
![login.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/index.gif)

- 发帖/回帖
![topic.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/topic.gif)

- 修改个人资料
![setting.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/setting.gif)

- 站内信
![mail.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/mail.gif)

- 重置密码
![reset_pass.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/reset_pass.gif)

- 个人主页
![profile.gif](https://github.com/geita6/SQLAlchemy_bbs/blob/master/static/profile.gif)


**依赖**
-
- Ubuntu 18.04
- Python 3.6

