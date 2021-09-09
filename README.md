# [Ceres使用说明 中文版本](https://github.com/hulatang/ceres-combineharvester/blob/main/README_ch.md)

---



# Ceres Combine-Harvester

Ceres is a combine harvester designed to harvest plots for Chia blockchain and multi chia forks(like flax, spare....) simultaneously by running single harvester on your machine.

---

# Basic: What is Ceres

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

---

# Before Install

Before install Ceres, you should choose the Ceres version you need.

Ceres version should match the version of your FullNode or Farmer version.

##### Note:

Which Ceres version to use is not related to whether og plots or pool plots you are going to harvester, only related to the forks FullNode version you are running.

---

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
   cd eres-combineharvester
   sudo chmod +x install.sh
   ./install.sh
   ```

3. Activate
   
   ```
   . ./activate
   ```

---

Configure forks you wanna to harvester

By default, Ceres is set to only harvest Chia

To harvester other forks, open file:

```
ceres/util/all-coins-config.yaml
```

Just umcomment the name and network_id line, then Ceres will harvest those forks.

The all-coins-config.yaml file looks like this:

chia:

network_id: "mainnet"

#flax:

    #network_id: "flax-mainnet"

#spare:

    #network_id: "mainnet"

#silicoin:

    #network_id: "mainnet"

#flora:

    #network_id: "mainnet"

---

# Init

If you have setup forks you want to harvest, it is to say you have got .chia or .forks under your home directory, you an just skip this chapter to Run

Here we init from absolutly fresh install, just run:

```
ceres init_all
```

note the underscore in init_all

this command will generate root path for each forks, like .chia, .flax under your home directory

Next we generate ssl files for each forks, for example you want to harvest flax:

1. copy ca directory from you flax farmer computer to local [path_to_ca], the ca directory is located at ~/.flax/mainnet/config/ssl/ca on your Flax Farmer machine.

2. run:

```
ceres init -n flax -c [path_to_ca]
```

config for other forks is similar, 

```
ceres init -n [fork_name] -c [path_to_ca]
```

Finally, what you need to change is your famer-peer ip address under Harvester section(not full node section) in each fork's config.yaml

For example you want to harvest flax:

Open the `~/.flax/mainnet/config/config.yaml` file, and enter your Farmer machine's IP address in the remote **`harvester`**'s farmer_peer section (NOT `full_node`).  
EX:

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

Repeat process  above for every fork you wanna to harvest

---

# Run

activate venv first, then run:

```
ceres start harvester -r
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

# Network Architecture

Defult Chia Harvester and Famer is structured as below

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/chia_default_net_structure.jpg" alt="alt txt" data-align="center">

By Chia default, you should run one harvester for each fork's farmer.

Ceres has a different structure, like below:

<img title="" src="https://github.com/hulatang/ceres-combineharvester/blob/wiki/wiki_images/ceres_network.png" alt="alt txt" data-align="center" width="486">

By using Ceres, you can run an unique Harvester server which will response to all the farmer's request. Thanks to Chia's asyncio pattern, a single Harvester server has enough throughput  to proccess farmer's asynchronous challenge hash request.

---

# Compatibility

For a harvester, it is responsible for communicating with famer by complying chia's Harvester Protocol.

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

```
ceres stop all -d
ceres start harvester -r
```

---

# How to select forks you want to harvest

By default, only Chia is activated.

Open the file ceres/util/all-coins-config.yaml

Just uncomment forks you want to harvest, like below (just delete the # before corresponding line)

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

```
ceres stop all -d
ceres start harvester -r
```
