import json
from Inscape.__init__ import logger
import time
from datetime import date, timedelta
from arweave.arweave_lib import Wallet, Transaction
from cryptography.fernet import Fernet
from Metaplex.api.metaplex_api import MetaplexAPI as metaPlexPythonLib
from solana.rpc.api import Client
from Metaplex.metaplex.metadata import get_metadata
from Inscape import configutils
from django.db import IntegrityError
from django.http import JsonResponse
from .models import *
from .forms import *
from .serializers import *
from datetime import date, timedelta, datetime
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.db.models import Q


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
IMAGE_URI = "https://raw.githubusercontent.com/DevVarunn/CDN/main/Sample_House2.png"

DEPLOYED = []
MINTED = []

# METAPLEX SETUP
cfg = {"PRIVATE_KEY": TEST_PRIVATE_KEY, "PUBLIC_KEY": TEST_PUBLIC_KEY,
       "DECRYPTION_KEY": SERVER_DECRYPTION_KEY}
api = metaPlexPythonLib(cfg)

# ARWEAVE WALLET CONNECTION

wallet_file_path = "apps/solNFT/awarekeypair.json"
wallet = Wallet(wallet_file_path)

# SOLANA NETWORK SET
api_endpoint = "https://api.devnet.solana.com"
# api_endpoint ="http://127.0.0.1:8899"
# api_endpoint ="https://api.testnet.solana.com"

res = Client(api_endpoint)

# returns the errors/messages string stored in config.ini


def responseMessage(arg):
    return configutils.getProperties('MESSAGES', arg)


# ALTER THE JSON FILE
def _alterJson(_date):
    with open('Metaplex/metadata/metadata.json', 'r+') as f:
        data = json.load(f)

        # <--- add `id` value.
        data['attributes'][0] = {"trait_type": "AccessDate", "value": _date}
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

    DEPLOYED = []
    MINTED = []
    data = {}

    # FETCH THE NUMBER OF DAYS
    number_of_days = _findNumberOfDays(_years)

    for i in range(1):
        # the current count of nft
        print(f"currently minting {i+1} .No NFT")

        # alter the json file using todays date
        todayDateString = todays_date.strftime("%m/%d/%Y")
        _alterJson(todayDateString)

        # read the json file and upload to arweave
        # with open('Metaplex/metadata/metadata.json', 'r') as notjson:
        #     Json_data = notjson.read()
        #     transaction = Transaction(wallet, data=Json_data)
        #     transaction.add_tag('Content-Type', 'application/json')
        #     transaction.sign()
        #     # Get the trnsaction id for arweave
        #     trx_id = transaction.id
        #     transaction.send()

        # create the account
        result = json.loads(api.deploy(
            api_endpoint, TOKEN_NAME, TOKEN_SYMBOL, 0))
        # print(f'\n i am sleeping 5s for this to work')
        # time.sleep(5)

        # check the result status or fail
        assert result['status'] == 200, "Sorry the account deploy failed"

        contract_key = result.get('contract')
        # DEPLOYED.append(contract_key)

        # Create actual token
        minted = json.loads(api.mint(
            api_endpoint, contract_key, TEST_PUBLIC_KEY, "https://raw.githubusercontent.com/DevVarunn/CDN/main/metadata.json"))
        # MINTED.append(minted)
        print(f'\n i am sleeping 3s for this to work')
        time.sleep(3)
        data1 = json.loads(api.getAccountInfo(
            api_endpoint, minted['associated_token_account']))
        # data2=json.loads(api.getAccountInfo(api_endpoint,result['metadata']))

        # data2=get_metadata(res,data1['result']['value']['data']['parsed']['info']['mint'])
        # print(f"\n the data by owner is : {api.getAccountsByOwner(api_endpoint,TEST_PUBLIC_KEY,minted['associated_token_account'])}")

        # add data to the object
        data['token_no'] = str(i)
        # data['contract'] = contract_key
        # data['deploy_trx'] = result['result']
        # data['associated_token_account'] = minted['associated_token_account']
        # data['mint_trx'] = minted['result']
        data['SPL_TOKEN'] = data1['result']['value']['data']['parsed']['info']['mint']
        data['METADATA_ACCOUNT'] = result['metadata']
        # data['token_data']=str(data2)

        MINTED.append(data)
        data = {}

        assert minted['status'] == 200, "Sorry the token mint failed"

        todays_date += timedelta(days=1)

    end = time.time()
    response = {
        'status': 200,
        'message': 'success',
        'time': time.strftime("%H:%M:%S", time.gmtime(end-start)),
        'Master_Data': {'symbol': TOKEN_SYMBOL, 'name': TOKEN_NAME, 'image': IMAGE_URI},
        'data': MINTED,
    }

    print("********************************")
    print("time taken :", time.strftime("%H:%M:%S", time.gmtime(end-start)))
    print("********************************")
    print("Finished minting")
    print("All Accounts : ", DEPLOYED)
    print("All Minted   : ", MINTED)
    return response


####   Stored user details in UserMaster table #####

