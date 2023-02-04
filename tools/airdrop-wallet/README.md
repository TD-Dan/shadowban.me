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

After the file is processed or if process is interrupted two files will be written: results-success.txt and results-fail.txt. These files contain smr addresses of successfull and failed sends

#### Examples:

<code>python airdrop-wallet.py wallet-airdrop --input my_address_list.txt --amount 123000 </code>
Sends 123000 Tokens to each smr address in the .txt file.
File needs to be one smr address per line.
Token id needs to be specified in .env file.

<code>python airdrop-wallet.py wallet-airdrop --input --amount SMR1234000 </code>

Sends 1.234 SMR (1234000glow) to each smr address in the default addresses.txt file.
File needs to be one smr address per line.
Token id needs to be specified in .env file.



### addresses-get
<code>python airdrop-wallet.py addresses-get [--input comments.json] [--output addresses.txt]</code>

Reads in twitter comments from .json file and outputs an .txt file with each found unique smr address per line



## Tips

- if the process takes too long or keeps giving errors you can use ctrl-c to stop
- 'no inputs found'/'the wallet account does not have enough native tokens' errors can be fixed by feeding the airdrop wallet with funds (both SMR and Tokens) in many smaller batches
- use <code>python airdrop-wallet.py wallet-airdrop --input result-failed.txt --amount 123000 </code> to rerun failed sends
