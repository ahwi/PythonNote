# mongo

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



