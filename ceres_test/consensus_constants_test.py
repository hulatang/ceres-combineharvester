import os
from importlib import util, import_module
from pathlib import Path
import os
MODULE_EXTENSIONS = '.py'


# all_consensus_directory_str = "../ceres/consensus/all_coins_default_constants"

package_name = "ceres.consensus.all_coins_default_constants"

def package_contents(package_name):
    spec = util.find_spec(package_name)
    if spec is None:
        return set()

    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith(MODULE_EXTENSIONS):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= package_contents(current)


    return ret

ret = sorted(package_contents(package_name))

print("Start scanning consensud constants files.")
print("")
for r in ret:
    try:
        m = import_module(r)
    except TypeError as e:
        print('Found Error:')
        print(f"Coin: {r.split('.')[-1]}")
        print("Error: ", e)
    except Exception as e:
        print('Got unkown error: ', e)
    finally:
        print(f"Coin: {r.split('.')[-1]} passed")
        print("")

