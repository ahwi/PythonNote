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
mongod --port 27017 --dbpath c:\data\db
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

### 认证方式

* authencation: 验证用户的身份
* authorization:授权决定用户对资源和操作的访问权限

#### 用户管理界面

可以用`db.createUser()`方法来创建用户，可以给user赋值roles来赋予权限





### 用户配置

#### 给用户添加已有数据库的权限

链接:<https://docs.mongodb.com/manual/reference/method/db.grantRolesToUser/>

```
db.grantRolesToUser( "<username>", [ <roles> ], { <writeConcern> } )

eg.
use products
db.grantRolesToUser(
   "accountUser01",
   [ "readWrite" , { role: "read", db: "stock" } ],
)
```



### 查询语句

```
# 查询
比如要查询每个班级的男生
db.school.aggregate([{$match:{sex:"男"}}, {$group:{_id:"$class"}}])
```



## mongodb手册



### 安全

1. mongodb提供了一些不同的特性来确保mongodb的安全性

* Authentication 认证
  * authentication
  * SCRAM
  * x.509
* Authorization 授权
  * Role-Based Access Control
  * Enable Access Control
  * Manage Users and Roles
* TLS/SSL
  * TLS/SSL(Transport Encryption)
  * Configure mongod and mongos for TLS/SSL
  * TLS/SSL Configuration for Clients
* Encryption
  * Client-Side Filed Level
  * Encryption
* Enterprise Only
  * 略

2. 安全检查列表

* <https://docs.mongodb.com/manual/administration/security-checklist/>

#### 安全检查列表

##### 制作前检查清单/注意事项

###### 启用访问控制并强制执行身份验证

启动访问控制并指定认证方案等

###### 配置基于角色的访问控制

首先创建一个用户管理员，然后创建其他用户。 为访问系统的每个人/应用程序创建一个唯一的MongoDB用户。


遵循最小特权原则。 创建角色，以定义一组用户所需的确切访问权限。 然后创建用户，并仅为其分配执行操作所需的角色。 用户可以是个人或客户端应用程序。

> 提示:
>
> 用户可以在不同的数据库之间拥有特权。 如果用户需要对多个数据库的特权，请创建一个具有授予适用数据库特权的角色的单个用户，而不是在不同的数据库中多次创建该用户。



#### 认证方式

##### 用户

* 用户管理界面
* 认证数据库
* 验证用户
* 集中的用户数据
* 分片群集用户
* Localhost异常

**用户管理界面**

MongoDB提供`db.createUser()`方法来添加用户。当添加用户的时候给他分配角色roles来赋予对应的权限。

