
default_configuration = {
    "nodes":{ "Shimmer":"https://api.shimmer.network",
              "Shimmer testnet":"https://api.testnet.shimmer.network"
    },
    "network":"Shimmer",
    "airdrop_delay_seconds":5.0,
    "claim_expiration_seconds":604800
}

class ConfigTool:
    short = 'c'
    long = 'config'
    help = 'Manage program configuration.'
    help_long = 'Manage settings that are used by all tools, like network and wallet preferences.'
    def __call__(self,*args):
        print("Henlo, I am config. I received "+ str(args))