from itertools import chain
import solcx
import json
import random
from web3 import Web3
from utils import *
from const import *
from dotenv import load_dotenv

if __name__ == '__main__':
    solcx.install_solc(SOL_VERSION)

    with open(ABI_FILE, "w") as abi_file:
        abi_file.write("") # empty the file

    with open("{}{}".format(CONTRACTS_DIR, SOL_FILENAME), "r") as file:
        sol_content = file.read()

    compiled_sol = solcx.compile_standard(
        {
            "language": "Solidity",
            "sources": {
                SOL_FILENAME: {
                    "content": sol_content
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            }
        },
        solc_version=SOL_VERSION
    )

    with open("compiled_code.json", "w") as compiled_file:
        json.dump(compiled_sol, compiled_file)

    bytecode = compiled_sol["contracts"][SOL_FILENAME][CONTRACT_NAME]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][SOL_FILENAME][CONTRACT_NAME]["abi"]

    with open(ABI_FILE, "w") as abi_file:
        json.dump(abi, abi_file)

    if SERVER_MODE == HARDHAT_SERVER_OPTION:
        w3 = Web3(Web3.HTTPProvider(HARDHAT_RPC_SERVER))
    elif SERVER_MODE == GANACHE_SERVER_OPTION:
        w3 = Web3(Web3.HTTPProvider(GANACHE_RPC_SERVER))
    elif SERVER_MODE == RINKEBY_SERVER_OPTION:
        w3 = Web3(Web3.HTTPProvider(RINKEBY_INFURA_RPC_SERVER))

    connected = w3.isConnected()
    if not connected:
        print("The chain is unavailable!")
        exit(1)

    if SERVER_MODE == HARDHAT_SERVER_OPTION:
        chain_id = HARDHAT_CHAIN_ID
        my_address = w3.toChecksumAddress(HARDHAT_ACCOUNT_PUBLIC_KEY)
        private_key = HARDHAT_ACCOUNT_PRIVATE_KEY
    elif SERVER_MODE == GANACHE_SERVER_OPTION:
        chain_id = GANACHE_CHAIN_ID
        my_address = w3.toChecksumAddress(GANACHE_ACCOUNT_PUBLIC_KEY)
        private_key = GANACHE_ACCOUNT_PRIVATE_KEY    
    elif SERVER_MODE == RINKEBY_SERVER_OPTION:
        my_address = w3.toChecksumAddress(RINKEBY_ACCOUNT_PUBLIC_KEY)
        private_key = RINKEBY_ACCOUNT_PRIVATE_KEY
        chain_id = 4
 
    # ---
    # Deploy a contract
 
    this_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(my_address)
    logger.info("Txn count = nonce = {}".format(nonce))
 
    txn = this_contract.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
            "gasPrice": w3.eth.gas_price
        }
    )
 
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.info("Waiting to deploy transaction!")
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    created_contract_address = txn_receipt.contractAddress
    logger.info("Done! Contract deployed to {}".format(created_contract_address))
