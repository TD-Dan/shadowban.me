import os
import time
import json
import pprint

from iota_wallet import IotaWallet, StrongholdSecretManager
from iota_client import IotaClient

from colorama import Fore, Back, Style, init, Cursor
init(autoreset=True)

all_tools = {}

def add_tool(fn: callable,short_command:str,long_command:str):
    all_tools[(short_command,long_command)]=fn

from tools.config import ConfigTool
add_tool(ConfigTool(),'c','config')

def main():

    print(Back.WHITE + Fore.BLACK + ' AIRDROP TOOL v.0.1.1 ')

    print('\nType ' + Fore.LIGHTWHITE_EX + 'help' + Fore.RESET +' for available commands.\nUse Ctrl-C anytime to abort current command.\n')

    while True:
        try:
            
            #print(Cursor.UP(1) + '\33[2K\rA-T>', end='') #\33[2K = erase line, \r = return to line beginning
            print('loading..') #\33[2K = erase line, \r = return to line beginning
            print(Cursor.UP(1)+"", end='')
            
            print('\33[2K\r'+Back.LIGHTBLACK_EX+Fore.BLACK+'A-T>'+Fore.RESET+Back.RESET, end='') #\33[2K = erase line, \r = return to line beginning
            try:
                user_input = input()
                print(Cursor.UP(1)+"", end='')
                for short, long in all_tools:
                    if user_input.casefold() == short or user_input.casefold() == long:
                        print('>>> '+long)
                        all_tools[(short,long)]()
            except KeyboardInterrupt:
                exit_command()
        except KeyboardInterrupt:
            pass
        except ProgramExit:
            print(Fore.LIGHTBLACK_EX + 'Normal program exit')
            exit()
        except Exception as e:
            print("Unhandled exception")
            raise
    

class ProgramExit(Exception):
    pass

"""Exits the program."""
def exit_command():
    if prompt_yes_no("Exit?"):
        raise ProgramExit
add_tool(exit_command,'x','exit')

"""Displays available commands."""
def help_command():
    print("Available commands:")
    for (short,long),tool in all_tools.items():
        print('\t'+short+' - '+long+'\t',end='')
        try:
            print(tool.help())
        except AttributeError:
            print("-")
add_tool(help_command,'h','help')

