import os
import argparse

from iota_wallet import IotaWallet, StrongholdSecretManager
from dotenv import load_dotenv


## Get commandline arguments
parser = argparse.ArgumentParser(prog='airdrop-snake', description='shadowban.me airdrop tool')

# # Required positional argument
parser.add_argument('tool', type=str,
                     help='Tool to use: wallet-create')
# # Optional positional argument
# parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                     help='An optional integer positional argument')
# # Optional argument
# parser.add_argument('--opt_arg', type=int,
#                     help='An optional integer argument')
# # Switch
# parser.add_argument('--switch', action='store_true',
#                     help='A boolean switch')

args = parser.parse_args()

# print("Argument values:")
print("Using tool: " + args.tool)
# print(args.opt_pos_arg)
# print(args.opt_arg)
# print(args.switch)


## Load the .env variables

load_dotenv()
# Get the stronghold password
STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')


## Open wallet

wallet_options = {
    'nodes': ['https://api.testnet.shimmer.network'],
}

# Shimmer coin type
coin_type = 4219

secret_manager = StrongholdSecretManager("wallet.stronghold", STRONGHOLD_PASSWORD)

wallet = IotaWallet('./_airdrop-database', wallet_options, coin_type, secret_manager)


match args.tool:
    case "wallet-create":
        # mnemonic (seed) should be set only for new storage
        # once the storage has been initialized earlier then you should omit this step
        # Store the mnemonic in the Stronghold snapshot, this only needs to be done once
        seed = wallet.generate_mnemonic()
        print(seed)
        account = wallet.store_mnemonic(seed)
        account = wallet.create_account('Airdrop')
        print("Created account:")
        print(account)
    case _:
        print(args.tool + " is not a tool")

