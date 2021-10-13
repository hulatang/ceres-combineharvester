# [Ceres使用说明 中文版本](https://github.com/hulatang/ceres-combineharvester/blob/main/README_ceres_0.2_ch.md)

---

# Ceres Combine-Harvester

Ceres is a combine harvester designed to harvest plots for Chia blockchain and multi chia forks(like flax, spare....) simultaneously by running single harvester on your machine.

---

# Basic: What is Ceres

Ceres runs a single harvester to communicate with multiple locale or remote Chia Farmer,  Flax Farmer, Spare Famer....., shown in the figure:

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

---

# Features

- **single harvester, multiple chia forks harvested**

- **ceres harvester will not conflict with Chia harvester or  any fork's havesters**

- both chia og plots and pool plots are supported

- based on Chia's source code, with least modification

- only one harvester is run, not each harvester for each fork

- same memory  and cpu usage as a single Chia harvester 

- follow Chia's asyncio design pattern,  by principle multiple forks activities will not affect Chia harvestering

- easy to configure to support more forks as you wish

- multi-platforms supported, such as Raspberry Pi

---

# Compatability

Currently, almost all forks have update their farmer version to Chia farmer version after 1.2.

So Ceres currently only support communication with farmers after Chia farmer 1.2

---

# Installation

---

**Note**

If you wanna reinstall Ceres or if you have installed old version Ceres before,

you should first delete .ceres directory under your user home directory before Ceres initialization.

```
rm -rf ~/.ceres
```

---

Ceres can be installed  the same way installing Chia normally.

