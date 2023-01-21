
default_configuration = {
    "nodes":{ "Shimmer":"https://api.shimmer.network",
              "Shimmer testnet":"https://api.testnet.shimmer.network"
    },
    "network":"Shimmer",
    "airdrop_delay_seconds":5.0,
    "claim_expiration_seconds":604800
}

class ConfigTool:
    def __call__(self):
        print("Hello, I am a config.")
    
    def help(self) -> str:
        return "Manage program configuration."