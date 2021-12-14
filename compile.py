from itertools import chain
import solcx
import json
import random
from web3 import Web3
from utils import *
from const import *
from dotenv import load_dotenv

if __name__ == '__main__':
    sol_version = get_sol_version(CONTRACTS_DIR + SOL_FILENAME)
    solcx.install_solc(sol_version)

    with open(ABI_FILE, "w") as abi_file:
        abi_file.write("") # empty the file

    sol_content = load_sol_content()

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
        solc_version=sol_version
    )

    with open("compiled_code.json", "w") as compiled_file:
        json.dump(compiled_sol, compiled_file)

    bytecode = compiled_sol["contracts"][SOL_FILENAME][CONTRACT_NAME]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][SOL_FILENAME][CONTRACT_NAME]["abi"]

    with open(ABI_FILE, "w") as abi_file:
        json.dump(abi, abi_file)

    with open(BYTECODE_FILE, "w") as bc_file:
        json.dump(bytecode, bc_file)

    with open(SAMPLE_WEB3_FILE, "w") as f:
        f.write(
            """
abi={abi};
bytecode="{bytecode}";
    
{contract_name}Contract = await new web3.eth.Contract(abi)
.deploy({{ 
    data: bytecode, 
    arguments: [] // Writing you constructor's arguments in the array
}})
.send({{ from: web3.currentProvider.selectedAddress }});
            """.format(
                abi=json.dumps(abi),
                bytecode=bytecode,
                contract_name=CONTRACT_NAME
            )
        )

    logger.info("Compiled the contract already!")
    logger.info("abi file:\t\t{}".format(ABI_FILE))
    logger.info("bytecode file:\t\t{}".format(BYTECODE_FILE))
    logger.info("sample web3 file:\t{}".format(SAMPLE_WEB3_FILE))
