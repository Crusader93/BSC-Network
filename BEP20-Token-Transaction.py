from web3 import Web3
import json
import sys

bsc = "https://bsc-dataseed1.binance.org:443"
web3 = Web3(Web3.HTTPProvider(bsc))

if (web3.isConnected()) == True:
    print("CONNECTED")
else:
    print("NOT CONNECTED!")    

abi1 = json.loads('') # contract abi
contract_address = "" # contract address

account_1 = "" # from
account_2 = "" # to
private = "" # account_1 key

contract = web3.eth.contract(address=contract_address, abi=abi1)

k = 1000000000
eth = 1000000000000000000

amount = 15 # account_1 token amount for transaction
amount = int(amount * eth) # converting

def myfunc():
    balance = web3.eth.get_balance(account_1)
    balanceOf = contract.functions.balanceOf(account_1).call() # token balance
    balanceOf = balanceOf/eth # converting
    print("Token balance: " + str(balanceOf))

    if balanceOf <= amount/eth:
        print("Error: token balance <= amount tokens")
        sys.exit()

    humanReadable = balance/eth # converting
    print("Balance: " + str(humanReadable))

    if humanReadable > 0.000105: # min BNB tax 5 GWEI
        
        gas = 21000 # gasLimit, set 60000-100000 if the transaction does not work, but then the minimum balance should be 0.0005 BNB. k = 1000000000, eth = 1000000000000000000, balance = 0.0005 * eth, gwei = 5 gas = 100000, wei = gwei * 1000000000, value = balance - (wei*gas), value must be > 0
        gwei = 5 # gasPrice in gwei
        wei = gwei * k # calculated gasPrice in wei
        summ = balance - (wei*gas)

        if summ <= 0:
            allowedGas = balance/wei
            print("Too much gasLimit, you can use no greater than: " + str(allowedGas))
            sys.exit()

        nonce = web3.eth.getTransactionCount(account_1)
        
        tx = contract.functions.transfer(account_2, amount).buildTransaction({
        'chainId': 56,
        'from': account_1,
        'nonce': nonce,
        'gas': gas,
        'gasPrice': int(wei)
        })

        signed_tx = web3.eth.account.signTransaction(tx,private)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        trans = web3.toHex(tx_hash)
        transaction = web3.eth.get_transaction(trans)
        print(transaction)
        print("DONE")
    else:
        print("The balance is less than the minimum network tax 0.000105 BNB")

if __name__ == '__main__':
    try:
        myfunc()
    except Exception as e:
        print(e)