It's highly recommended to read through Chia's wiki, easpecially this article , [Farming on many machines · Chia-Network/chia-blockchain Wiki · GitHub](https://github.com/Chia-Network/chia-blockchain/wiki/Farming-on-many-machines) before using Ceres.

**We start to initialize Ceres**

1. **Download Code**

```
git clone https://github.com/hulatang/ceres-combineharvester.git
```

2. **Installation**
   
   ```
   cd ceres-combineharvester
   sudo chmod +x install.sh
   ./install.sh
   ```

3. **Activate virtual environment**
   
   ```
   . ./activate
   ```

---

# Ceres Init

**Read this section carefully**

Totally initialization has three steps,  read instruction detail below

```
# first, initialize directory structure for ceres
1. ceres init

# second, after you have configure farmer info, initialize 
# directories for every coins
2. ceres init --coins

# third, copy farmer ca directories to specific directory under .ceres
# and generate ssl files for every coin
3. ceres generate_ssl
```

**We start to initialize Ceres by steps in detail**:

(venv) ➜  stands for ceres virtual environment

~ stands for user home directory

1. **Initialize ceres directory structure**
   
   ```
   (venv) ➜ ceres init
   ```

 after complete this step, there will be a .ceres under your /home/username/ directory,

.ceres directory looks like this:

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

2. **Setup farmer peers info**
   
   ~/.ceres/mainnet/config/coins_config.yaml is an importatnt configure file in which your farmer info is configured.
   
   by default top lines of coins_config.yaml looks like this
   
   ```
   farmer_machine:
       - farmer_peer: 
           address: localhost
           coins:
             #- chia
             #- flax
   ```

now let's assume you have two farmer machines, and you are going to farm chia, flax, spare and kale

A: 192.168.1.100: chia, flax

B: 192.168.1.299: spare, kale

open ~/.ceres/mainnet/config/coins_config.yaml and enter your farmer info like below:

**NOTE** the indent and "-" symbol

```
farmer_machine:

- farmer_peer: 
  address: 192.168.1.100
  coins:
    - chia
    - flax

- farmer_peer
  address: 192.168.1.200
  coins:
    - spare
    - kale
```

Then run command:

```
(venv) ➜ ceres init --coins
```

After this step finished, ceres will make default root directories for every coin under .ceres

Now .ceres directory looks like this:

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

3. **Copy your farmer ca directory of every coin into ceres**
   
   Take Chia for example, copy ca directory of your Chia farmer machine into  .ceres/mainnet/all_ca/chia_ca
   
   ```
   scp -r username@192.168.1.100:~/.chia/mainnet/config/ssl/ca ~/.ceres/mainnet/all_ca/chia_ca
   ```

repeat above step, copy ca directory of every coin on your farmer machin into .ceres/mainnet/all_ca/[coin_name_]_ca directory

after above step finnished, .ceres/mainnet/all_ca looks like this:

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
│       └── ca
```

4. **Generate ssl files**
   
   ```
   (venv) ➜ ceres generate_ssl
   ```

After above steps completed, Ceres is successfully initialized.

---

## Log Level

Before start ceres, you can configure log level as you wish.

By default, Ceres set log level the same as Chia: "Warning"

If you wanna to set log level of Ceres to "DEBUG",

open ~/.ceres/mainnet/config/config.yaml

set the log level:

```
log_level: "DEBUG"
```

---

## Add plot directories

open file ~/.ceres/mainnet/config/coins_config.yaml

by default it looks like this:

```
#path of your plot files
plot_directories: []
```

you should set plot_directories like this, NOTE the indent and "-" symbol

```
plot_directories:

- /home/your/plot/path/0001

- /home/your/plot/path/0002

- /home/your/plot/path/0003
```

---

# Run

activate venv first, then run:

```
(venv) ➜ ceres start harvester -r
```

you can use this command to see if Ceres works correctly:

```
tail -f ~/.ceres/mainnet/log/debug.log | grep ceres.harvester
```

you should see some info like this:

```
harvester ceres.harvester.harvester: INFO     (flax)     : 0 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (chia)     : 0 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (flax)     : 2 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (chia)     : 1 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00012 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (spare)    : 0 plots were eligible for farming 5c63a7238a... Found 0 proofs. Time: 0.00011 s. Total 20 plots
harvester ceres.harvester.harvester: INFO     (kale)     : 1 plots were eligible for farming 1734aefc18... Found 0 proofs. Time: 0.00009 s. Total 20 plots
```

### Note:

Nothing wrong if you see some info says like: No keys on this machine

Running harvester does not require any keys.

---

# Stop

```
ceres stop all -d
```

---

## Coin Names you can use:

Please DO use names in coins_config.yaml

```
vim ~/.ceres/mainnet/config/coins_config.yaml
```

You can only use names under coin_names:

```
coin_names:
  - chia
  - flax
  - spare
  - silicoin
  - flora 
  - socks 
  - apple 
  - kale 
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
  - sector
  - nchain
  - btcgreen
  - cannabis
  - scam
  - fork
  - olive
  - pipscoin
  - beer
  - cunt
  - littlelambocoin
  - stor
  - beet
  - lotus
  - mint
  - kiwi
  - mogua
  - tranzact
  - peas
  - salvia
  - staicoin
  - taco
  - melati
  - cryptodoge
```

---

## Add coin steps:

Let's say you wanna add silicoin to farmer 192.168.1.100

First stop ceres

```
(venv) ➜ ceres stop all -d
```

open ~/.ceres/mainnet/config/coins_config.yaml

1. add silicoin to farmer_peer:

```
 farmer_machine:
     - farmer_peer: 
         address: 192.168.1.100
         coins:
           - chia
           - flax
           - silicoin  <--- add silicoin here
```

2. Then:

```
(venv) ➜ ceres init --coins
```

next copy silicoin farmer's ca directory to ~/.ceres/mainnet/all_ca/silicoin_ca

3. next generate ssl files

```
(venv) ➜ ceres generate_ssl
```

4. restart ceres:

```
(venv) ➜ ceres restart harvester -r
```

---

# Note:

Once you set up one harvester machine

you can copy ceres all_ca directory under ~/.ceres/mainnet and coins_config.yaml under ~/.ceres/mainnet/config to another harvester machine

Then on the other machine:

```
(venv) ➜ ceres init
(venv) ➜ ceres init --coins
(venv) ➜ ceres generate_sll
(venv) ➜ ceres start harvester -r
```

---

## Current supported forks:

Chia, Flax, Spare, Silicoin, Flora, Kale, Goji,, Seno, Apple

Greendoge, Tad, Dogechia, Maize, Wheat, Taco, Covid, Melati, Cactus,

Hddcoin, Avocado, Sector, Nchain, Btcgreen, Cannabis, Scam, Fork

---

## Network Architecture

Defult Chia Harvester and Famer is structured as below

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/chia_default_net_structure.jpg" alt="alt txt" data-align="center">

By Chia default, you should run one harvester for each fork's farmer.

Ceres has a different structure, like below:

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

By using Ceres, you can run an unique Harvester server which will response to all the farmer's request. Thanks to Chia's asyncio pattern, a single Harvester server has enough throughput  to proccess farmer's asynchronous challenge hash request.

---

# How to update Ceres

besure you are under ceres-combineharvester directory

```
# update ceres
git pull origin main
(venv) ➜ ceres update

# restart ceres
(venv) ➜ ceres stop all -d
(venv) ➜ ceres start harvester -r
```

NOTE: after pulling code from github, don't forget to run ceres update to complete ceres updating.

---

# ChangeLog

---

**2021-10-13**

**Add more supported coins:**

- olive
- pipscoin
- beer
- cunt
- littlelambocoin
- stor
- beet
- lotus
- mint
- kiwi
- mogua
- tranzact
- peas
- salvia
- staicoin
- taco
- melati
- cryptodoge
