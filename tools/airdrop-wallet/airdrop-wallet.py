import os
import argparse
import json

from iota_wallet import IotaWallet, StrongholdSecretManager
from dotenv import load_dotenv


def main():
    ## Get commandline arguments
    parser = argparse.ArgumentParser(prog='airdrop-snake', description='shadowban.me airdrop tool')

    # # Required positional argument
    parser.add_argument('tool', type=str,
                        help='Tool to use: wallet-create, addresses-get')
    # # Optional positional argument
    # parser.add_argument('opt_pos_arg', type=int, nargs='?',
    #                     help='An optional integer positional argument')
    # Optional argument
    parser.add_argument('--input', type=str,
                        help='Filename of input file')
                        
    parser.add_argument('--out', type=str,
                        help='Filename of output file')
    # # Switch
    # parser.add_argument('--switch', action='store_true',
    #                     help='A boolean switch')

    args = parser.parse_args()

    # print("Argument values:")
    print("Using tool: " + args.tool)
    #print(args.input)
    #print(args.out)
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
        case "addresses-get":
            in_file = args.input
            out_file = args.out
            addresses = []
            if in_file == None:
                print("no input file specied: trying default 'comments.json'")
                in_file = "comments.json"
            print("reading " + in_file)
            f = open(in_file, encoding='utf8')
            if in_file.endswith(".json"):
                data = json.load(f)
                addresses = look_thru(data)
            if len(addresses) > 0:
                print("Found "+len(addresses)+" addresses")
                if out_file == None:
                    print("no input file specied: using default 'addresses.txt'")
                    out_file = "addresses.txt"
            
                
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

def look_thru(data):
    #print("looking thru data...")
    found = []
    for k, v in data.items():
        #print(v)
        #if v is dict:
        if hasattr(v, "items"):
            subfound = look_thru(v)
            found += subfound
        if k == "text" and isinstance(v, str):
             #print(v)
             words = v.split()
             for w in words:
                if w.startswith("smr1"):
                    #print(w)
                    found.append(w)
    return found

if __name__ == "__main__":
    main()