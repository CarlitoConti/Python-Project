#import libraries used in the script
import requests
import json
import time
import discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from pybit.unified_trading import HTTP

#create a session to Bybit Exchange, manually create api keys 
session = HTTP(
    testnet=False,
    api_key="insert your api key",
    api_secret="insert your api secret",
)

#create a discord channel and setup a discord webhook, retrieve the link and past it here

discordurl = "insert your discord webhook" 

webhook = DiscordWebhook(url=discordurl)

#url to fetch new tickers
api_url = 'https://api.bybit.com/derivatives/v3/public/tickers'

#function to make request to Bybit's API
def fetch_data():
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None

#define previous data as a set
previous_data = set()                

#make request every half a second to the API and compare the retrieved data with the data of the previous request
#If there's no change then keep running into the while otherwise send a buy order of the new ticker to the exchange
while True:
    
    data = fetch_data()
    
    if data and "result" in data and "list" in data["result"]:
        
        #add every ticker to the current data set
        current_data = {item["symbol"] for item in data["result"]["list"]}  
        
        #spot if there's a new ticker
        new_tickers = current_data - previous_data      

        if new_tickers:
            
            #this first if is for the first time the script is ran
            if len(new_tickers) >= 2: 
              
                print("List has been loaded") 

            else: 
                print(f"New tickers detected: {', '.join(new_tickers)}")
                
                #send a webhook to let us know a new ticker has been detected
                embed = DiscordEmbed(title="New Ticker {} detected! ".format("".join(new_tickers)), description="https://www.bybit.com/trade/usdt/{}".format(",".join(new_tickers)), color="03b2f8")
                webhook.add_embed(embed) 
                response = webhook.execute()
                
                we = ','.join(new_tickers)
                
                #fetch last price of the token to determine quantity based on amount we want to buy
                last_price = [symbol['lastPrice'] for symbol in data['result']['list'] if symbol['symbol'] == we][0]  
                quantity = 200 / float(last_price)

                #try to place an order and send a webhook of confirmation otherwise return an error
                try: 
                    order = session.place_order(
                        category='linear',
                        symbol=','.join(new_tickers),
                        orderType='Market',
                        side='Buy',
                        qty= round(quantity)
                    )

                    weborder = DiscordWebhook(url=discordurl, content="Successfully Placed Order!")
                    response = weborder.execute()

                except:     

                    weberror = DiscordWebhook(url=discordurl, content="Error! Go to Console for details")
                    response = weberror.execute()

        else:

            print("No new tickers")

        previous_data = current_data   
    
    time.sleep(0.5)