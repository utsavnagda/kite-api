from numpy import indices
from kite_trade import *
import pyotp

# user_id = "TZ6658"       # Login Id
# password = "Okayokay@5"      # Login password
# twofa = pyotp.TOTP("AIF7NLNP6PJAKB3QHZAA5IGAVWZGVHF6").now()         # Login Pin or TOTP

enctoken = "l/4+R4Op/KyBGStyuVFmPCs6CzrY1UtdWlUVdGz7CGLHDPmJwQFwy+hUwTzy14qsvmgZBMb2MASu3Yfskr5QxK6qgH5Lx0T2vFQgUhJoNXXDM6mcHphYJQ=="
kite = KiteApp(enctoken=enctoken)

# before
indices = kite.ltp("NSE:NIFTY 50")

# after
curr_indces = kite.ltp("NSE:NIFTY 50")
print(indices)
print("previous day close: ", indices["NSE:NIFTY 50"]["last_price"])
print("one percent subtracted: ", indices["NSE:NIFTY 50"]["last_price"] - (indices["NSE:NIFTY 50"]["last_price"]/100))
print("current price: ", curr_indces["NSE:NIFTY 50"]["last_price"])

print((indices["NSE:NIFTY 50"]["last_price"] - (indices["NSE:NIFTY 50"]["last_price"]/100)) < curr_indces["NSE:NIFTY 50"]["last_price"])
