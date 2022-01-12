import json
from cryptography.fernet import Fernet
import base58
from nacl.public import PrivateKey
from solana.keypair import Keypair
from Metaplex.metaplex.transactions import deploy, topup, mint, send, burn, update_token_metadata, accountInfo, getDataByOwner
from Metaplex.utils.execution_engine import execute


class MetaplexAPI:

    def __init__(self, cfg):
        self.private_key = list(base58.b58decode(cfg["PRIVATE_KEY"]))[:32]
        self.public_key = cfg["PUBLIC_KEY"]
        self.keypair = Keypair(PrivateKey(bytes(self.private_key)))
        self.cipher = Fernet(cfg["DECRYPTION_KEY"])

    @staticmethod
    def wallet():
        """ Generate a wallet and return the address and private key. """
        keypair = Keypair()
        pub_key = keypair.public_key
        private_key = list(keypair.seed)
        return json.dumps(
            {
                'address': str(pub_key),
                'private_key': private_key
            }
        )

    def deploy(self, api_endpoint, name, symbol, fees, max_retries=3, skip_confirmation=False, max_timeout=10,
               target=15, finalized=True):
        """
        Deploy a contract to the blockchain (on network that support contracts). Takes the network ID and contract
        name, plus initializers of name and symbol. Process may vary significantly between blockchains. Returns
        status code of success or fail, the contract address, and the native transaction data.
        """
        try:
            tx, signers, contract, metadata = deploy(
                api_endpoint, self.keypair, name, symbol, fees)
            resp = execute(
                api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["contract"] = contract
            resp["metadata"]=metadata
            resp["status"] = 200
            return json.dumps(resp)
        except:
            return json.dumps({"status": 400})

    def topup(self, api_endpoint, to, amount=None, max_retries=3, skip_confirmation=False, max_timeout=60, target=20,
              finalized=True):
        """
        Send a small amount of native currency to the specified wallet to handle gas fees. Return a status flag of
        success or fail and the native transaction data.
        """
        try:
            tx, signers = topup(api_endpoint, self.keypair, to, amount=amount)
            resp = execute(
                api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return json.dumps(resp)
        except:
            return json.dumps({"status": 400})

    def mint(self, api_endpoint, contract_key, dest_key, link, max_retries=3, skip_confirmation=False, max_timeout=20,
             target=1, finalized=True, supply=1):
        """
        Mints an NFT to an account, updates the metadata and creates a master edition
        """
        tx, signers, associated_token_account = mint(
            api_endpoint, self.keypair, contract_key, dest_key, link, supply=supply)
        resp = execute(
            api_endpoint,
            tx,
            signers,
            max_retries=max_retries,
            skip_confirmation=skip_confirmation,
            max_timeout=max_timeout,
            target=target,
            finalized=finalized,
        )
        resp["associated_token_account"] = associated_token_account
        resp["status"] = 200
        return json.dumps(resp)
        # except:
        #     return json.dumps({"status": 400})

    def update_token_metadata(self, api_endpoint, mint_token_id, link, data, creators_addresses, creators_verified,
                              creators_share, fee, max_retries=3, skip_confirmation=False, max_timeout=60, target=20,
                              finalized=True, supply=1):
        """
            Updates the json metadata for a given mint token id.
            """
        tx, signers = update_token_metadata(api_endpoint, self.keypair, mint_token_id, link, data, fee,
                                            creators_addresses, creators_verified, creators_share)
        resp = execute(
            api_endpoint,
            tx,
            signers,
            max_retries=max_retries,
            skip_confirmation=skip_confirmation,
            max_timeout=max_timeout,
            target=target,
            finalized=finalized,
        )
        resp["status"] = 200
        return json.dumps(resp)

    def send(self, api_endpoint, contract_key, sender_key, dest_key, encrypted_private_key, max_retries=3,
             skip_confirmation=False, max_timeout=60, target=20, finalized=True):
        """
        Transfer a token on a given network and contract from the sender to the recipient.
        May require a private key, if so this will be provided encrypted using Fernet: https://cryptography.io/en/latest/fernet/
        Return a status flag of success or fail and the native transaction data. 
        """
        try:
            private_key = list(self.cipher.decrypt(encrypted_private_key))
            tx, signers = send(api_endpoint, self.keypair,
                               contract_key, sender_key, dest_key, private_key)
            resp = execute(
                api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return json.dumps(resp)
        except:
            return json.dumps({"status": 400})

    def burn(self, api_endpoint, contract_key, owner_key, encrypted_private_key, max_retries=3, skip_confirmation=False,
             max_timeout=60, target=20, finalized=True):
        """
        Burn a token, permanently removing it from the blockchain.
        May require a private key, if so this will be provided encrypted using Fernet: https://cryptography.io/en/latest/fernet/
        Return a status flag of success or fail and the native transaction data.
        """
        try:
            private_key = list(self.cipher.decrypt(encrypted_private_key))
            tx, signers = burn(api_endpoint, contract_key,
                               owner_key, private_key)
            resp = execute(
                api_endpoint,
                tx,
                signers,
                max_retries=max_retries,
                skip_confirmation=skip_confirmation,
                max_timeout=max_timeout,
                target=target,
                finalized=finalized,
            )
            resp["status"] = 200
            return json.dumps(resp)
        except:
            return json.dumps({"status": 400})

    def getAccountInfo(self, api_endpoint, pub_key):
        try:
            data = accountInfo(api_endpoint, pub_key)
            data["status"] = 200
            return json.dumps(data)
        except:
            return json.dumps({"status": 400})

    def getAccountsByOwner(self,api_endpoint,owner,mint):
        try:
            data=getDataByOwner(api_endpoint,owner,mint)
            data['status']=200
            return json.dumps(data)
        except:
             return json.dump({"status": 400})

    