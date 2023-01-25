#import all necessary libs
import time 
import config
import ccxt

#bot connection
phemex = ccxt.phemex({
    'enableRateLimit': True,
    'apiKey': config.key,
    'secret': config.secret,
})


#body of code
class Trade():
    def __init__(self, symbol, amount, currency):
        self.symbol=symbol #traded pair, for example "BTC/USDC"
        self.amount=amount #the amount of cryptocurrency that you are willing to buy on the buy side or sell on the sell side. For example for "BTC/USDC" this would be the amount of BTC
        self.currency=currency#cryptocurrency tag required for transaction free

        try:
            while True:
                book = phemex.fetch_order_book(symbol)
                bid = book['bids'][0][0]
                ask = book['asks'][0][0]
                open_orders = phemex.fetch_open_orders(symbol)#extracts active orders created by us
                free = phemex.fetch_balance()["free"][currency]#extracts the balance of the currency we need
                usdc = phemex.fetch_balance()["free"]["USDC"]#extracts USDC balance

                #small algorithm needed to get the smallest cost in USDC 
                #P.S.: Since the algorithm relies on your trade data, you have to make the first orders by hand, otherwise there may be errors:( 
                ticker = phemex.fetch_my_trades(symbol)
                costs = []
                for cost in ticker:
                    if cost["side"] == "buy":
                        cost = cost["cost"]
                        costs.append(cost)
                cost = min(costs)
            
                #algorithm of buying and selling cryptocurrency
                if not open_orders: #If there are no open orders, the script runs       
                    if free >= amount:  #compares the amount of currency from our wallet with the amount of currency we want to offer for sale
                        sell = phemex.create_limit_sell_order(symbol, amount, ask + .0045)  
                    
                    if usdc >= cost:  #compares the amount of USDC from the wallet with the value of currency in USDC 
                        buy = phemex.create_limit_buy_order(symbol, amount, bid -.0005)
                                                           
                        
                time.sleep(5)
                open_orders = phemex.fetch_open_orders(symbol)  
        #notification of possible errors during the operation of the script
        except ccxt.base.error.NetworkError:
            print("[!] соединение прервано [!]") 
        except ccxt.base.error.InsufficientFunds:
            print(f"[!] недостаточно USDC или {currency}, чтобы провести обмен {symbol} [!]")           
    
#examples of traded pairs     
dot_usdc = Trade("DOT/USDC", .4, "DOT")
xrp_usdc = Trade("XRP/USDC", 4, "XRP")
doge_usdc = Trade("DOGE/USDC", 19, "DOGE")
ada_usdc = Trade("ADA/USDC", 5, "ADA")
matic_usdc = Trade("MATIC/USDC", 2, "MATIC")
trx_usdc = Trade("TRX/USDC", 32, "TRX")