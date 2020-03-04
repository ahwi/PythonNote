# mongo

## 安装与配置

下载地址：<https://www.mongodb.com/download-center/community>

### 安装

**创建数据库目录：**

```cmd
c:\>cd c:\
c:\>mkdir data
c:\>cd data
c:\data>mkdir db
c:\data>cd db
c:\data\db>
```

**命令行下运行MongoDB服务器**

```
C:\mongodb\bin\mongod --dbpath c:\data\db
```

**连接db**

```
C:\mongodb\bin\mongo.exe
```

### 配置

**创建目录(管理员权限)：**

```
mkdir c:\data\db
mkdir c:\data\log
```

**创建配置文件：**

 `C:\mongodb\mongod.cfg`

```
systemLog:
    destination: file
    path: c:\data\log\mongod.log
storage:
    dbPath: c:\data\db
```

**安装MongoDB服务：**

```
C:\mongodb\bin\mongod.exe --config "C:\mongodb\mongod.cfg" --install
```

**启动/关闭 /移除 MongoDB服务：**

```
net start MongoDB
net stop MongoDB
C:\mongodb\bin\mongod.exe --remove
```

### 创建管理员用户

参考：<https://www.jianshu.com/p/c5f778adfbb3>

**1. 新建Mongodb服务:**

```
mongod --port 27017 --dbpath /data/db1
```

**2. 开启mongodb客户端shell：**

````
mongo --port 27017

use admin
> db.createUser(
... {
... user:"adminUser",
... pwd:"adminPass",
... roles:[{role:"userAdminAnyDatabase", db:"admin"}]
... }
... )

````

管理员创建成功，现在拥有了用户管理员
用户名：adminUser
密码：adminPass
然后，断开 mongodb 连接， 关闭数据库

启动带访问控制的Mongodb:

```
mongod --auth --port 27017 --dbpath c:\data\db
```



**3. Mongodb用户验证登录**

两种登录方式:

* 客户端连接时，指定用户名，密码，db名称 (类似mysql)

  ```
  mongo --port 27017 -u "adminUser" -p "adminPass" --authenticationDatabase "admin"
  ```

* 客户端连接后，再进行验证

  ```
  mongo --port 27017
  
  use admin
  db.auth("adminUser", "adminPass")
  // 输出 1 表示验证成功
  ```

**4. 创建普通用户**

```
use foo

db.createUser(
  {
    user: "simpleUser",
    pwd: "simplePass",
    roles: [ { role: "readWrite", db: "foo" },
             { role: "read", db: "bar" } ]
  }
)
```

现在我们有了一个普通用户
用户名：simpleUser
密码：simplePass
权限：读写数据库 foo， 只读数据库 bar。

<font color=red>注意:</font>
 `use foo`表示用户在 foo 库中创建，就一定要 foo 库验证身份，即用户的信息跟随随数据库。比如上述 simpleUser 虽然有 bar 库的读取权限，但是一定要先在 foo 库进行身份验证，直接访问会提示验证失败。

```
use foo
db.auth("simpleUser", "simplePass")

use bar
show collections
```

**5. 内建角色**

* Read：允许用户读取指定数据库

* readWrite：允许用户读写指定数据库

* dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile

* userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户

* clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。

* readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限

* readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限

* userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限

* dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。

* root：只在admin数据库中可用。超级账号，超级权限



## pyhon连接远程monog

```python
from sshtunnel import SSHTunnelForwarder
import pymongo
import pprint

ssh_username = 'root'
ssh_password = 'root'
ssh_port = 21

MONGO_HOST = 'xxx.xxx.xxx.xxx' # host
MONGO_DB = "test"
MONGO_USER = "root"
MONGO_PASS = "root"
MONGO_PORT = 1234



server = SSHTunnelForwarder(
    (MONGO_HOST, ssh_port),
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    remote_bind_address=('127.0.0.1', MONGO_PORT) # 
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)
pprint.pprint(db.collection_names())

server.stop()
```



## 数据库操作

### 查询语句

```
# 查询
比如要查询每个班级的男生
db.school.aggregate([{$match:{sex:"男"}}, {$group:{_id:"$class"}}])
```



## 相关阅读

博客

https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

多线程连接的相关问题:

<https://juejin.im/post/5a3b1e9c51882515945abedf>



