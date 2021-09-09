# Ceres Combine-Harvester

# Ceres 联合收割机

Ceres is a combine harvester designed to harvest plots for Chia blockchain and multi chia forks(like flax, spare....) simultaneously by running single harvester on your machine.

Ceres是一款多挖软件， 适用于Chia以及Chia的分支币种，比如Flax, Spare等等.

Ceres只需要运行一个Harvester，就可以同时多挖多个币种.

---

# Basic: What is Ceres

# 基础: Ceres是什么

Ceres运行一个单一的Harvester， 便可以和多个币种的Farmer通讯， 进行plot文件的挖币

如下图:

Ceres runs single harvester to harvester plots for multiple Chia Farmer,  Flax Farmer, Spare Famer....., shown in the figure:

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

---

# Features

- single harvester, multiple chia forks harvested

- both chia og plots and pool plots are supported

- based on Chia's source code, with least modification

- only one harvester is run, not each harvester for each fork

- same memory  and cpu usage as a single Chia harvester 

- follow Chia's asyncio design pattern,  by principle multiple forks activities will not affect Chia harvestering

- easy to configure to support more forks as you wish

- multi-platforms supported, such as Raspberry Pi



# 特点

- 只需运行一个Harvester， 就可以实现多挖

- 支持Chia的OG plot，以及pool plot (单机plot, 以及矿池plot)

- 基于Chia源码，进行了尽可能少的改动

- 不需要为每一个币种运行一个Harvester

- 和只挖Chia一个币种相比，几乎等同的cpu和内存使用量

- 遵循Chia的异步设计模式， 几乎不会影响Chia的挖币

- 配置简单，可以轻松扩展支持更多的币种

- 多平台支持，比如树莓派

---

# Before Install

Before install Ceres, you should choose the Ceres version you need.

Ceres version should match the version of your FullNode or Farmer version.

##### Note:

Which Ceres version to use is not related to whether og plots or pool plots you are going to harvester, only related to the forks FullNode version you are running.

# 准备

在安装Ceres之前，您需要先选择需要安装的Ceres版本

### 注意:

Ceres版本的选择，应该依据您安装的FullNode或者Farmer的版本， 而不是您的plot文件是原生的OG plot还是新的pool plot

---

# 安装

Ceres的安装方式和Chia的安装方式相同

强烈建议您在安装Ceres之前，先阅读一下Chia的文档，尤其是这篇文章

[Farming on many machines · Chia-Network/chia-blockchain Wiki · GitHub](https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines)



1. **下载代码**
   
   - 
   
   如果您的FullNode或者Farmer版本是基于Chia 1.2之后的， 使用以下命令下载:
   
   ```
   ```
   git clone https://github.com/hulatangeric/Ceres-CombineHarvester.git
   ```
   ```
- 如果您的FullNode或者Farmer版本低于1.7.1， 使用以下命令下载:
  
  ```
  ```
  git clone https://github.com/hulatangeric/Ceres-CombineHarvester.git -b og
  ```
  ```

2 . **安装**



```
cd Ceres-CombineHarvester
sudo chmod +x install.sh
./install.sh
```





# Installation

Ceres can be installed  the same way installing Chia normally.

It's highly recommended to read through Chia's wiki, easpecially this article , [Farming on many machines · Chia-Network/chia-blockchain Wiki · GitHub](https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines) before using Ceres.

1. **Download code ** 
- if you are running FullNode version after chia 1.2.*, download Ceres by:

```
git clone https://github.com/hulatangeric/Ceres-CombineHarvester.git
```

- if you are running FullNode version before chia 1.7.1, download Ceres by:

```
git clone https://github.com/hulatangeric/Ceres-CombineHarvester.git -b og
```

2. **Installation**
   
   ```
   cd Ceres-CombineHarvester
   sudo chmod +x install.sh
   ./install.sh
   ```

---

# Init

If you have setup forks you want to harvest, it is to say you have got .chia or .forks under your home directory, you an just skip this chapter to Run

Here we init from absolutly fresh install, just run:

```
ceres init_all
```

this command will generate root path for each forks, like .chia, .flax under your home directory

# 初始化

如果您已经配置好了各种币的Harvester, 也就是说， 您的机器上已经有 .chia, .flax 等等币种的目录和配置文件， 您可以跳过本章，直接到 运行  章节继续。



这里我们从全新安装开始，运行代码, 注意 init_all里的下划线:

```
ceres init_all
```

 



Next we generate ssl files for each forks, for example you want to harvest flax:

1. copy ca directory from you flax farmer computer to local [path_to_ca]

2. run:

```
ceres init -n flax -c [path_to_ca]
```



