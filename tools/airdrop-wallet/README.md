# airdrop-wallet
tool to airdrop huge amounts of shimmies/tokens to multiple addresses

## usage
edit the .env file to set your wallet (stronghold) password, token id and other settings



### wallet-create

<code>python airdrop-wallet.py wallet-create</code>

Create airdrop wallet

will write a wallet.stronghold file and _airdrop_database folder. Prints out your mnemonic words: WRITE THEM DOWN and BE AWARE: If you delete these your created wallet is forever lost



### wallet-status

<code>python airdrop-wallet.py wallet-status</code>

Gives info on wallet balance, receive address and unclaimed tokens



### wallet-claim-all

<code>python airdrop-wallet.py wallet-claim-all</code>

Claims **all** unclaimed tokens that have been sent to this airdrop wallet




### wallet-airdrop

<code>python airdrop-wallet.py wallet-airdrop  --amount 123000 [--input my_smr_list.txt]</code>

Sends out **amount** to **input** address list

#### Examples:

<code>python airdrop-wallet.py wallet-airdrop --input my_address_list.txt --amount 123000 </code>
Sends 123000 Tokens to each smr address in the .txt file.
File needs to be one smr address per line.
Token id needs to be specified in .env file.

<code>python airdrop-wallet.py wallet-airdrop --input --amount SMR1234000 </code>

Sends 1.234000 SMR (1234000glow) to each smr address in the default addresses.txt file.
File needs to be one smr address per line.
Token id needs to be specified in .env file.



### addresses-get
<code>python airdrop-wallet.py addresses-get [--input comments.json] [--output addresses.txt]</code>

Reads in twitter comments from .json file and outputs an .txt file with each found unique smr address per line