可以对存在的用户执行修改密码、赋予或撤回对应的角色。详见[User Management](https://docs.mongodb.com/manual/reference/method/#user-management-methods).

用户以用户名和关联的身份验证数据库为唯一标识。

**认证数据库**

添加用户时，可以在特定数据库中创建该用户。 该数据库是用户的<font color=red>身份认证数据库</font>。

<font color=red>用户可以在不同的数据库之间拥有特权</font>； 也就是说，用户的权限不限于其身份验证数据库。 通过分配其他数据库中的用户角色，在一个数据库中创建的用户可以具有对其他数据库执行操作的权限。 有关角色的更多信息，请参见[Role-Based Access Control](https://docs.mongodb.com/manual/core/authorization/)。

用户名和身份验证数据库是该用户的唯一标识符。 也就是说，如果两个用户具有相同的名称，但在不同的数据库中创建，则它们是两个单独的用户。<font color=blue> 如果打算让一个用户在多个数据库上具有权限，请在合适的数据库中创建一个具有角色的单个用户，而不是在不同的数据库中多次创建该用户。</font>

**验证用户**

要验证用户必须提供用户名、密码以及关联的认证数据库

* 使用mongo shell的方式认证

  * 使用对应的选项：

    [`--username`](https://docs.mongodb.com/manual/reference/program/mongo/#cmdoption-mongo-username), [`--password`](https://docs.mongodb.com/manual/reference/program/mongo/#cmdoption-mongo-password), and [`--authenticationDatabase`](https://docs.mongodb.com/manual/reference/program/mongo/#cmdoption-mongo-authenticationdatabase)

  * 先连接再认证

    * db.auth( "username", passwordPrompt() )
    * db.auth( "username", "password" )

    > 重要
    >
    > 以不同用户身份进行多次身份验证不会删除先前已身份验证的用户的凭据。 这可能导致连接具有比用户预期更多的权限，并导致逻辑会话中的操作引发错误。

* 使用MongoDB driver来认证

  see the [driver documentation](https://docs.mongodb.com/ecosystem/drivers/)

> 分片本地用户

某些维护操作（例如cleanupOrphaned，compact，rs.reconfig（））需要直接连接到分片群集中的特定分片。 要执行这些操作，您必须直接连接到分片并以分片本地管理用户身份进行身份验证。

要创建分片本地管理用户，请直接连接到分片并创建该用户。 MongoDB将分片本地用户存储在分片本身的管理数据库中。

这些分片本地用户与通过mongos添加到分片集群的用户完全独立。 分片本地用户是分片本地用户，mongos无法访问。

与分片的直接连接仅应用于分片特定的维护和配置。 通常，客户端应通过mongos连接到分片群集。

**Localhost 异常**

本地主机异常允许你在启用访问控制后在系统中创建第一个用户。在启用访问控制后，localhost异常允许你连接到本地主机接口并在admin数据库中创建第一个用户。第一个用户必须具有创建其他用户的特权，例如具有userAdmin或userAdminAnyDatabase角色的用户。使用localhost异常的连接只有在admin数据库上创建第一个用户的权限。

在版本3.4中进行了更改：MongoDB 3.4扩展了localhost异常，以允许执行db.createRole（）方法。该方法允许用户通过LDAP授权在MongoDB内部创建一个角色，该角色映射到LDAP中定义的角色。有关更多信息，请参见LDAP授权。

localhost异常仅在MongoDB实例中没有创建用户的情况下适用。

对于分片群集，localhost异常适用于每个分片，也适用于整个群集。创建分片集群并通过mongos实例添加用户管理员后，您仍然必须防止未经授权的访问各个分片。对群集中的每个分片执行以下步骤之一：

* 创建一个管理用户，或
* 在启动时禁用localhost异常。要禁用localhost异常，请将enableLocalhostAuthBypass参数设置为0。



**集中的用户数据**

对于在MongoDB中创建的用户，MongoDB将所有用户信息（包括名称，密码和用户的身份验证数据库）存储在admin数据库的system.users集合中。

不要直接访问此集合，而要使用用户管理命令（ [user management commands](https://docs.mongodb.com/manual/reference/command/#user-management-commands)）。

**分片集群用户**

要为分片群集创建用户，请连接到[mongos](https://docs.mongodb.com/manual/reference/program/mongos/#bin.mongos) 实例并添加用户。 然后，客户端通过mongos实例对这些用户进行身份验证。 在分片群集中，MongoDB将用户配置数据存储在配置服务器（ [config servers](https://docs.mongodb.com/manual/reference/glossary/#term-config-server)）的admin数据库中。



###### 添加用户

* 总览
* 先决条件
* 例子
* 用户名/密码认证
* Kerberos身份验证
* LDAP验证
* x.509客户端证书认证 

**1. 总览**

MongoDB使用基于角色的访问控制（RBAC）来确定用户的访问权限。 授予用户一个或多个角色，这些角色确定用户对MongoDB资源的访问或特权以及用户可以执行的操作。 用户应仅具有确保系统具有最低特权所需的最小特权集。

MongoDB系统的每个应用程序和用户都应映射到不同的用户。 这种访问隔离有助于访问撤消和持续的用户维护。

**2. 先决条件**

如果为部署启用了访问控制，则可以使用localhost异常在系统中创建第一个用户。 该第一个用户必须具有创建其他用户的特权。 从MongoDB 3.0开始，在localhost异常中，您只能在admin数据库上创建用户。 创建第一个用户后，必须以该用户身份进行身份验证后才能添加后续用户。" 启用访问控制（[Enable Access Control](https://docs.mongodb.com/manual/tutorial/enable-authentication/)）" -- 提供有关在部署启用访问控制时添加用户的更多详细信息。

对于常规用户创建，您必须拥有以下权限：

* 要在数据库中创建新用户，您必须对该数据库资源执行[`createUser`](https://docs.mongodb.com/manual/reference/privilege-actions/#createUser)操作([action](https://docs.mongodb.com/manual/reference/privilege-actions/#security-user-actions))。
* 要向用户授予角色，您必须对角色的数据库执行[`grantRole`](https://docs.mongodb.com/manual/reference/privilege-actions/#grantRole)操作。

[`userAdmin`](https://docs.mongodb.com/manual/reference/built-in-roles/#userAdmin) 和[`userAdminAnyDatabase`](https://docs.mongodb.com/manual/reference/built-in-roles/#userAdminAnyDatabase) 内置角色在其各自的资源上提供createUser和grantRole操作。

**3. 例程**

可以使用 [`db.createUser()`](https://docs.mongodb.com/manual/reference/method/db.createUser/#db.createUser)和[`createUser`](https://docs.mongodb.com/manual/reference/command/createUser/#dbcmd.createUser)命令来创建用户

**3.1 用户名/密码认证**

下面用来在reporting数据库中创建一个用户

```
use reporting
db.createUser(
  {
    user: "reportsUser",
    pwd: passwordPrompt(),  // or cleartext password
    roles: [
       { role: "read", db: "reporting" },
       { role: "read", db: "products" },
       { role: "read", db: "sales" },
       { role: "readWrite", db: "accounts" }
    ]
  }
)
```



**4. Kerberos身份验证**

**5. LDAP验证**

**6. x.509客户端证书认证**









## 相关阅读

博客

https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

多线程连接的相关问题:

<https://juejin.im/post/5a3b1e9c51882515945abedf>