下一步，我们为每一个币种生产所需要的ssl文件， 比如你要配置flax

1. 从你的Flax Farmer机器上复制ca文件夹到你本地创建的一个文件夹，比如叫 [path_to_ca], ca文件夹是你Flax Farmer机器上的 ~/.flax/mainnet/config/ssl/ca

    2. 运行

```
ceres init -n flax -c [path_to_ca]
```

为其他币种配置是一样的

```
ceres init -n [币名] -c [path_to_ca]
```



Finally, what you need to change is your famer-peer ip address under Harvester section(not full node section) in each fork's config.yaml

For example you want to harvest flax:

Open the `~/.flax/mainnet/config/config.yaml` file, and enter your Farmer machine's IP address in the remote **`harvester`**'s farmer_peer section (NOT `full_node`).  
EX:

最后，你需要为每一个币种，更改Farmer机器的ip地址，

具体位置是每一个币种的config.yaml文件中的Harvester部分(不是full node部分)



比如你想配置flax:

打开 ~/.flax/mainnet/config/config.yaml文件， 将远端harvester的farmer_peer， 改为您的Flax Farmer机器的IP地址

如下:

```
harvester:
  flax_ssl_ca:
    crt: config/ssl/ca/flax_ca.crt
    key: config/ssl/ca/flax_ca.key
  farmer_peer:
    host: Farmer.Machine.IP
    port: 8447
```

#### Note:

Do above process for every fork's Farmer

### 注意:

每一个币种，都要重复上述过程



---

# Run

activate venv first, then run:

# 运行

```
ceres start harvester -r
```

# Stop

#停止

```
ceres stop all -d
```

---

# Network Architecture

Defult Chia Harvester and Famer is structured as below

# Ceres的网络结构

Chia的默认Harvester和Farmer的结构如下

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/chia_default_net_structure.jpg" alt="alt txt" data-align="center">

By Chia default, you should run one harvester for each fork's farmer.

Ceres has a different structure, like below:

在Chia的默认情况下，您需要为每一个币种都运行一个Harvester, 而Ceres使用了不同的方式，只需要运行一个Harvester

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

By using Ceres, you can run an unique Harvester server which will response to all the farmer's request. Thanks to Chia's asyncio pattern, a single Harvester server has enough throughput  to proccess farmer's asynchronous challenge hash request.

通过使用Ceres, 您只需运行一个Harvester，就可以响应多个币种Farmer的请求. 得益于Chia的异步运行模式，一个Ceres的Harvester拥有足够的吞吐量来处理多个币种Farmer的C挖币请求

---

# Compatibility

For a harvester, it is responsible for communicating with famer by complying chia's Harvester Protocol.

# 适配性

对于Harvester来说，它的工作是响应Farmer的请求，

### 目前支持的币种

### Current supported forks:

Chia, Flax, Spare, Silicoin, Flora, Chiarose, Kale, Goji, Chaingreen, Seno, Socks, Apple

Equality, Greendoge, Tad, Dogechia, Maize, Wheat, Taco, Covid, Melati, Cactus, 

Hddcoin, Avocado, Cryptodoge, Sector, Nchain, Btcgreen, Cannabis, Scam, Fork, Olive, 

Lucky, Pipscoin, Beer, Cunt, Thyme, Littlelambocoin    

---

# How to add more forks?

It is easy for Ceres to add more forks support .

Just download the all-coin-config.yaml from github and replace the old file in chia/util  subdirectory.

then run:

# 如果添加更多的币种支持

对于Ceres， 添加更多的币种非常容易

只需要从Ceres的github仓库下载最新的all-coin-config.yaml文件,覆盖掉之前的，就可以了

然后，运行

```
ceres stop all -d
ceres start harvester -r
```

---

# How to select forks you want to harvest

By default, only Chia is activated.

Open the file ceres/util/all-coins-config.yaml

Just uncomment forks you want to harvest, like below

# 如何选择您想要挖的币种

默认情况下， 我们仅打开了Chia

如果您想打开其他的币种， 打开文件 ceres/util/all-coins-config.yaml

将您想要挖的币种的部分的注释删除，就可以了(删除掉对应行前面的#)

```
chia:
  network_id: "mainnet"
flax:
  network_id: "flax-mainnet"
#kale:
  #network_id: "kale-mainnet"
#goji:
  #network_id: "mainnet" 
```

Next, you should generate ssl files for every forks you activated, edit Farmer peer IP in its corresponded config files (.[fork]/mainnet/config/config.yaml)

Finnaly:

下一步， 您仍然需要按照之前的章节， 为新加的币种，生成ssl文件

最后:

```
ceres stop all -d
ceres start harvester -r
```
