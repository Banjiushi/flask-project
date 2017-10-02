# flask-project

### 使用flask和bootstrap搭建了一个简易问答平台
a) 技术范畴：flask，bootstrap  
b) 实现细节：一个基于flask及bootstrap的简单的仿知乎问答平台；支持登录，注册，发布问题，回答问题，查找答案等。  
c) 项目特色：flask实现，灵活、易扩展；bootstrap搭建，简单易学。

### 流程
结构搭建 --> 导航条 --> 模板分离 --> 登录页面 --> 注册页面 --> User模型 --> 注册功能 --> 登录功能 --> 登录注销状态切换 --> 发布问答界面（视图函数） --> 

执行数据库相关操作时报错：  
```
ModuleNotFoundError: No module named 'MySQLdb'
```
安装 mysqlclient 后解决