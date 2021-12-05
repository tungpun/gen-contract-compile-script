import logging
import sys
import re

LOG_FILE_NAME = 'app.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(LOG_FILE_NAME)
file_handler.setFormatter(formatter)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def get_sol_version(sol_filename):
    with open(sol_filename, 'r') as f:
        file_content = f.read()
    for line in file_content.splitlines():
        if "pragma solidity" in line:
            versions = re.findall('[0-9.]+', line)
            if len(versions) == 0:
                return None
            return versions[-1]
    return None