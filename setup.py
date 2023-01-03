from setuptools import setup

dependencies = [
    "blspy==1.0.5",  # Signature library
    "chiavdf==1.0.3",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.4",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.10",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the ceres processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
    "watchdog==2.2.1",  # Filesystem event watching - watches keyring.yaml
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="ceres-blockchain",
    author="Hulatang",
    author_email="hulatang@ceres.net",
    description="Ceres blockchain full node, farmer, timelord, and wallet.",
    url="https://ceres.net/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="ceres blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "ceres",
        "ceres.cmds",
        "ceres.clvm",
        "ceres.consensus",
        "ceres.consensus.all_coins_default_constants",
        "ceres.daemon",
        "ceres.full_node",
        "ceres.timelord",
        "ceres.farmer",
        "ceres.harvester",
        "ceres.introducer",
        "ceres.plotting",
        "ceres.pools",
        "ceres.protocols",
        "ceres.rpc",
        "ceres.server",
        "ceres.simulator",
        "ceres.types.blockchain_format",
        "ceres.types",
        "ceres.util",
        "ceres.util.coins_initial_config",
        "ceres.wallet",
        "ceres.wallet.puzzles",
        "ceres.wallet.rl_wallet",
        "ceres.wallet.cc_wallet",
        "ceres.wallet.did_wallet",
        "ceres.wallet.settings",
        "ceres.wallet.trading",
        "ceres.wallet.util",
        "ceres.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "ceres = ceres.cmds.ceres:main",
            "ceres_wallet = ceres.server.start_wallet:main",
            "ceres_full_node = ceres.server.start_full_node:main",
            "ceres_harvester = ceres.server.start_harvester:main",
            "ceres_farmer = ceres.server.start_farmer:main",
            "ceres_introducer = ceres.server.start_introducer:main",
            "ceres_timelord = ceres.server.start_timelord:main",
            "ceres_timelord_launcher = ceres.timelord.timelord_launcher:main",
            "ceres_full_node_simulator = ceres.simulator.start_simulator:main",
        ]
    },
    package_data={
        "ceres": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "ceres.util": ["*.yaml", "english.txt"],
        "ceres.util.coins_initial_config": ["*.yaml"],
        "ceres.ssl": ["chia_ca.crt", "chia_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
