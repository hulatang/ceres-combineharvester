# Ceres Combine-Harvester

Ceres is a combine harvester designed to harvest plots for Chia blockchain and its forks using proof-of-space-and-time(PoST) consensus algorithm.

---

# Features

- Single harvester, multiple forks harvested

- Ceres is based on Chia's source code, with least modification

- Ceres is running with only one harvester server, not each server for each fork

- Almost same cpu and memory usage as a single Chia harvester 

- Follow Chia's asyncio design pattern,  by principle multiple forks activities will not affect Chia harvestering

- Easy to configure to support more forks as you wish

- Multi-platforms supported, such as Raspberry Pi

---

# Installing

Ceres can be installed by the same way installing Chia normally.

```
git clone https://github.com/hulatangchen/ceres-combineharvester.git -b latest

cd ...

sh install.sh

. ./activate
```

---

# Init

if you have setup forks you want to harvest, it is to say you have got .chia or .forks under your home directory, you an just skip this chapter to Run

here we init from absolutly fresh install, just run:

1. ```
   chia init_all
   ```
   
   this command will generate root path for each forks, like .chia, .flax under your home directory

next we generate ssl files for each forks, for example you want to harvest flax:

1. copy ca directory from you farmer computer to local [path_to_ca]

2. run:
   
   ```
   chia init -n flax -c [path_to_ca]
   ```

Finally, what you need to change is your famer-peer ip address under Harvester section(not full node section) in each fork's config.yaml

---

# Run

activate venv first, then run:

```
chia start harvester -r
```

---

# Network Architecture

Defult Chia Harvester and Famer is structured as below

<img src="file:///home/eric/develope/chia_default_net_structure.jpg" title="" alt="alt txt" data-align="center">

By Chia default, you should run one harvester for each fork's farmer.



Ceres has a different structure, like below:

<img title="" src="file:///home/eric/develope/ceres_network.png" alt="alt txt" data-align="center" width="486">

By using Ceres, you can run an unique Harvester server which will response to all the farmer's request. Thanks to Chia's asyncio pattern, a single Harvester server has enough throughput  to proccess farmer's asynchronous challenge hash request.





---

# Compatibility

For a harvester, it is responsible for communicating with famer by complying chia's Harvester Protocol.

Inspecting most fork's source code shown that there exsits two way to modify Chia's source code.

1.  Chia family:
   
   forks like flax, goji and many uses the exactly same harvester protocol as Chia

2. Spare family:
   
   forks like spare uses their extended harvester protocol
   
   

Currently, Creres only support the Chia family forks, these fork's harvester say the same language to their farmer like Chia does.

Spare family forks will be supported very soon.

    

---

# How to add more forks?

It is easy for Ceres to add more forks support .

Just download the all-coin-config.yaml from github and replace the old file in chia/util  subdirectory.

then run:

```
chia stop all -d
chia start harvester -r
```
