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

### 查询语句

```
# 查询
比如要查询每个班级的男生
db.school.aggregate([{$match:{sex:"男"}}, {$group:{_id:"$class"}}])
```



## mongodb手册

链接：<https://docs.mongodb.com/manual/>

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

###### 开启访问控制和强制验证

选择认证机制并开启访问控制，之后所有连接系统的客户端和服务都必须提供有效的认证。

See [Authentication](https://docs.mongodb.com/manual/core/authentication/) and [Enable Access Control](https://docs.mongodb.com/manual/tutorial/enable-authentication/).

###### 配置基于角色的访问控制

首先创建一个用户管理员，然后创建其他用户。 为访问系统的每个人/应用程序创建一个唯一的MongoDB用户。

遵循最小特权原则。 创建角色，以定义一组用户所需的确切访问权限。 然后创建用户，并仅为其分配执行操作所需的角色。 用户可以是个人或客户端应用程序。

> 提示：
>
> 用户可以在不同的数据库之间拥有特权。 如果用户需要对多个数据库的特权，请创建一个具有授予适用数据库特权的角色的单个用户，而不是在不同的数据库中多次创建该用户。

See [Role-Based Access Control](https://docs.mongodb.com/manual/core/authorization/) and [Manage Users and Roles](https://docs.mongodb.com/manual/tutorial/manage-users-and-roles/).

###### 加密通讯（TLS / SSL）

配置MongoDB使用TLS/SSL来加密连接。使用TSL/SSL来加密mongod和mongos组件之间的通信。

See [Configure mongod and mongos for TLS/SSL](https://docs.mongodb.com/manual/tutorial/configure-ssl/).

###### 加密和保护数据

  从MongoDB Enterprise 3.2开始，您可以使用WiredTiger存储引擎的本机静态加密来加密存储层中的数据。
  如果您不使用WiredTiger的加密功能，则应在每个主机上使用文件系统，设备或物理加密（例如dm-crypt）对MongoDB数据进行加密。 使用文件系统权限保护MongoDB数据。 MongoDB数据包括数据文件，配置文件，审核日志和密钥文件。
  将日志收集到中央日志存储中。 这些日志包含DB身份验证尝试，包括源IP地址。



###### 限制网络暴露

确保MongoDB在受信任的网络环境中运行，并配置防火墙或安全组以控制MongoDB实例的入站和出站流量。

仅允许受信任的客户端访问可使用MongoDB实例的网络接口和端口。 例如，使用IP白名单来允许从受信任的IP地址进行访问（请参阅参考资料）



###### 审核系统活动

跟踪对数据库配置和数据的访问和更改。 MongoDB 企业版 包含系统审核工具，可以记录MongoDB实例上的系统事件（例如，用户操作，连接事件）。 这些审核记录可以进行分析，并允许管理员验证适当的控制措施。 您可以设置过滤器以记录特定事件，例如身份验证事件。

See [Auditing](https://docs.mongodb.com/manual/core/auditing/) and [Configure Auditing](https://docs.mongodb.com/manual/tutorial/configure-auditing/).

###### 用专用用户运行MongoDB

使用专用的操作系统用户帐户运行MongoDB进程。 确保该帐户具有访问数据的权限，但没有不必要的权限。

See [Install MongoDB](https://docs.mongodb.com/manual/installation/) for more information on running MongoDB.

###### 使用安全配置选项运行MongoDB

  MongoDB支持对某些服务器端操作执行JavaScript代码：mapReduce和$ where。 如果不使用这些操作，请在命令行上使用--noscripting选项禁用服务器端脚本。
  保持输入验证启用。 默认情况下，MongoDB通过net.wireObjectCheck设置启用输入验证。 这样可以确保mongod实例存储的所有文档都是有效的BSON。

SEE

[Network and Configuration Hardening](https://docs.mongodb.com/manual/core/security-hardening/).

###### 索取《安全技术实施指南》（如果适用）

  《安全技术实施指南》（STIG）包含美国国防部内部署的安全指南。 MongoDB Inc.可根据需要提供STIG，以供需要时使用。 请索取更多信息。

###### 考虑符合安全标准

  对于需要符合HIPAA或PCI-DSS要求的应用程序，请参考MongoDB安全参考架构，以了解更多有关如何使用关键安全功能来构建兼容的应用程序基础结构的信息。

###### 定期/正在进行的生产检查

定期检查MongoDB产品CVE并升级您的产品。请咨询MongoDB生命周期终止日期并升级您的MongoDB安装。 通常，尝试保持最新版本。

确保您的信息安全管理系统策略和过程扩展到MongoDB安装，包括执行以下操作：

- 定期将补丁应用到您的计算机并查看准则。
- 查看策略/过程更改，尤其是对网络规则的更改，以防止MongoDB意外暴露于Internet。
- 查看MongoDB数据库用户并定期轮换他们。



#### 启用访问控制

- 总览
- 用户管理员
- 过程
- 其他注意事项

**总览**

在MongoDB部署上启用访问控制会强制执行身份验证，要求用户标识自己。 访问启用了访问控制的MongoDB部署时，用户只能执行由其角色确定的操作。

以下教程在独立的mongod实例上启用访问控制，并使用默认的身份验证机制。 有关所有受支持的身份验证机制，请参阅身份验证机制。

**用户管理员**

启用访问控制后，请确保您在管理数据库中拥有一个具有userAdmin或userAdminAnyDatabase角色的用户。 该用户可以管理用户和角色，例如：创建用户，向用户授予或撤消角色，以及创建或修改定制角色。

**过程**

以下过程首先将用户管理员添加到在没有访问控制的情况下运行的MongoDB实例，然后启用访问控制。

> 示例MongoDB实例使用端口27017和数据目录/ var / lib / mongodb目录。 该示例假定数据目录为/ var / lib / mongodb。 根据需要指定其他数据目录。

1. 启动没有访问控制的MongoDB

   启动一个没有访问控制的Mongodb实例

   ```shell
   mongod --port 27017 --dbpath /var/lib/mongodb
   ```

2. 连接实例

   ```shell
   mongo --port 27017
   ```

3. 创建管理员用户

   在mongo shell中，在admin数据库中添加一个具有userAdminAnyDatabase角色的用户。 包括此用户所需的其他角色。 例如，以下代码在user数据库中使用userAdminAnyDatabase角色和readWriteAnyDatabase角色创建用户myUserAdmin。

   > 提示:
   >
   > 从mongo Shell的4.2版本开始，您可以将passwordPrompt（）方法与各种用户身份验证/管理方法/命令结合使用以提示输入密码，而不是直接在方法/命令调用中指定密码。 但是，仍然可以像使用早期版本的mongo shell一样直接指定密码。

   ```shell
   use admin
   db.createUser(
     {
       user: "myUserAdmin",
       pwd: passwordPrompt(), // 或者直接写明文密码
       roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
     }
   )
   
   # 自己的密码:123456
   ```

   > 注意
   >
   > 在其中创建用户的数据库（在本示例中为admin）是用户的身份验证数据库。 尽管用户将对此数据库进行身份验证，但是该用户可以拥有其他数据库中的角色(role)； 即用户的身份验证数据库不限制用户的权限。

4. 使用访问控制重新启动MongoDB实例

   a. 关闭mongod实例。 例如，在mongo shell中，发出以下命令：

   ```shell
   db.adminCommand({shutdown:1})
   ```

   b. 退出mongo shell

   c. 启动访问控制的mongod

   - 如果是使用命令行来启动mongod，添加--auth选项：

     ```shell
     mongod --auth --port 27017 --dbpath /var/lib/mongodb
     ```

   - 如果是使用配置文件来启动mongod，在配置文件中添加security.authorization配置选项：

     ```ini
     security:
         authorization: enabled
     ```

   现在，连接到该实例的客户端必须将自己认证为MongoDB用户。 客户只能执行由其分配的角色确定的操作。

5. 以用户管理员身份连接并进行身份验证

   使用mongo shell有两种连接方式：

   - 通过传递用户凭据进行身份验证来连接

     ```shell
     mongo --port 27017  --authenticationDatabase "admin" -u "myUserAdmin" -p
     ```

   - 先连接而不进行身份验证，然后发出db.auth（）方法进行身份验证。

     ```shell
     mongo --port 27017
     use admin
     db.auth("myUserAdmin", passwordPrompt()) // or cleartext password
     ```

#### 认证方式

- 认证方式
- 认证机制
- 内部认证
- 分片群集上的身份验证

身份验证是验证客户端身份的过程。 启用访问控制（即授权）后，MongoDB要求所有客户端进行身份验证才能确定其访问权限。

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





## MongoDB权威指南

### 第五章 索引

#### 5.1 索引简介

* 创建索引

  ```
  db.users.ensureIndex({"username" : 1})
  ```

* 查看索引的创建进度

  * db.currentOp() 执行shell命令
  * 查看mongod的日志

* 创建索引的代价：

  * 每次写操作（插入、更新、删除）不仅要更新文档，还需要更新集合上的索引，将耗费更多的时间
  * MongoDB 限制每个集合上最多只能有 64 个索 引
  * 通常，在一个特定的集合上，<font color=red>不应该拥有两个以上的索引</font>。

##### 5.1.1 复合索引简介

1. 简介：主要说明索引创建顺序导致查询效率的不同

2. 建立复合索引:

   ```
   db.users.ensureIndex({"age" : 1, "username" : 1})
   ```

   这里先根据age排序再根据username进行排序，索引username在这里发挥的作用并不大

3. 例子：

   假设有一个users集合，在这个集合上执行一个不排序的查询：

    ```
    > db.users.find({}, {"_id" : 0, "i" : 0, "created" : 0}) 
    { "username" : "user0", "age" : 69 } 
    { "username" : "user1", "age" : 50 } 
    { "username" : "user2", "age" : 88 } 
    { "username" : "user3", "age" : 52 } 
    { "username" : "user4", "age" : 74 } 
    { "username" : "user5", "age" : 104 } 
    { "username" : "user6", "age" : 59 }
    { "username" : "user7", "age" : 102 } 
    { "username" : "user8", "age" : 94 } 
    { "username" : "user9", "age" : 7 } 
    { "username" : "user10", "age" : 80 } 
    ...
    ```

   如果使用`{"age" : 1， "username" : 1} `建立索引，这个索引大概是这样子的

    ```
    [0, "user100309"] -> 0x0c965148 
    [0, "user100334"] -> 0xf51f818e 
    [0, "user100479"] -> 0x00fd7934 
    ... 
    [0, "user99985" ] -> 0xd246648f 
    [1, "user100156"] -> 0xf78d5bdd 
    [1, "user100187"] -> 0x68ab28bd 
    [1, "user100192"] -> 0x5c7fb621 
    ... 
    [1, "user999920"] -> 0x67ded4b7 
    [2, "user100141"] -> 0x3996dd46 
    [2, "user100149"] -> 0xfce68412 
    [2, "user100223"] -> 0x91106e23 
    ...
    ```

   这里的 "age" 字段是严格升序排列的，"age" 相同的条目按照 "username" 升序排列。每 个 "age" 都有大约 8000 个对应的 "username"，这里只是挑选了少量数据用于传 达大概的信息。

   3.1 MongoDB 对这个索引的使用方式取决于查询的类型。下面是三种主要的方式:

   * db.users.find({"age" : 21}).sort({"username" : -1}) 

     这是一个点查询（point query），用于查找单个值（尽管包含这个值的文档可能有 多个）。由于索引中的第二个字段，查询结果已经是有序的了：MongoDB 可以从 {"age" : 21} 匹配的最后一个索引开始，逆序依次遍历索引：

        ```
        [21, "user999977"] -> 0x9b3160cf 
        [21, "user999954"] -> 0xfe039231 
        [21, "user999902"] -> 0x719996aa 
        ...
        ```

        这种类型的查询是非常高效的：MongoDB 能够直接定位到正确的年龄，而且不需要对结果进行排序（因为只需要对数据进行逆序遍历就可以得到正确的顺序了）。 
        注意，排序方向并不重要：MongoDB 可以在任意方向上对索引进行遍历。

    * db.users.find({"age" : {"$gte" : 21， "$lte" : 30}})

      这是一个多值查询（multi-value query），查找到多个值相匹配的文档（在本例 中，年龄必须介于 21 到 30 之间）。MongoDB 会使用索引中的第一个键 "age" 得到匹配的文档，如下所示：

      ```
      [21, "user100000"] -> 0x37555a81 
      [21, "user100069"] -> 0x6951d16f 
      [21, "user1001"]   -> 0x9a1f5e0c 
      [21, "user100253"] -> 0xd54bd959 
      [21, "user100409"] -> 0x824fef6c 
      [21, "user100469"] -> 0x5fba778b 
      ... 
      [30, "user999775"] -> 0x45182d8c 
      [30, "user999850"] -> 0x1df279e9 
      [30, "user999936"] -> 0x525caa57
      ```

      通常来说，如果 MongoDB 使用索引进行查询，那么查询结果文档通常是按照索引顺序排列的

    * db.users.find({"age" : {"$gte" : 21， "$lte" :30}}).sort({"username":1}) 

      这是一个多值查询，与上一个类似，只是这次需要对查询结果进行排序。跟之前 一样，MongoDB 会使用索引来匹配查询条件：

      ```
      [21, "user100000"] -> 0x37555a81 
      [21, "user100069"] -> 0x6951d16f 
      [21, "user1001"]   -> 0x9a1f5e0c 
      [21, "user100253"] -> 0xd54bd959 
      ... 
      [22, "user100004"] -> 0x81e862c5 
      [22, "user100328"] -> 0x83376384 
      [22, "user100335"] -> 0x55932943 
      [22, "user100405"] -> 0x20e7e664 
      ...
      ```

      然而，使用这个索引得到的结果集中 "username" 是无序的，而查询要求结果以 "username" 升序排列，所以 MongoDB 需要先在内存中对结果进行排序，然后才能返回。因此，这个查询通常不如上一个高效。

      当然，查询速度取决于有多少个文档与查询条件匹配：

      * 如果结果集中只有少数几 个文档，MongoDB 对这些文档进行排序并不需要耗费多少时间。

      * 如果结果集中的文档数量比较多，查询速度就会比较慢

      * 如果结果集的大小 超过 32 MB，MongoDB 就会出错，拒绝对如此多的数据进行排序

        ```
        Mon Oct 29 16:25:26 uncaught exception: error: {    
        	"$err" : "too much data for sort() with no index. add an index or   		specify a smaller limit",    
        	"code" : 10128 
        	}
        ```

   3.2 最后一个查询的执行效率问题

   最后一个查询可以使用另一个索引（同样的键，但是顺序调换了）：

   `{"username" : 1， "age" : 1}`

   MongoDB 会反转所有的索引条目，但是会以 你期望的顺序返回。MongoDB 会根据索引中的 "age" 部分挑选出匹配的文档：

   ```
   ["user0", 69] 
   ["user1", 50] 
   ["user10", 80] 
   ["user100", 48] 
   ["user1000", 111] 
   ["user10000", 98] 
   ["user100000", 21] -> 0x73f0b48d 
   ["user100001", 60] 
   ["user100002", 82] 
   ["user100003", 27] -> 0x0078f55f 
   ["user100004", 22] -> 0x5f0d3088 
   ["user100005", 95] 
   ...
   ```

   这样非常好，因为不需要在内存中对大量数据进行排序。但MongoDB 不得不扫描整个索引以便找到所有匹配的文档。因此，如果对查询结果的范围做了限制， 那么 MongoDB 在几次匹配之后就可以不再扫描索引，在这种情况下，将排序键放 在第一位是一个非常好的策略。

   查看执行效率：

   * 通过{"age" : 1， "username" : 1}索引进行查询 

       ```
       > db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}). 
       ... sort({"username" : 1}). 
       ... explain() 
       {    
           "cursor" : "BtreeCursor age_1_username_1",    
           "isMultiKey" : false,    
           "n" : 83484,    
           "nscannedObjects" : 83484,    
           "nscanned" : 83484,    
           "nscannedObjectsAllPlans" : 83484,    
           "nscannedAllPlans" : 83484,
           "scanAndOrder" : true,    
           "indexOnly" : false,    
           "nYields" : 0,    
           "nChunkSkips" : 0,    
           "millis" : 2766,   
           "indexBounds" : {       
               "age" : [
                   [
                       21, 
                       30            
                   ]        
               ],        
               "username" : [
                   [
                       {
                           "$minElement" : 1 
                       },
                       {
                       "$maxElement" : 1
                       }
                   ]
               ]
           }, 
           "server" : "spock:27017" 
       }
       
       ```

       注意，"cursor" 字段说明这次查询使 用的索引是 {"age" : 1， "user name" : 1}，而且只查找了不到 1/10 的文档 （"nscanned" 只有 83484），但是这个查询耗费了差不多 3 秒的时间（"millis" 字 段显示的是毫秒数）。这里的 "scanAndOrder" 字段的值是 true：说明 MongoDB 必须在内存中对数据进行排序

   * 通过{"username" : 1， "age" : 1} 进行查询（可以通过 hint 来强制 MongoDB 使用某个特定的索引）

       ```
       > db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}). 
       ... sort({"username" : 1}). 
       ... hint({"username" : 1, "age" : 1}). 
       ... explain() {    
       	"cursor" : "BtreeCursor username_1_age_1",
           "isMultiKey" : false,
           "n" : 83484,
           "nscannedObjects" : 83484,
           "nscanned" : 984434,
           "nscannedObjectsAllPlans" : 83484,
           "nscannedAllPlans" : 984434,
           "scanAndOrder" : false,
           "indexOnly" : false,
           "nYields" : 0,
           "nChunkSkips" : 0,
           "millis" : 14820,
           "indexBounds" : {
       		"username" : [
       			[
       				{
       					"$minElement" : 1
       				},
       				{
       					"$maxElement" : 1
       				}
       			]
       		],
       		"age" : [
       			[
       				21,
       				30
       			]
       		]
       	},
           “server” : “spock:27017”
       }
       ```

       注意，这次查询耗费了将近 15 秒才完成。对比鲜明，第一个索引速度更快。然而， 如果限制每次查询的结果数量，新的赢家产生了：

       ```
       db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}). 
       ... sort({"username" : 1}).
       ... limit(1000).
       ... hint({"age" : 1, "username" : 1}).
       ... explain()['millis']
       2031 
       > db.users.find({"age" : {"$gte" : 21, "$lte" : 30}}).
       ... sort({"username" : 1}).
       ... limit(1000).
       ... hint({"username" : 1, "age" : 1}).
       ... explain()['millis']
       181
       ```

       第一个查询耗费的时间仍然介于 2 秒到 3 秒之间，但是第二个查询只用了不到 1/5 秒

       在实际的应用程序中，{"sortKey" : 1， "queryCriteria" : 1} 索引通常是很有用的，因为大多数应用程序在一次查询中只需要得到查询结果最前面的少数结 果，而不是所有可能的结果




## 相关阅读

博客

https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

多线程连接的相关问题:

<https://juejin.im/post/5a3b1e9c51882515945abedf>



