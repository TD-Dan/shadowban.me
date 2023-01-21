
default_airdrop = {
    "token_name"
    "airdrop_delay_seconds":5.0,
    "claim_expiration_seconds":604800
}

class AirdropTool:
    short = 'a'
    long = 'airdrop'
    help = 'Deliver an airdrop.'
    help_long = 'Prepare and send out an airdrop to multiple recipients.\n'+\
                'Airdrops are managed by stages: staging, drop active, follow.\n'+\
                'If "simulate" is enabled will only do a test airdrop run without sending any actual coins or tokens.'
    def __call__(self,*args):
        #Report on previously created airdrops
        print("\tAirdrop name\tstatus")
        print("\t-\t-")