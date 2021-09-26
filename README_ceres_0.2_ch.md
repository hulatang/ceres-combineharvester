# Ceres 联合收割机

Ceres是一款多挖软件， 适用于Chia以及Chia的分支币种，比如Flax, Spare等等.

Ceres只需要运行一个Harvester，就可以同时多挖多个币种.

---

# 基础: Ceres是什么

Ceres运行一个单一的Harvester， 便可以和多个币种的Farmer通讯， 进行plot文件的挖币

如下图:

---

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

---

# 特点

- **只需运行一个Ceres Harvester， 不需要为每一个币种运行一个Harvester**

- **Ceres独立运行，不会跟Chia以及其他币种客户端冲突**

- 支持Chia的OG plot，以及pool plot (单机plot, 以及矿池plot)

- 基于Chia源码，进行了尽可能少的改动

- 和只挖Chia一个币种相比，几乎等同的cpu和内存使用量

- 遵循Chia的异步设计模式， 几乎不会影响Chia的挖币

- 配置简单，可以轻松扩展支持更多的币种

- 多平台支持，比如树莓派

---

# 版本适配

当前版本的Ceres， 仅适配基于Chia 1.2 及之后的Farmer

目前大多数的币种客户端，都已经升级到Chia 1.2

---

# 安装

Ceres的安装方式和Chia的安装方式相同

强烈建议您在安装Ceres之前，先阅读一下Chia的文档，尤其是这篇文章

[Farming on many machines · Chia-Network/chia-blockchain Wiki · GitHub](https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines)

1. **下载源代码**
   
   ```
   git clone https://github.com/hulatang/ceres-combineharvester.git
   ```

2. **安装**
   
   ```
   cd ceres-combineharvester
   sudo chmod +x install.sh
   ./install.sh
   ```

3. **激活虚拟环境**
   
   ```
   . ./activate
   ```

---

# 初始化 Ceres

**这一步很重要，请仔细阅读**

1. **初始化目录** 
   
   以下的 (venv) ➜ 代表命令行的提示符， 表明您已处于虚拟环境中
   
   请输入(venv) ➜后面的命令  

```
(venv) ➜  ceres-combineharvester git:(main) ceres init
```

   目录初始化成功之后， ceres会在用户根目录创建一个 .ceres 目录， 看起来是这样子的

   ~ 代表您的用户根目录, 比如 /home/your_name/

```
(venv) ➜ tree ~/.ceres -L 4
.ceres
└── mainnet
   └── config
       ├── coins_config.yaml
       ├── config.yaml
       └── ssl
           ├── ca
           ├── daemon
           ├── farmer
           ├── full_node
           ├── harvester
           ├── introducer
           ├── timelord
           └── wallet
```

2. **配置挖矿相关信息**
   
   ~/.ceres/mainnet/config/coins_config.yaml 这个文件很重要，跟挖矿相关的信息都在这个文件里进行配置.
   
   coins_config.yaml 默认内容的头部， 是这样的: 

    =========================================
    
    # *** User Defined Section ***
    
    # =========================================
    
    
    #  Edit your Farmer machine IP address below
    #  Add coins name to it's farmer peer's coins part
    #  Only Use coin names under coins supported section below
    farmer_machine:
        - farmer_peer: 
            address: localhost
            coins:
              - chia
                #- flax
    
    
        # Farmer Peer SAMPLE
        # You can add as many farmer peers as you have
        # Note the indent
    
        # - farmer_peer: 
        #     address: 192.168.1.100
        #     coins:
        #       - flora
        #       - kale
    
        # - farmer_peer: 
        #     address: 192.168.1.101
        #     coins:
        #       - spare
        #       - chaingreen
    
    # path of your plot files
    plot_directories:[]

下面我们假设，您有两台电脑, 一共挖四种币，chia, flax, spare, kale, 分别为:

- 192.168.1.100, 币种为 chia, flax

- 192.168.1.200 币种为 spare, kale

修改coins_config.yaml中， farmer_machine的内容, 注意缩进 和 - 号

```
farmer_machine:
 - farmer_peer: 
address: 192.168.1.100
 coins:
 - chia
 - flax
 - farmer_peer: 
address: 192.168.1.200
 coins:
 - spare
 - kale
```

**初始化挖矿配置**

```
(venv) ➜ ceres init --coins
```

币种初始化成功后， .ceres目录看起来是这样的

```
(venv) ➜ tree ~/.ceres/mainnet -a -L 3
.ceres/mainnet
├── all_ca
│   ├── chia_ca
│   ├── flax_ca
│   ├── kale_ca
│   └── spare_ca
├── all_coins
│   ├── .chia
│   │   └── mainnet
│   ├── .flax
│   │   └── mainnet
│   ├── .kale
│   │   └── mainnet
│   └── .spare
│   └── mainnet
└── config
 ├── coins_config.yaml
 ├── config.yaml
 └── ssl
 ├── ca
 ├── daemon
 ├── farmer
 ├── full_node
 ├── harvester
 ├── introducer
 ├── timelord
 └── wallet
```

