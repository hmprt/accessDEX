from web3 import Web3
import json
import sys

#setting up environment: immporting credentials from file
fo = open("credentials.txt", "r")
infura_url = fo.readline().rstrip('\n')
public_key = fo.readline().rstrip('\n')
private_key = fo.readline().rstrip('\n')

#Setting up a web3 object
w3 = Web3(Web3.HTTPProvider(infura_url))

#Check that the connection has been made
if (w3.isConnected() == False):
    print("No web3 connection!")
    sys.exit(0)

#Basic user dashboard with connection details, block number and current Ether balance
print("\n************************************")
print("Connected to Web3 via {}".format(infura_url))
print("Current block is {}".format(w3.eth.blockNumber))
balance = w3.eth.getBalance(public_key)
print("Current ETH balance:" + str(w3.fromWei(balance, 'ether')))
print("************************************")

#Checking ETH vs DAI on Uniswap V2

# Importing JSON Array of ERC-20 tokens
try:
    erc20_file = open("tokens.json")
    database = json.load(erc20_file)
    print("Loaded database successufully!")
except:
    print("Database error. Inspect database")
    sys.exit(0)

#importing currencies (will do this algorithmically eventually)

try:
    DAI = database["tokens"]["DAI"]
    USDT = database["tokens"]["USDT"]
    print("Loaded tokens successfully!")
except:
    print("Database error. Inspect database")
    sys.exit(0)

# Contacting UniswapV2
uniswapData = database["exchanges"]["UniswapV2"]
UniswapV2 = w3.eth.contract(address=uniswapData["address"],
                            abi=uniswapData["ABI"])

#I'm eventually going to just store the checksum addresses
DAItoUSDTAdress = UniswapV2.functions.getPair(w3.toChecksumAddress(DAI['address']),
                                  w3.toChecksumAddress(USDT['address'])).call()
