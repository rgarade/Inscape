import json

from Inscape.__init__ import logger

import time

from datetime import date, timedelta

from arweave.arweave_lib import Wallet, Transaction

from cryptography.fernet import Fernet

from Metaplex.api.metaplex_api import MetaplexAPI as metaPlexPythonLib

# KEYPAIR SOLAN WALLET DETAILS
SERVER_DECRYPTION_KEY = Fernet.generate_key().decode("ascii")
TEST_PRIVATE_KEY = "4nGG6pSDX8vBMz4kU6rXLdeKisZz9De4sNaf4xfiWVghsdzBHUjmWPTjDsJ2hny5FDYqdbcer7J8RofAj8rriQBC"
TEST_PUBLIC_KEY = "FM7FYxjs7FVjK4Dw2HTuX7eaaLPAwmvGhY66rE9RDcFk"

# GLOBAL DATA
CREATOR_TOKEN_PUBLIC_KEY = "FM7FYxjs7FVjK4Dw2HTuX7eaaLPAwmvGhY66rE9RDcFk"
TOKEN_NAME = "FINAL TIME SHARE TOKEN"
TOKEN_SYMBOL = "FTST"
COLLECTION_NAME = "FINAL TIMESHARE RESORT"
COLLECTION_FAMILY = "FTRS"
IMAGE_URI = "https://arweave.net/Umi1tOw4hIPn8VkJtq_fjamMgT-YCOGa55g22t6sT6M?ext=jpg"

DEPLOYED=[]
MINTED=[]

# METAPLEX SETUP
cfg = {"PRIVATE_KEY": TEST_PRIVATE_KEY, "PUBLIC_KEY": TEST_PUBLIC_KEY, "DECRYPTION_KEY": SERVER_DECRYPTION_KEY}
api = metaPlexPythonLib(cfg)

# ARWEAVE WALLET CONNECTION

wallet_file_path = "apps/solNFT/awarekeypair.json"
wallet = Wallet(wallet_file_path)

# SOLANA NETWORK SET
api_endpoint = "https://api.devnet.solana.com"
# api_endpoint ="http://127.0.0.1:8899"
# api_endpoint ="https://api.testnet.solana.com"


# ALTER THE JSON FILE
def _alterJson(_date):
    with open('Metaplex/metadata/metadata.json', 'r+') as f:
        data = json.load(f)

        data['attributes'][0] = {"trait_type": "AccessDate", "value": _date}  # <--- add `id` value.
        data['name'] = TOKEN_NAME
        data['symbol'] = TOKEN_SYMBOL
        data['image'] = IMAGE_URI
        data['collection']['name'] = COLLECTION_NAME
        data['collection']['family'] = COLLECTION_FAMILY
        data['properties']['creators'][0]['address'] = CREATOR_TOKEN_PUBLIC_KEY

        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part
        f.close()  # close the file
    return True


# FUNCTION TO CALCULATE THE NUMBER OF DAYS
def _findNumberOfDays(_yearsOfLife):
    # creating the date object of today's date
    todays_date = date.today()
    current_year = todays_date.year
    # Count the number of days
    no_of_days = 0

    for yearAlive in range(_yearsOfLife):
        if _checkYearLeapOrNot(current_year):
            no_of_days += 366
        else:
            no_of_days += 365

        current_year += 1

    return no_of_days


# FUNCTION TO CHECK FOR LEAP YEAR
def _checkYearLeapOrNot(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# MINT TOKEN
def mintToken(_years: object):
    # get current date
    todays_date = date.today()
    start = time.time()

    DEPLOYED=[]
    MINTED=[]

    # FETCH THE NUMBER OF DAYS
    number_of_days = _findNumberOfDays(_years)

    for i in range(2):
        print("******************************************************")
        print(f"currently minting {i} th NFT")
        # alter the json file
        todayDateString = todays_date.strftime("%m/%d/%Y")
        _alterJson(todayDateString)

        # read the json file and upload to arweave
        with open('Metaplex/metadata/metadata.json', 'r') as notjson:
            Json_data = notjson.read()
            transaction = Transaction(wallet, data=Json_data)
            transaction.add_tag('Content-Type', 'application/json')
            transaction.sign()
            # Get the trnsaction id for arweave
            trx_id = transaction.id
            transaction.send()

        # create the account
        result = json.loads(api.deploy(api_endpoint, TOKEN_NAME, TOKEN_SYMBOL, 0))

        # check the result status or fail
        assert result['status'] == 200, "Sorry the account deploy failed"

        contract_key = result.get('contract')
        DEPLOYED.append(contract_key)

        # Create actual token
        minted = json.loads(api.mint(api_endpoint, contract_key, TEST_PUBLIC_KEY, "https://arweave.net/" + trx_id))
        MINTED.append(minted)

        assert minted['status'] == 200, "Sorry the token mint failed"

        todays_date += timedelta(days=1)

    end = time.time()
    response = {
        'status':True,
        'message':'Token has been created successfully',
        'time':time.strftime("%H:%M:%S", time.gmtime(end-start)),
        'tokens':10,
        'data': MINTED,
        'contracts':DEPLOYED
        }

    
    print("********************************")
    print("time taken :",time.strftime("%H:%M:%S", time.gmtime(end-start)))
    print("********************************")
    print("Finished minting")
    print("All Accounts : ", DEPLOYED)
    print("All Minted   : ", MINTED)
    return  response
    
