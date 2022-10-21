from operator import imod
from anyio import current_time
from requests import delete
from kite_trade import *
import pandas as pd
import time
from datetime import datetime
import pyotp


# Getting nifty data before the market opens

user_id = "TZ6658"       # Login Id
password = "Okayokay@5"      # Login password
twofa = pyotp.TOTP("AIF7NLNP6PJAKB3QHZAA5IGAVWZGVHF6").now()         # Login Pin or TOTP

enctoken = get_enctoken(user_id, password, twofa)
kite = KiteApp(enctoken=enctoken)

prv_indices = kite.ltp("NSE:NIFTY 50")


# Cheking if it is time of the opening market hours
while(True):
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if (now.strftime("%H:%M:%S") >= "09:15:00"):
        print("date and time =", dt_string)
        break
    time.sleep(60 * 5)


# logging in
user_id = "TZ6658"       # Login Id
password = "Okayokay@5"      # Login password
twofa = pyotp.TOTP("AIF7NLNP6PJAKB3QHZAA5IGAVWZGVHF6").now()         # Login Pin or TOTP

enctoken = get_enctoken(user_id, password, twofa)
kite = KiteApp(enctoken=enctoken)

# cheking if nifty 50 has gapped down by 1% if so ignore all trades
curr_indices = kite.ltp("NSE:NIFTY 50")

if((prv_indices["NSE:NIFTY 50"]["last_price"] - (prv_indices["NSE:NIFTY 50"]["last_price"]/100)) < curr_indices["NSE:NIFTY 50"]["last_price"]):
    print("Not a good day, sayonnara")

    exit()

# Getting ideal stocks for the day
data = pd.read_excel("EOD.xlsm")

# filtering data
data = data.iloc[1:493, 5:15]

# looking for ideal conditions
filt = (data["Breakout Filter"] == "Breakout") & (data["Unnamed: 7"] == "Green candle") & (data["Unnamed: 8"] == "Good")
stocks_EOD = data[filt]["Unnamed: 5"]
stock_cls = data[filt]["Unnamed: 12"]

# converting to a list
stocks = stocks_EOD.to_list()
cls_price = stock_cls.to_list()
print("previously: ",stocks)

# checking if the stock has alreayd increased by 1% if so remove from the stocks list
remove_list = []
for i,x in enumerate(stocks):
    my_dict = kite.ltp(f"NSE:{x}")
    opening = my_dict[f"NSE:{x}"]["last_price"]
    price_tolarance = (cls_price[i] + (cls_price[i]/100))
    # print("stock: ", x, "price_tolarance: ", price_tolarance, " Opening price: ", opening)
    if opening > (price_tolarance):
        remove_list.append(x)
    if opening < cls_price[i]:
        remove_list.append(x)

for x in remove_list:
    stocks.remove(x)
print(stocks)


# placing the order for the filtered list of stocks
order_tracking = dict()

for i,x in enumerate(stocks):
    quant = int(10000/cls_price[i])
    try:
        order = kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NSE,
                            tradingsymbol=x,
                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                            quantity=quant,
                            product=kite.PRODUCT_MIS,
                            order_type=kite.ORDER_TYPE_MARKET,
                            price=None,
                            validity=None,
                            disclosed_quantity=None,
                            trigger_price=None,
                            squareoff=None,
                            stoploss=None,
                            trailing_stoploss=None,
                            tag="TradeViaPython")
        if(order):
            order_tracking[x] = order
    except(TypeError):
        print("error")

    # my_dict = kite.ltp(f"NSE:{x}")
    # opening = my_dict[f"NSE:{x}"]["last_price"]
    # sl_trigger = opening - ((opening*0.5)/100)
    # try:
    #     order = kite.place_order(variety=kite.VARIETY_REGULAR,
    #                         exchange=kite.EXCHANGE_NSE,
    #                         tradingsymbol=x,
    #                         transaction_type=kite.TRANSACTION_TYPE_SELL,
    #                         quantity=quant,
    #                         product=kite.PRODUCT_MIS,
    #                         order_type=kite.ORDER_TYPE_SLM,
    #                         price=None,
    #                         validity=None,
    #                         disclosed_quantity=None,
    #                         trigger_price=sl_trigger,
    #                         squareoff=None,
    #                         stoploss=None,
    #                         trailing_stoploss=None,
    #                         tag="TradeViaPython")
    #     if(order):
    #         order_tracking[x] = order
    # except(TypeError):
    #     print("error")

print(order_tracking)