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

    if humanReadable > 0.000105: # min BNB tax - 5 GWEI

        gas = 21000 # gasLimit
        gwei = 5 # gasPrice in gwei
        wei = gwei * k # calculated gasPrice in wei
        
        if gwei < 5:
            print("gasPrice cant be less than 5 GWEI")
            sys.exit()

        calcAmount = balance - (wei*gas) # calculated amount with network tax
        tax = (balance-calcAmount)/eth # tax

        if amount == balance:
            gwei = 5
            wei = gwei * k
            global amount
            amount = balance - (wei*gas)
        elif amount > calcAmount:
            print("Not enough funds. Too much gas price: " + str(tax))
            print("Maximum allowed amount is " + str(calcAmount/eth))
            sys.exit()

        nonce = web3.eth.getTransactionCount(account_1)

        tx = {
        'nonce': nonce,
        'to': account_2,
        'value': int(amount),
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
        print("The balance is less than the minimum network tax 0.000105 BNB")

if __name__ == '__main__':
    try:
        myfunc()
    except Exception as e:
        print(e)




