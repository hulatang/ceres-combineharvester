# -*- mode: python ; coding: utf-8 -*-
import importlib
import pathlib
import platform
import os

from pkg_resources import get_distribution

from PyInstaller.utils.hooks import collect_submodules, copy_metadata

THIS_IS_WINDOWS = platform.system().lower().startswith("win")

ROOT = pathlib.Path(importlib.import_module("ceres").__file__).absolute().parent.parent


def solve_name_collision_problem(analysis):
    """
    There is a collision between the `ceres` file name (which is the executable)
    and the `ceres` directory, which contains non-code resources like `english.txt`.
    We move all the resources in the zipped area so there is no
    need to create the `ceres` directory, since the names collide.

    Fetching data now requires going into a zip file, so it will be slower.
    It's best if files that are used frequently are cached.

    A sample large compressible file (1 MB of `/dev/zero`), seems to be
    about eight times slower.

    Note that this hack isn't documented, but seems to work.
    """

    zipped = []
    datas = []
    for data in analysis.datas:
        if str(data[0]).startswith("ceres/"):
            zipped.append(data)
        else:
            datas.append(data)

    # items in this field are included in the binary
    analysis.zipped_data = zipped

    # these items will be dropped in the root folder uncompressed
    analysis.datas = datas


keyring_imports = collect_submodules("keyring.backends")

# keyring uses entrypoints to read keyring.backends from metadata file entry_points.txt.
keyring_datas = copy_metadata("keyring")[0]

version_data = copy_metadata(get_distribution("ceres-blockchain"))[0]

block_cipher = None

SERVERS = [
    "wallet",
    "full_node",
    "harvester",
    "farmer",
    "introducer",
    "timelord",
]

# TODO: collapse all these entry points into one `chia_exec` entrypoint that accepts the server as a parameter

entry_points = ["ceres.cmds.ceres"] + [f"ceres.server.start_{s}" for s in SERVERS]

hiddenimports = []

coin_constants_path = f"{ROOT}/ceres/consensus/all_coins_default_constants"

constants_files = []

all_files = os.listdir(coin_constants_path)

for f in all_files:
  if f == "__init__.py":
    continue
  constants_files.append("ceres/consensus/all_coins_default_constants/" + f)

hiddenimports.extend(constants_files)
hiddenimports.extend(entry_points)
hiddenimports.extend(keyring_imports)

binaries = []


if THIS_IS_WINDOWS:
    hiddenimports.extend(["win32timezone", "win32cred", "pywintypes", "win32ctypes.pywin32"])

# this probably isn't necessary
if THIS_IS_WINDOWS:
    entry_points.extend(["aiohttp", "ceres.util.bip39"])

if THIS_IS_WINDOWS:
    ceres_mod = importlib.import_module("ceres")
    dll_paths = ROOT / "*.dll"

    binaries = [
        (
            dll_paths,
            ".",
        ),
        (
            "C:\\Windows\\System32\\msvcp140.dll",
            ".",
        ),
        (
            "C:\\Windows\\System32\\vcruntime140_1.dll",
            ".",
        ),
    ]


datas = []

datas.append((f"{ROOT}/ceres/util/english.txt", "ceres/util"))
datas.append((f"{ROOT}/ceres/util/*.yaml", "ceres/util"))
datas.append((f"{ROOT}/ceres/util/coins_initial_config/*.yaml", "ceres/util/coins_initial_config"))
datas.append((f"{ROOT}/ceres/wallet/puzzles/*.hex", "ceres/wallet/puzzles"))
datas.append((f"{ROOT}/ceres/ssl/*", "ceres/ssl"))
datas.append((f"{ROOT}/mozilla-ca/*", "mozilla-ca"))
datas.append(version_data)

pathex = []


def add_binary(name, path_to_script, collect_args):
    analysis = Analysis(
        [path_to_script],
        pathex=pathex,
        binaries=binaries,
        datas=datas,
        hiddenimports=hiddenimports,
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False,
    )

    solve_name_collision_problem(analysis)

    binary_pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)

    binary_exe = EXE(
        binary_pyz,
        analysis.scripts,
        [],
        exclude_binaries=True,
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
    )

    collect_args.extend(
        [
            binary_exe,
            analysis.binaries,
            analysis.zipfiles,
            analysis.datas,
        ]
    )


COLLECT_ARGS = []

add_binary("ceres", f"{ROOT}/ceres/cmds/ceres.py", COLLECT_ARGS)
add_binary("daemon", f"{ROOT}/ceres/daemon/server.py", COLLECT_ARGS)

for server in SERVERS:
    add_binary(f"start_{server}", f"{ROOT}/ceres/server/start_{server}.py", COLLECT_ARGS)

COLLECT_KWARGS = dict(
    strip=False,
    upx_exclude=[],
    name="daemon",
)

coll = COLLECT(*COLLECT_ARGS, **COLLECT_KWARGS)
