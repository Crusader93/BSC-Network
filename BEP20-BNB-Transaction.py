from web3 import Web3
import json
import time
import requests
import sys

bsc = "https://bsc-dataseed1.binance.org:443"
web3 = Web3(Web3.HTTPProvider(bsc))

# telegram_bot_ID = ""
# telegram_API_key = ""
# telegram_chat_id = ""

# def telegram_botsendtext(msg):
#     send_text = 'https://api.telegram.org/bot' + telegram_bot_ID + ':' + telegram_API_key + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + msg
#     response = requests.get(send_text)
#     return response.json()

if (web3.isConnected()) == False:
    print("NOT CONNECTED!")
    # telegram_botsendtext("NOT CONNECTED!")
else:
    print("CONNECTED")

k = 1000000000
eth = 1000000000000000000

account_1 = "" # from
account_2 = "" # to
private = "" # account_1 key

amount = 0.02 # BNB amount for transaction
amount = int(amount * eth)

def myfunc():
    balance = web3.eth.get_balance(account_1)
    humanReadable = balance/eth # converting
    print("Balance: " + str(humanReadable))

    if humanReadable > 0.00011:

        gas = 21000 # gasLimit
        gwei = 5 # gasPrice in gwei
        wei = gwei * k # calculated gasPrice in wei

        calcAmount = amount - (wei*gas) # calculated amount with network tax

        if amount <= 0.00011:
            print("The amount cannot be less than the network tax!")
            sys.exit()

        if amount >= (humanReadable-0.00011):
            warnAmount = (balance - (wei*gas))/eth
            print("The amount cannot be greater than (balance-network tax)")
            print("Maximum allowed amount is " + str(warnAmount))
            sys.exit()

        nonce = web3.eth.getTransactionCount(account_1)

        tx = {
        'nonce': nonce,
        'to': account_2,
        'value': int(calcAmount),
        'gas': gas,
        'gasPrice': int(wei)
        }
        signed_tx = web3.eth.account.signTransaction(tx,private)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        trans = web3.toHex(tx_hash)
        transaction = web3.eth.get_transaction(trans)
        print(transaction)
        print("DONE")
        # telegram_botsendtext("Balance: " + str(humanReadable))
    else:
        print("The balance is less than the minimum network tax 0.00011")

if __name__ == '__main__':
    try:
        myfunc()
    except Exception as e:
        print(e)




