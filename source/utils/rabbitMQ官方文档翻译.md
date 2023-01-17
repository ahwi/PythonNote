# Documentation: Table of Contents（文档：目录）

链接：`https://www.rabbitmq.com/documentation.html`

**Distributed RabbitMQ 分布式RabbitMQ**

- [Replication and Distributed Feature Overview](https://www.rabbitmq.com/distributed.html)复制和分布式功能概述

- [Clustering](https://www.rabbitmq.com/clustering.html)集群

- [Cluster Formation and Peer Discovery](https://www.rabbitmq.com/cluster-formation.html)集群形参与对等发现

- [Inter-node traffic compression](https://www.rabbitmq.com/clustering-compression.html)节点间流量压缩

- [Quorum Queues](https://www.rabbitmq.com/quorum-queues.html): 仲裁队列

  a modern highly available replicated queue type 现代的高可用复制队列类型

- [Reliability](https://www.rabbitmq.com/reliability.html) 可靠性

  of distributed deployments, publishers and consumers 分布式部署、发布者和消费者

- [Classic Mirrored Queues](https://www.rabbitmq.com/ha.html) (legacy) 经典镜像队列（遗留）

- Active-passive [standby configuration with Pacemaker](https://www.rabbitmq.com/pacemaker.html) (legacy) 主动-被动（使用Pacemaker的备用配置）

## Replication and Distributed Feature Overview 复制和分布式功能概述

有三种方法实现RabbitMQ的分布式

* clustering 集群
* Federation
* Shovel

这三种方式不是互相排斥的，有时候可以组合使用。

### Clustering 集群

集群江多台机器连接在一起形成一个集群。内部节点间通信对客户端来说是透明的。集群的设计假设网络是可靠的并提供类似LAN的延时。

集群里面的所有节点安装的RabbitMQ和Erlang必须是兼容的。

节点之间通常使用自动化部署工具预设的密钥来进行认值。

Virtual host、exchanges、users还有permissions自动在集群的所有节点见进行复制。队列可以只存在于单个节点中，也可以在各个节点中复制以达到高可用性。仲裁队列（ [Quorum queues](https://www.rabbitmq.com/quorum-queues.html) ）是一种现代的复制队列类型，主要关注数据安全。经典队列可以有选择的进行镜像。

连接到集群中的任何节点的客户端，可以使用集群中的任何非独占队列，即使它们不在该节点上。

集群节点可以帮助提高性能、队列中数据的安全性并且提高客户端的并发连接数。The [Clustering](https://www.rabbitmq.com/clustering.html), [Quorum Queues](https://www.rabbitmq.com/quorum-queues.html) and [Classic Mirrored Queues](https://www.rabbitmq.com/ha.html) guides provide more details on these topics.

### Federation

federation允许一个代理（broker）上的exchange或queue接收发布到另一个broker上的exchange或queue上的消息（broker可以是单独的机器或集群）。通信时通过AMQP（带有可选的SSL）进行的，因此对于要federation的两个exchange或queue，它们必须被授予适当的用户或权限。

## Clustering 集群

本指南涵盖RabbitMQ集群相关的主题：

* 如何识别RabbitMQ的节点：节点名称（[node names](https://www.rabbitmq.com/clustering.html#node-names)）
* 集群所需的条件（[Requirements](https://www.rabbitmq.com/clustering.html#cluster-formation-requirements) ）

* 哪些数据是在集群节点中复制，哪些数据不是在集群节点中复制（[replicated between cluster nodes](https://www.rabbitmq.com/clustering.html#cluster-membership)）

* 集群对客户端意味着什么（[means for clients](https://www.rabbitmq.com/clustering.html#clustering-and-clients)）
* 集群是如何构成的（[How clusters are formed](https://www.rabbitmq.com/clustering.html#cluster-formation)）
* 节点之间如何相互认证（和使用CLI工具）（ [authenticate to each other](https://www.rabbitmq.com/clustering.html#erlang-cookie) ）
* 为什么使用奇数个节点很重要（ [use an odd number of nodes](https://www.rabbitmq.com/clustering.html#node-count)），强烈建议不要使用两个集群节点
* 节点重启（[Node restarts](https://www.rabbitmq.com/clustering.html#restarting) ）和如何让节点重新加入集群
* 节点就绪状态检测（[Node readiness probes](https://www.rabbitmq.com/clustering.html#restarting-readiness-probes) ）和它们如何影响集群的重启
* 如何删除一个集群的节点（ [remove a cluster node](https://www.rabbitmq.com/clustering.html#removing-nodes)）
* 如何把集群的节点恢复为原始状态（[reset a cluster node](https://www.rabbitmq.com/clustering.html#resetting-nodes) ）

RabbitMQ集群是一个或多个节点的逻辑分组，每个节点共享用户、虚拟主机、队列、交换、绑定、运行时参数和其他分布式状态。

### Cluster Formation 集群的构成

#### 构成集群的方法

RabbitMQ集群有多种方式形成：

* 通过在配置文件中列出集群节点来声明（[config file](https://www.rabbitmq.com/configure.html)）

* 通过基于DNS的方式来声明
* Declaratively using [AWS (EC2) instance discovery](https://github.com/rabbitmq/rabbitmq-peer-discovery-aws) (via a plugin)
* Declaratively using [Kubernetes discovery](https://github.com/rabbitmq/rabbitmq-peer-discovery-k8s) (via a plugin)
* Declaratively using [Consul-based discovery](https://github.com/rabbitmq/rabbitmq-peer-discovery-consul) (via a plugin)
* Declaratively using [etcd-based discovery](https://github.com/rabbitmq/rabbitmq-peer-discovery-etcd) (via a plugin)
* Manually with rabbitmqctl

详情查看集群构成指南（ [Cluster Formation guide](https://www.rabbitmq.com/cluster-formation.html) ）

集群的组成可以动态地改变。所有RabbitMQ代理一开始都运行在单个节点上。这些节点可以加入到集群中，后面也可以再次变回单独的代理。

#### 节点名称（标识identifiers）

RabbitMQ节点由节点名称来标识。一个节点名称由两部分构成：前缀（通常是`rabbit`）和主机名称（hostname）。例如，节点名称`rabbit@node1.messaging.svc.local`，前者是`rabbit`，主机名是`node1.messaging.svc.local`。

在集群中节点名称必须是唯一的。如果在一个主机上允许多个节点（通常在测试环境或者QA环境中），它们必须使用不同的前缀，例如`rabbit1@hosname`和`rabbit2@hostname`。

在集群中，节点使用节点名互相标识和联系。这意味着必须解析节点名中的主机名部分（ [hostname resolve](https://www.rabbitmq.com/clustering.html#hostname-resolution-requirement)）。CLI工具（ [CLI tools](https://www.rabbitmq.com/cli.html) ）还使用节点名称来标识和寻址节点。

当节点启动时，它会检测是否已经为其分配节点名。这是通过环境变量`RABBITMQ_NODENAME`来完成的。如果没有配置该值，节点通过解析主机名和添加`rabbit`的前缀来计算节点名。

如果系统对主机名使用完全限定域名（qualified domain names(FQDNs)），RabbitMQ和CLI工具必须配置为长节点名。对于服务器节点，将通过配置环境变量`RABBITMQ_USE_LONGNAME`来完成。对于CLI工具来说，必须设置`RABBITMQ_USE_LONGNAME`或者指定`--longnames`选项。

### Cluster Formation Requirements（节点构成的所需条件）

#### 主机名解析





