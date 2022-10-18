
from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from store_contract import *
from beaker import *

ALGOD_HOST = "http://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

ROOT_ACCOUNT_MNEMONIC = "point visa rotate quiz rice neutral tenant elephant toss verify syrup above seven question drive welcome loop goose kind define matrix lumber purity able roast"

ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

def get_create_store_app(app_id: int = 0):
    """
    Creates a store app and returns the appId. If the app_id exists already, return the application address 
    """
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
    app_client = client.ApplicationClient(
        algod_client, Store(), signer=ACCOUNT_SIGNER, app_id=app_id
    )

    if app_id == 0:
        # Create  an app client for our app
        app_id, app_addr, _ = app_client.create()
        print(f"Created app at {app_id} {app_addr}")
        app_client.fund(5 * consts.algo)
        print("Funded app")
        app_client.opt_in()
        print("Opted in")
    else:
        app_addr = get_application_address(app_id)

    app_state = app_client.get_application_state()
    print(f"Current app state:{app_state}")
    acct_state = app_client.get_account_state()
    print(f"Current account state:{acct_state}")

if __name__ == "__main__":
    print("Starting deploy of the Store App on Algorand TestNet...")
    get_create_store_app()