"""Prompts an yes or no input from user."""
def prompt_yes_no(prompt: str) -> bool:
    print(prompt+ "(y/n) > ", end='')
    user_input = input()
    print(Cursor.UP(1), end='')
    match user_input: 
        case 'Y'|'y'|'Yes'|'yes':
            return True
    return False


    # ## Setup client

    # print(Back.GREEN + 'Opening client...', end='')
    
    # try:
    #     client = IotaClient({'nodes': ['https://api.testnet.shimmer.network']})
    #     node_info = client.get_info()
    #     if "type" in node_info:
    #         raise RuntimeError(node_info["type"])

    #     print("\t" + Back.GREEN + 'OK')
    # except Exception as e:
    #     print("\t" + Back.RED + 'FAIL')
    #     raise

    # ## Setup wallet

    # print(Back.GREEN + "Opening wallet...", end='')

    # wallet_options = {
    #     'nodes': ['https://api.shimmer.network'],
    # }

    # # Shimmer coin type
    # coin_type = 4219

    # secret_manager = StrongholdSecretManager("wallet.stronghold", STRONGHOLD_PASSWORD)

    # wallet = IotaWallet('./_airdrop-database', wallet_options, coin_type, secret_manager)

    # print("\t" + Back.GREEN + 'OK')


    # print("Using tool: " + args.tool)

    # match args.tool:
    #     case "addresses-get":
    #         in_file = args.input
    #         out_file = args.out
    #         addresses = []
    #         if in_file == None:
    #             print("no input file specied: trying default 'comments.json'")
    #             in_file = "comments.json"
            
    #         print("reading " + in_file)
    #         with open(in_file, encoding='utf8') as f:
    #             if in_file.endswith(".json"):
    #                 data = json.load(f)
    #                 addresses = find_addresses_from_dict(data)
    #                 addresses = remove_duplicates(addresses)
            
    #         if len(addresses) > 0:
    #             print("Found "+str(len(addresses))+" addresses")
    #             if out_file == None:
    #                 print("no output file specied: using default 'addresses.txt'")
    #                 out_file = "addresses.txt"
    #             with open(out_file, mode="w", encoding="utf8") as f:
    #                 for line in addresses:
    #                     f.write(line+"\n")
    #         else:
    #             print("No addresses found in file!")
    #     case "node-info":
    #         # Get the node info
    #         node_info = client.get_info()
    #         pprint.pprint(f'{node_info}')
            
    #     case "wallet-create":
    #         # mnemonic (seed) should be set only for new storage
    #         # once the storage has been initialized earlier then you should omit this step
    #         # Store the mnemonic in the Stronghold snapshot, this only needs to be done once
    #         seed = wallet.generate_mnemonic()
    #         print(seed)
    #         account = wallet.store_mnemonic(seed)
    #         account = wallet.create_account('Airdrop')
    #         print("Created account:")
    #         print(account)

    #     case "wallet-status":
    #         account = wallet.get_account('Airdrop')
            
    #         response = account.sync_account()
    #         print("Synced:")
    #         pprint.pprint(response)

    #         #balance = account.get_balance()
    #         #print("Balance:")            
    #         #pprint.pprint(balance)
            
    #         wallet_addr = account.addresses()
    #         print("Address:")
    #         pprint.pprint(wallet_addr)

    #         output_ids = account.get_outputs_with_additional_unlock_conditions('All')
    #         print(f'Available outputs to claim: {output_ids}')

    #     case "wallet-claim-all":
    #         account = wallet.get_account('Airdrop')
            
    #         response = account.sync_account()
            
    #         output_ids = account.get_outputs_with_additional_unlock_conditions('All')
    #         print(f'Available outputs to claim: {output_ids}')
    #         transaction_result = account.claim_outputs(output_ids)
    #         print(f'Sent transaction: {transaction_result}')

    #     case "wallet-airdrop":
            
    #         addresses = []
    #         failed_addresses = []
    #         success_addresses = []
    #         other_addresses = []

    #         send_smr = False
    #         in_file = args.input
    #         amount = args.amount

    #         try:

    #             if not amount:
    #                 print("missing argument: --amount (amount of tokens as 123 or SMR123 for glow)")
    #                 return
    #             if amount.startswith("SMR"):
    #                 send_smr = True
    #                 amount = amount[3:]

    #             if in_file == None:
    #                 print("no input file specied: trying default 'addresses.txt'")
    #                 in_file = "addresses.txt"

    #             with open(in_file, encoding='utf8') as f:
    #                 if in_file.endswith(".txt"):
    #                     addresses = [line.rstrip() for line in f]
                
    #             print(f'Found {len(addresses)} addresses from {in_file}')


    #             account = wallet.get_account('Airdrop')
                
    #             transaction_result = None
    #             count = 1
    #             total = len(addresses)


    #             for addr in addresses:
    #                 # sleep some to give time for client to process sync and previous transaction
    #                 time.sleep(DELAY_SECONDS)

    #                 #refresh account
    #                 response = account.sync_account()

    #                 if send_smr:
    #                     print(f'\n[{count}/{total}] Sending {amount} glow (SMR) to {addr}')
    #                     outputs = [{
    #                         "address": addr,
    #                         "amount": amount,
    #                         "expiration": EXPIRATION_SECONDS
    #                     }]
    #                     transaction_result = account.send_amount(outputs)
    #                 else:
    #                     print(f'\n[{count}/{total}] Sending {amount} TOKENS to {addr}')
    #                     outputs = [{
    #                         "address": addr,
    #                         "expiration": EXPIRATION_SECONDS,
    #                         "nativeTokens": [(
    #                                 TOKEN_ID,
    #                                 hex(int(amount))
    #                         )],
    #                     }]
    #                     transaction_result = account.send_native_tokens(outputs)


    #                 if 'payload' in transaction_result:
    #                     print(f'SENT transaction: {transaction_result["transactionId"]}')
    #                     success_addresses.append(addr)
    #                 elif 'error' in transaction_result:
    #                     print(f'ERROR: {transaction_result}')
    #                     failed_addresses.append(addr)
    #                 else:
    #                     print(f'OTHER: {transaction_result}')
    #                     other_addresses.append(addr)
                    
    #                 count += 1
            
    #         except FileNotFoundError as e:
    #             print(f'\nInput file not found: {e.strerror} (use --input filename.txt to specify your own file)')
    #         except Exception as e:
    #             print("\n!!! Stopped because of:\n")
    #             pprint.pprint(e)
    #             raise
            
    #         finally:
                
    #             total_failed = [addr for addr in addresses if addr not in success_addresses ]
    #             print(f'\n\nSUCCESS: {len(success_addresses)}, FAIL: {len(failed_addresses)}, FAIL BY NO TRY: {len(total_failed)-len(failed_addresses)}, OTHER: {len(other_addresses)}\n')
    #             if len(success_addresses)>0:
    #                 with open("result-success.txt", mode="w", encoding="utf8") as f:
    #                     for line in success_addresses:
    #                         f.write(line+'\n')
    #             if len(total_failed)>0:
    #                 with open("result-failed.txt", mode="w", encoding="utf8") as f:
    #                     for line in total_failed:
    #                         f.write(line+'\n')
    #             if len(other_addresses)>0:
    #                 with open("result-other.txt", mode="w", encoding="utf8") as f:
    #                     for line in other_addresses:
    #                         f.write(line+'\n')

    #     case _:
    #         print(args.tool + " is not a tool")


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