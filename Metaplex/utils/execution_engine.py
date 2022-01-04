import time
from solana.rpc.api import Client
from solana.rpc.types import TxOpts


def remove_duplicated(items):
    # removes duplicated items in an iterator while preserving order
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]


def execute(api_endpoint, tx, signers, max_retries=3, skip_confirmation=True, max_timeout=20, target=1,
            finalized=True):
    client = Client(api_endpoint,'confirmed',True)
    signers = remove_duplicated(signers)
    last_error = None
    for attempt in range(max_retries):
        try:
            result = client.send_transaction(tx, *signers, opts=TxOpts(skip_preflight=True,skip_confirmation=True,preflight_commitment='confirmed'))
            signatures = [x.signature for x in tx.signatures]
            if not skip_confirmation:
                await_confirmation(client, signatures, max_timeout, target, finalized)
            return result
        except Exception as e:
            print(f"Failed attempt {attempt}: {e}")
            last_error = e
            continue
    raise last_error


def await_confirmation(client, signatures, max_timeout=20, target=1, finalized=True):
    elapsed = 0
    while elapsed < max_timeout:
        sleep_time = 1
        time.sleep(sleep_time)
        elapsed += sleep_time
        resp = client.get_signature_statuses(signatures)
        if resp["result"]["value"][0] is not None:
            confirmations = resp["result"]["value"][0]["confirmations"]
        else:
            continue
        
        if confirmations >= target :
            print(f"Took {elapsed} seconds to confirm {confirmations} confirmation for transaction")
            return
