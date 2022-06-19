import atexit
import datetime
import tda
import json
import os
import pathlib

API_KEY = os.environ['API_KEY']
TOKEN_PATH = os.environ['TOKEN_PATH']
REDIRECT_URI = 'https://localhost/'
OUT_PATH=os.environ['OUT_PATH'] #the folder where the data is stored.

def make_webdriver():
    # Import selenium here because it's slow to import
    from selenium import webdriver

    driver = webdriver.Chrome()
    atexit.register(lambda: driver.quit())
    return driver

# Create a new client
client = tda.auth.easy_client(
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    make_webdriver)

def get_accounts():
    # Get account info
    r = client.get_accounts(fields=tda.client.base.BaseClient.Account.Fields.POSITIONS)

    # Save current holdings in a csv
    all = json.loads(r.text)
    if not "error" in all:

        now = datetime.datetime.now()
        with open(OUT_PATH+"/tda_current_assets.csv", "w") as f1, \
            open(OUT_PATH+"/tda_historical_networth.csv", "a") as f2, \
            open(OUT_PATH+"/tda_current_networth.csv", "w") as f3   :
            for account in all:
                accountId =  (account["securitiesAccount"]["accountId"])
                networth =  account["securitiesAccount"]["initialBalances"]['liquidationValue']
                str = f"{now}, {accountId}, {networth}\n"
                f2.write(str)
                f3.write(str)

                for position in account["securitiesAccount"]["positions"]:
                    symbol = position["instrument"]['symbol']
                    units = position['settledLongQuantity']
                    marketvalue = position['marketValue']
                    str = f"{now}, {accountId}, {symbol}, {units}, {marketvalue}\n"
                    f1.write(str)
    return all

def update_transactions(accountId):
    # Get the transaction history
    now = datetime.datetime.now()

    sdate = (now.date() - datetime.timedelta(days=1))
    edate = sdate
    pathlib.Path(OUT_PATH+'/tda_lastupdate.txt').touch() #First touch the file, i.e. if the file doesn't exist. We just create it
    with open(OUT_PATH+"/tda_lastupdate.txt", "r") as f:
        str = f.read()
        if (str != ""):
            sdate = datetime.date.fromisoformat(str) + datetime.timedelta(days=1)
    if (sdate > edate):
        print("Skipping getting Tx data for account " + accountId + "as start date " + sdate + "is greater than end date " + edate)
        return
    r = client.get_transactions(accountId, \
                transaction_type=tda.client.base.BaseClient.Transactions.TransactionType.TRADE, \
                    start_date=sdate, end_date=edate)

    # Save the transaction history
    all = json.loads(r.text)
    # print("Account id is " + accountId)
    # print(all)
    if not "error" in all:

        with open(OUT_PATH+"/tda_trades.csv", "a") as f:
            for trade in all:
                #accountId =  (trade["transactionItem"]["accountId"])
                symbol = trade["transactionItem"]['instrument']['symbol']
                units = trade['transactionItem']['amount']
                cost = trade['transactionItem']['cost']
                date = trade['settlementDate']
                desc = trade['description']
                str = f"{accountId}, {date}, {symbol}, {units}, {cost}, {desc}\n"
                f.write(str)

        with open("tda_lastupdate.txt", "w") as f:
            f.write(edate.isoformat())
def get_quotes():
    symbols = ['SPY', 'NVDA', 'GOOGL', 'AAPL', 'NFLX', 'BRK.B', 'XLK', 'TSLA',
                'AMZN', 'AMD', 'META', 'LQD', 'BND', 'JNK']
    r = client.get_quotes(symbols)
    all = json.loads(r.text)
    # print(all)

    if "error" in all:
        print("Bailing as there was an error getting quotes")
        print(all)
        return

    with open(OUT_PATH+"/tda_hilo.csv", "w") as f:
        for symbol in symbols:
            mark = all[symbol]['mark']
            high52 = all[symbol]['52WkHigh']
            low52 = all[symbol]['52WkLow']
            fromhigh  = round((high52 - mark)/high52*100, 2)
            fromlow = round((mark - low52)*100/low52, 2)
            tohigh  = round((high52 - mark)/mark*100, 2)
            tolow = round((mark - low52)*100/mark, 2)
            date = datetime.datetime.now().date()
            str = f"{date}, {symbol}, {mark}, {fromhigh}, {tohigh}, {fromlow}\n"
            f.write(str)

#accounts = get_accounts()

#     for account in accounts:
#             accountId =  (account["securitiesAccount"]["accountId"])
#             update_transactions(accountId)
#

get_quotes()
