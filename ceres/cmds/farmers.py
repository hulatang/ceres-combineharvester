from logging import root
from typing import List
from collections import Counter
import click
import sys
from ipaddress import ip_address

from ceres.util.ceres_config import get_valid_coin_names
from ceres.util.config import load_config
from ceres.util.default_root import DEFAULT_CERES_ROOT_PATH



VALID_COIN_NAMES = get_valid_coin_names()


@click.group("farmers", short_help="Mangager Farmers")
@click.pass_context
def farmers_cmd(ctx: click.Context):
    print("inside farmers")




@farmers_cmd.command("show", short_help="Show Farmers")
@click.pass_context
def show_cmd(
    ctx: click.Context
):
    print('farmer show')

    root_path  = ctx.obj["root_path"]
    ceres_config = load_config(root_path, filename="coins_config.yaml")
    farmer_machine = ceres_config["farmer_machine"]

    if not farmer_machine:
        print("No Farmer Peer set")
        print("run ceres farmers add to add new farmer peers")
        return 

    print("-" * 50)
    detect_conflict()



    print("-" * 50)
    print("All Farmer Peers:")
    for farmer in farmer_machine:
        print(f"Famer Peer")
        host = farmer["farmer_peer"]["address"]
        coins = farmer["farmer_peer"]["coins"]
        print(f"    Address: {host}")
        print(f"    coins: {coins}")
        print("")
    print("-" * 50)

    valid_coins = get_valid_coin_names()
    print("")
    print(f"Ceres currently support {len(valid_coins)} coins:")
    print("")
    print(sorted(valid_coins))







@farmers_cmd.command("add", short_help="Add Farmer Peers")
@click.option("--host", help="Farmer peer IP address", type=str, required=True)
@click.option("-c", "--coins", help="coins to harvester", type=click.Choice(VALID_COIN_NAMES), multiple=True, required=True)
@click.pass_context
def add_cmd(
    ctx: click.Context,
    host: str,
    coins: str
):
    try:
        input_host = ip_address(host)
    except ValueError as e:
        print("Invalid IP address:", e)
        return
    
    
    
    # print(f"Ceres Root Path: {ctx['root_path']}")
    root_path = ctx.obj["root_path"]
    print(root_path)
    print(f"You Input IP: {host}")
    print("Coins: ", coins)

    ceres_config = load_config(DEFAULT_CERES_ROOT_PATH, filename="coins_config.yaml")

    farmer_machine = ceres_config["farmer_machine"]

    # farmer_peer = None

    if not farmer_machine:
      farmer_peer = {
          "address": format(input_host),
          "coins": coins
      }  
      print(f"Farmer peer {host} added")
      return 
    

    for farmer in farmer_machine:
        farmer_peer = farmer["farmer_peer"]
        farmer_host = ip_address(farmer_peer["address"])
        if farmer_host == input_host:
            mining_coins = set(farmer_peer["coins"])
            mining_coins.update(coins)
            farmer_peer["coins"] = list(mining_coins)
            print(f"Farmer Peer {farmer_host} exists, coins added")
            return
    
    farmer_peer = {
        "address": format(input_host),
        "coins": coins
    }  
    farmer_machine.append(
        {
            "farmer_peer": farmer_peer
        }
    )
    print(f"Farmer peer {host} added")
 


# def check_conflict(host, coins):
def detect_conflict():
    ceres_config = load_config(DEFAULT_CERES_ROOT_PATH, filename="coins_config.yaml")
    farmer_machine = ceres_config["farmer_machine"]

    if not farmer_machine:
        return False
    
    err = False

    detect_valid_name(farmer_machine)
    
    try:
        detect_duplicated_hosts(farmer_machine)
    except ValueError as e:
        err = True
        cnt = e.args[0]
        for h, c in cnt.items():
            print(f"Error: Found duplicated host {h} {c} times.")
        print("")
    #     # return -1
    
    try:
        detect_duplicated_coins(farmer_machine)
    except ValueError as e:
        err = True
        err = e.args[0]
        for name, hosts in err.items():
            print(f"Error: Found duplicated coin names \"{name}\": in hosts: {hosts}")
        print("")
    
    # if err:
    #     sys.exit("Found error, fix the conflicts.")
    

    


    # for farmer in farmer_machine:
    #     farmer_peer = farmer_machine["farmer_peer"]
    #     farmer_host = farmer_peer["address"]
    #     mining_coins = farmer_peer["coins"]
    #     duplicated_coins = [c for c in coins if c in mining_coins]


def detect_duplicated_hosts(famer_machine):
    hosts = []
    for farmer in famer_machine:
        hosts.append(farmer["farmer_peer"]["address"])
    
    if not hosts:
        return

    cnt = Counter()
    for host in hosts:
        cnt[host] += 1

    not_duplicated_host = [host for host in cnt if cnt[host] == 1]

    for h in not_duplicated_host:
        cnt.pop(h)
    
    if cnt:
        raise ValueError(cnt)
        # err = f""
        # for h, c in cnt.itmes():
        #     err += f"Found duplicated host: {h} {c} times\n"
        # raise ValueError(err)
    else:
        return 




def detect_duplicated_coins(farmer_machine):
    cnt = Counter()

    for farmer in farmer_machine:
        coins = farmer["farmer_peer"]["coins"]
        for name in coins:
            cnt[name] += 1
    
    not_duplicated_names = [name for name in cnt if cnt[name] == 1]
    for dn in not_duplicated_names:
        cnt.pop(dn)
    
    # for name, c in cnt.items():
    #     if c == 1:
    #         cnt.pop(name)
    
    if not cnt:
        return
    
    err = {}

    for name in cnt:
        hosts = []
        for farmer in farmer_machine:
            coins = farmer["farmer_peer"]["coins"]
            if name in coins:
                hosts.append(farmer["farmer_peer"]["address"])
        err[name] = hosts
    
    raise ValueError(err)

def detect_valid_name(farmer_machine):
    valid_names = get_valid_coin_names()
    not_supported_names = []

    for farmer in farmer_machine:
        coins = farmer["farmer_peer"]["coins"]
        unsupported_names = [name for name in coins if name not in valid_names]
        not_supported_names.extend(unsupported_names)
    
    print("")
    for name in not_supported_names:
        print(f"Error: Found coins not supported: {name}")
    print("")
    




 
    