其中， all_ca文件夹是下一步用来存放每个币种的ca文件夹的，all_coins里面的内容不需要用户配置

3. **拷贝每个币种的ca文件夹**

以chia为例

将 chia所在farmer机器下， ~/.chia/mainnet/config/ssl/ca 文件夹， 拷贝到 ~/.ceres/mainnet/all_ca/chia_ca目录下

```
scp -r username@192.168.1.100:~/.chia/mainnet/config/ssl/ca ~/.ceres/mainnet/all_ca/chia_ca
```

**拷贝每一个币种的ca文件夹到all_ca目录下对应的文件夹**

拷贝完成后， ~/.ceres/mainnet/all_ca目录看起来是这样子的

```
.ceres/mainnet
├── all_ca
│   ├── chia_ca
│   │   └── ca
│   ├── flax_ca
│   │   └── ca
│   ├── kale_ca
│   │   └── ca
│   └── spare_ca
│   └── ca
```

4. **生成ssl加密文件**

```
(venv) ➜ ceres generate_ssl
```

**ceres配置完成！**

---

# 配置Ceres日志级别

运行ceres之前， 您可以选择ceres log的日志级别 , 默认设置遵循chia, 为warning.

日志级别的配置文件是 ~/.ceres/mainnet/config/config.yaml

**注意**:

日志级别的配置文件是 config.yaml 

挖币相关配置文件为 coins_config.yaml

```
vim ~/.ceres/mainnet/config/config.yaml
```

修改

```
log_level: "DEBUG"
```

修改之后是这样子:

```
# Controls logging of all servers (harvester, farmer, etc..). Each one can be overriden.

logging: &logging
 log_level: "DEBUG" # Can be CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
```

---

# 添加plot目录

plot目录的配置位置，是在 ~/.ceres/mainnet/config/coins_config.yaml 中的 plot_directories

默认情况下

```
#path of your plot files
plot_directories: 【】
```

添加您自己的plot文件夹,

```
plot_directories:
- /home/yourname/[path]/0001
- /home/yourname/[path]/0002
- /home/yourname/[path]/0003
```

---

# 运行Ceres

```
(venv) ➜ ceres start harvester -r
```

运行成功后， 运行如下命令查看日志信息

```
tail -f ~/.ceres/mainnet/log/debug.log | grep ceres.harvester
```

如果运行成功， 可以看到如下信息

```
harvester ceres.harvester.harvester: INFO     (flax)     : 0 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (chia)     : 0 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (flax)     : 2 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (chia)     : 1 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (spare)    : 0 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00011 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (kale)     : 1 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00009 s. Total 20 plots
```

---

## 币种的名字

**请务必使用配置文件中默认的名字**

打开coins_config.yaml配置文件

```
vim ~/.ceres/mainnet/config/coins_config.yaml
```

可以使用的名字，在文件的下部

```
coin_names:
   - chia
   - flax
   - spare
   - silicoin
   - flora 
   - chiarose
   - socks 
   - apple 
   - kale 
   - chaingreen
   - seno
   - equality 
   - greendoge 
   - tad 
   - dogechia
   - maize 
   - wheat
   - taco
   - covid
   - melati
   - cactus
   - hddcoin
   - avocado
   - cryptodoge
   - sector
   - nchain
   - btcgreen
   - cannabis
   - scam
   - fork
   - lucky
```

---

# 添加币种

要添加远端机器和币种，顺序如下

1. 修改 coins_config.yaml文件， 位置是 ~/.ceres/mainnet/config/coins_config.yaml
   
   比如给 192.168.1.100添加 silicoin
   
   ```
    farmer_machine:
        - farmer_peer: 
            address: 192.168.1.100
            coins:
              - chia
              - flax
            ### 把silicoin添加到这里
              - silicoin
   ```

2. 运行币种初始化
   
   ```
   (venv) ➜ ceres init --coins
   ```

3. 拷贝远端机器的silicoin的ca文件夹
   
   ```
   scp -r username@192.168.1.100:~/.silicoin/mainnet/config/ssl/ca ~/.ceres/mainnet/all_ca/silicoin_ca 
   ```

4. 生成ssl文件
   
   ```
   (venv) ➜ ceres generate_ssl
   ```

5. 停止ceres, 重启ceres
   
   ```
   (venv) ➜ ceres stop all -d
   (venv) ➜ ceres start harvester -r
   ```

---

# 注意:

- ~/.ceres/mainnet 下的 all_ca目录，一旦您把所有的ca文件夹都拷贝完成了，  这个all_ca文件夹，可以直接拷贝的其他需要运行ceres的机器上， 目标目录为 .ceres/mainnet/

- ~/.ceres/mainnet/config文件夹下的 coins_config.yaml文件，也可以直接复制到另一台需要运行ceres的机器上

- 另外一台ceres机器， 拷贝上上述文件夹后，顺序运行如下命令
  
  ```
  (venv) ➜ ceres init
  (venv) ➜ ceres init --coins
  (venv) ➜ ceres generate_ssl
  ```
