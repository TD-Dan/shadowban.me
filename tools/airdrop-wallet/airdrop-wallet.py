import os
import time
import argparse
import json

from iota_wallet import IotaWallet, StrongholdSecretManager
from dotenv import load_dotenv


def main():
    ## Get commandline arguments
    parser = argparse.ArgumentParser(prog='airdrop-wallet', description='shadowban.me airdrop tool')

    # # Required positional argument
    parser.add_argument('tool', type=str,
                        help='Tool to use: wallet-create, wallet-status, wallet-claim-all\n wallet-airdrop \naddresses-get')
    # # Optional positional argument
    # parser.add_argument('opt_pos_arg', type=int, nargs='?',
    #                     help='An optional integer positional argument')
    # Optional argument
    parser.add_argument('--input', type=str,
                        help='Filename of input file')
                        
    parser.add_argument('--out', type=str,
                        help='Filename of output file')
                        
    parser.add_argument('--amount', type=str,
                        help='Amount of smr/tokens')
    # # Switch
    # parser.add_argument('--switch', action='store_true',
    #                     help='A boolean switch')

    args = parser.parse_args()

    print("Using tool: " + args.tool)


    ## Load the .env variables

    load_dotenv()
    # Get the stronghold password
    STRONGHOLD_PASSWORD = os.getenv('STRONGHOLD_PASSWORD')
    TOKEN_ID = os.getenv('TOKEN_ID')

    ## Setup wallet

    wallet_options = {
        'nodes': ['https://api.shimmer.network'],
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
            with open(in_file, encoding='utf8') as f:
                if in_file.endswith(".json"):
                    data = json.load(f)
                    addresses = find_addresses_from_dict(data)
                    addresses = remove_duplicates(addresses)
            
            if len(addresses) > 0:
                print("Found "+str(len(addresses))+" addresses")
                if out_file == None:
                    print("no output file specied: using default 'addresses.txt'")
                    out_file = "addresses.txt"
                with open(out_file, mode="w", encoding="utf8") as f:
                    for line in addresses:
                        f.write(line+"\n")
            else:
                print("No addresses found in file!")

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
        
        case "wallet-status":
            account = wallet.get_account('Airdrop')
            
            response = account.sync_account()
            print(f'Synced: {response}\n')

            balance = account.get_balance()
            print(f'Balance: {balance}\n')
            
            wallet_addr = account.addresses()
            print(f'Address: {wallet_addr}\n')

            output_ids = account.get_outputs_with_additional_unlock_conditions('All')
            print(f'Available outputs to claim: {output_ids}')

        case "wallet-claim-all":
            account = wallet.get_account('Airdrop')
            
            response = account.sync_account()
            
            output_ids = account.get_outputs_with_additional_unlock_conditions('All')
            print(f'Available outputs to claim: {output_ids}')
            transaction_result = account.claim_outputs(output_ids)
            print(f'Sent transaction: {transaction_result}')

        case "wallet-airdrop":
            send_smr = False
            in_file = args.input
            amount = args.amount
            if amount.startswith("SMR"):
                send_smr = True
                amount = amount[3:]
            addresses = []
            failed_addresses = []
            success_addresses = []
            other_addresses = []

            if in_file == None:
                print("no input file specied: trying default 'addresses.txt'")
                in_file = "addresses.txt"

            with open(in_file, encoding='utf8') as f:
                if in_file.endswith(".txt"):
                    addresses = f.readlines()
            
            print(f'Found {len(addresses)} addresses from {in_file}')

            account = wallet.get_account('Airdrop')
            
            transaction_result = None

            count = 1
            total = len(addresses)

            for addr in addresses:
                addr = addr.strip()

                #refresh account
                response = account.sync_account()

                if send_smr:
                    print(f'\n[{count}/{total}] Sending {amount} glow (SMR) to {addr}')
                    outputs = [{
                        "address": addr,
                        "amount": amount
                    }]
                    transaction_result = account.send_amount(outputs)
                else:
                    print(f'\n[{count}/{total}] Sending {amount} TOKENS to {addr}')
                    outputs = [{
                        "address": addr,
                        "nativeTokens": [(
                                TOKEN_ID,
                                hex(int(amount))
                        )],
                    }]
                    transaction_result = account.send_native_tokens(outputs)

                if 'error' in transaction_result:
                    print(f'ERROR: {transaction_result}')
                    failed_addresses.append(addr)
                elif 'payload' in transaction_result:
                    print(f'SENT transaction: {transaction_result["transactionId"]}')
                    success_addresses.append(addr)
                else:
                    print(f'OTHER: {transaction_result}')
                    other_addresses.append(addr)
                count += 1
                time.sleep(3)
            
            if len(failed_addresses)>0:
                with open("adw-failed.txt", mode="w", encoding="utf8") as f:
                    for line in failed_addresses:
                        f.write(line+'\n')
            if len(success_addresses)>0:
                with open("adw-success.txt", mode="w", encoding="utf8") as f:
                    for line in success_addresses:
                        f.write(line+'\n')
            if len(other_addresses)>0:
                with open("adw-other.txt", mode="w", encoding="utf8") as f:
                    for line in other_addresses:
                        f.write(line+'\n')

        case _:
            print(args.tool + " is not a tool")

def find_addresses_from_dict(data):
    #print("looking thru data...")
    found = []
    for k, v in data.items():
        #print(v)
        #if v is dict:
        if hasattr(v, "items"):
            subfound = find_addresses_from_dict(v)
            found += subfound
        if k == "text" and isinstance(v, str):
             #print(v)
             words = v.split()
             for w in words:
                if w.startswith("smr1"):
                    #print(w)
                    found.append(w)
    return found

def remove_duplicates(seq):
  singles = set(seq)
  print("Removed "+ str(len(seq)-len(singles)) + "duplicates")
  return list(singles)

if __name__ == "__main__":
    main()