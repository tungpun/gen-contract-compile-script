import sys
import os

from dotenv import load_dotenv
from optparse import OptionParser

load_dotenv()

parser = OptionParser()

parser.add_option("-n", "--contract-name", dest="contract_name", help="contract name")
parser.add_option("-s", "--sol-file-contract", dest="contract_sol_file", help="contract file")
parser.add_option("-d", "--contract-dir", dest="contract_dir", help="directory contains sol contract files", default="contracts/")

(options, args) = parser.parse_args()



HARDHAT_SERVER_OPTION = 1
GANACHE_SERVER_OPTION = 2
RINKEBY_SERVER_OPTION = 3

# config the server mode
SERVER_MODE = RINKEBY_SERVER_OPTION

CONTRACTS_DIR = options.contract_dir
SOL_FILENAME = options.contract_sol_file
CONTRACT_NAME = options.contract_name

ABI_FILE = "output/abi.json"
BYTECODE_FILE = "output/bytecode.json"
SAMPLE_WEB3_FILE = "output/sample-web3.js"

HARDHAT_ACCOUNT_PUBLIC_KEY = os.getenv("HARDHAT_ACCOUNT_PUBLIC_KEY")
HARDHAT_ACCOUNT_PRIVATE_KEY = os.getenv("HARDHAT_ACCOUNT_PRIVATE_KEY")
HARDHAT_RPC_SERVER = os.getenv("HARDHAT_RPC_SERVER")
HARDHAT_CHAIN_ID = os.getenv("HARDHAT_CHAIN_ID")

GANACHE_RPC_SERVER = os.getenv("GANACHE_RPC_SERVER")
GANACHE_ACCOUNT_PUBLIC_KEY = os.getenv("GANACHE_ACCOUNT_PUBLIC_KEY")
GANACHE_ACCOUNT_PRIVATE_KEY = os.getenv("GANACHE_ACCOUNT_PRIVATE_KEY")
GANACHE_CHAIN_ID = os.getenv("GANACHE_CHAIN_ID")

RINKEBY_ACCOUNT_PUBLIC_KEY = os.getenv("RINKEBY_ACCOUNT_PUBLIC_KEY")
RINKEBY_ACCOUNT_PRIVATE_KEY = os.getenv("RINKEBY_ACCOUNT_PRIVATE_KEY")

RINKEBY_INFURA_RPC_SERVER = os.getenv("RINKEBY_INFURA_RPC_SERVER")
