# protobuf的使用

官方：[https://developers.google.com/protocol-buffers/docs/pythontutorial](https://links.jianshu.com/go?to=https%3A%2F%2Fdevelopers.google.com%2Fprotocol-buffers%2Fdocs%2Fpythontutorial)

参考资料：

* https://www.jianshu.com/p/1aeb8ee87b99

* https://www.cnblogs.com/luyanjie/p/10403869.html

protobuf是google推出的任意语言，任意平台，任意设备上皆可用的一种数据协议，具有以下特点：

1. 使用`.proto`格式文件描述数据层级结构
2. protobuf编译器会根据`.proto`文件的描述自动创建一个class编码转换你指定的数据结构，同时生成的这类会自动提供数据转换的getter和setter方法，完成一个protocol buffer的内容的组成或者是读写
3. protobuf格式支持格式扩展兼容，使用旧的proto协议编码仍然可以读取使用了新协议编码的数据，当然你更新的新协议也是可以兼容之前proto的定义

## 安装：

1. 安装protoc

   https://github.com/google/protobuf/releases

   这里安装 `protoc-3.7.0-win64.zip`版本

   解压后把bin目录添加的环境变量中

2. python安装protobuf

   `protobuf==3.19.4`

## 测试：

**创建文件`protobuf/test2.proto`**

```txt
syntax = "proto2";
message testinfo 
{ 
required int32 devtype = 1; 
required int32 devid = 2; 
required int32 unitid = 3; 
required int32 chlid = 4; 
optional int32 testid = 5 [default = 0]; 
required bytes stepdata = 6; 
}
```

**编译：**

```cmd
protoc --python_out=./ test2.proto
```

执行后会生成文件`test2_pb2.py`

**调用代码`protobuf/test.py`**

```python
import test2_pb2
  
testinfo = test2_pb2.testinfo()  
testinfo.devtype = 100  
testinfo.devid = 2  
testinfo.unitid = 3  
testinfo.chlid = 4  
testinfo.testid = 250
testinfo.stepdata = b'abd'

print(testinfo, testinfo.devtype)  # 打印 protobuf 结构的内容
out = testinfo.SerializeToString()  
print(out)  # 打印 Protobuf 序列字符串
  
  
decode = test2_pb2.testinfo()  
decode.ParseFromString(out)  
  
print(decode) # 打印 解析Protobuf后的内容
```