def saveUserDetails(body):
    logger.info("---START FUNCTION: saveUserDetails(body)/service---")
    try:
        logger.info(f"body of function is : {body}")
        body['dDOB'] = datetime.strptime(body['dDOB'], '%d/%m/%Y')
        body['sPassword'] = make_password(body['sPassword'])
        fd = userMasterMapping(body)

        if fd.is_valid():
            if User.objects.filter(sWalletAddress=body['sWalletAddress'], sEmailaddress=body['sEmailaddress']).exists():
                logger.info("User already exists:")
                response = {
                    'status': False,
                    'message': responseMessage('user_is_already_Exists')
                }
                return response
            else:
                logger.info("User has been created successfully")
                fd.save()
                response = {
                    'status': True,
                    'message': responseMessage('user_created')
                }
                return response

        else:
            print(fd.errors)
            logger.error(f"Error ocuured for saving data : {fd.errors}")
            response = {
                'status': False,
                'Error': fd.errors
            }
            return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except User.DoesNotExist:
        response = {'status': False, 'message': responseMessage(
            'user_is_already_Exists')}
        return response


def login(username, password):
    try:
        user = User.objects.get(username=username)
        print(user.username)
        user = User.objects.get(username=username)
        if check_password(password, user.sPassword):
            token = Token.objects.filter(user=user)
            if(token.exists()):
                token = Token.objects.get(user=user)
            else:
                token = Token.objects.create(user=user)

            response = {
                'status': True,
                'message': responseMessage('login_success'),
                'token': token.key
            }
            return response

        else:
            response_message = responseMessage('invalid_username_or_password')

            response = {
                'status': False,
                'message': response_message,
            }
            return response
    except User.DoesNotExist:
        response_message = responseMessage('invalid_username_or_password')
        response = {'status': False, 'message': response_message}
        return response


def logout(token):
    logger.info("---START FUNCTION: logout(token)/service---")
    try:
        token = Token.objects.get(key=token)
        token.delete()
        response = {'status': 'True',
                    'message': responseMessage('User_Loged_Out')}
        return response
    except Token.DoesNotExist as e:
        response_message = responseMessage('authorization_fail')
        response = {'status': 'False', 'message': response_message}
        logger.error(f"Authorization Fail: {e}")
        return response


####   retrieve user details from UserMaster table #####

def getUserDetails(token):
    logger.info("---START FUNCTION: getUserDetails(token)/service---")
    try:
        logger.info(f"Token of that user is  : {token}")
        token = Token.objects.get(key=token)
        user = User.objects.get(pk=token.user_id)
        user1 = UserSerializer(user, many=False)
        userData = json.loads(json.dumps(user1.data))
        response = {
            'status': True,
            'data': userData
        }
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except User.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response
    except Token.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response


def getAllProperty():
    logger.info("---START FUNCTION: getAllProperty(token)/service---")
    try:
        data = PropertyMaster.objects.all()
        data2 = propertySerializer(data, many=True)

        dataFinal={}

        for data in json.loads(json.dumps(data2.data)):
            dataFinal[data["sPropertyName"]]=data
     
        response = {
            'status': True,
            'data': dataFinal
        }
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except PropertyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response


def getAllPropertyFiltered(body):
    logger.info("---START FUNCTION: getAllProperty(token)/service---")
    try:

        filters = {}
        if body['ePropertyCategoryId']:
            filters['ePropertyCategoryId'] = body['ePropertyCategoryId']
        if body['pricemax']:
            filters['fPropertyCurrentPrice__lte'] = body['pricemax']
        if body['pricemin']:
            filters['fPropertyCurrentPrice__gte'] = body['pricemin']
        if body['iCurrencyId']:
            filters['iCurrencyId']=body['iCurrencyId']
        
        filter_q = Q(**filters)
        print(f"Filter {filter_q}")
        filteredData = PropertyMaster.objects.filter(filter_q)

        data2 = propertySerializer(filteredData, many=True)
        dataFinal={}

        for data in json.loads(json.dumps(data2.data)):
            dataFinal[data["sPropertyName"]]=data

        response = {
            'status': True,
            'data': dataFinal
        }
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except PropertyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response
    except CurrencyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response


def getPropertyDetails(body):
    logger.info("---START FUNCTION: getProperty(token)/service---")
    try:
        propertydata=PropertyMaster.objects.get(sPropertyName=body['sPropertyName']) 
        data2 = propertySerializer(propertydata, many=False)

        dataFinal={}

        data=json.loads(json.dumps(data2.data))
        dataFinal[data["sPropertyName"]]=data


        response = {
            'status': True,
            'data': dataFinal
                }
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except PropertyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response
    except CurrencyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response

def getAccountInfo(body):
    
    logger.info("---START FUNCTION: getWalletInfo(token)/service---")
    try:
        walletAddress=body['wallet']
        data=json.loads(api.getAccountInfo(api_endpoint,walletAddress))
        if data['status']==200:
            sol=0.000000001*data['result']['value']['lamports']
            response = {
                'status': True,
                'data':  {
                'SOL':sol
                         }
                }

        else:
            response = {
                'status': False,
                 'message':"Error Occoured"
                }
            
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
  

def getAllCurrency():

    
    logger.info("---START FUNCTION: getAllCurrency(token)/service---")
    try:
        data = CurrencyMaster.objects.all()
        data2 = currencySerializer(data, many=True)

        dataFinal={}

        for data in json.loads(json.dumps(data2.data)):
            dataFinal[data["sCurrencyName"]]=data
     
        response = {
            'status': True,
            'data': dataFinal
        }
        return response

    except IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        response = {'Error': str(e)}
        return response
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        response = {'Key Error': str(e)}
        return response
    except CurrencyMaster.DoesNotExist:
        response = {'status': False,
                    'message': responseMessage('user_not_found')}
        return response
