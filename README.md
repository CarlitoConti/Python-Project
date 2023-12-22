# Documentation Python Code - Crypto Trading Strategy

## Introduction
This code sets up a continuous loop to check for new tickers from Bybit's API, and if it detects new tickers,it sends a notification to a user’s Discord channel using a webhook. Additionally, it places a buy order for the new ticker(s) on the Bybit Exchange.

##  Requirements

To run the provided code successfully, you need to fulfill several requirements, including installing specific Python libraries, creating a Bybit account, and generating API keys. Below are the detailed requirements.

1.	Install the required libraries and import them in your environment using the following commands:
```py
```
```py
import requests
import json
import time
import discord_webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from pybit.unified_trading import HTTP
```

2.	Create a Bybit account by visiting the [Bybit](https://www.bybit.com/en/sign-up) website. Log in or sign up for an 
account. Be sure that your account is set as an Unified Trading Account, otherwise the script won’t work, and that your preferences are like this, which should be by default.
![image](https://github.com/CarlitoConti/Python-Project/assets/154532693/45e22d95-eccd-43b8-9d8e-365a5e30d490)

 
3.	After logging in to your Bybit account, navigate to the API Management section. Create a new System-Generated API key with the necessary permissions (e.g., trading permissions).
![image](https://github.com/CarlitoConti/Python-Project/assets/154532693/ad0a9a6d-dc8f-4306-b5c9-647701fd41b6)

Replace "insert your api key" and "insert your api secret" with the API key and secret you obtained from Bybit.

```py
#create a session to Bybit Exchange, manually create api keys 
session = HTTP(
    testnet=False,
    api_key="4DSbiiGMmtbvtQS08N",
    api_secret="bJuPOE1dQ8z4WCmyKYNYuxs0RjzeNCgJp8vS",
)
```

3. Create a Discord channel where you want to receive notifications. Set up a Discord webhook for the channel. You can follow Discord's official guide on how to create a webhook. 
 
```py
#create a discord channel and setup a discord webhook, retrieve the link and past it here

discordurl = "https://discord.com/api/webhooks/1162735444795084920/72JbBo2thRXjbF6yDhYKE6ARcrzhusjEUdtkoYOp0WLRumJum3WBY3U1NOwzhMSn-Wsj" 

webhook = DiscordWebhook(url=discordurl)
```
Replace "insert your discord webhook" with the actual Discord webhook URL you obtained in the previous step.




## How it works

## A.  Function for getting data

After fulfilling all the requirements, the code fetches the data from the Bybit API. 
Once all prerequisites are met, the code retrieves information from the Bybit API, specifically focusing on newly listed futures tickers. The script exclusively considers the addition of new cryptocurrencies within the derivatives section.
Indeed, when a new cryptocurrency is listed in Bybit, a new ticker is assigned and all crypto’s information is embedded in the above API. Therefore, we use it to get the data.

 
This code defines a function named fetch_data() and initializes a variable previous_data as an empty set.
1.	fetch_data() Function:
a.	The fetch_data() function is responsible for making an HTTP GET request to a specified api_url using the requests library.
b.	Inside a try-except block, it sends a GET request to the provided api_url using requests.get().
c.	If the response status is a success (HTTP status code 200), it retrieves the JSON content of the response using response.json() and returns it.
d.	If an exception of type requests.exceptions.RequestException occurs during the HTTP request (e.g., network issue, timeout, etc.), it catches the exception, prints an error message indicating the issue encountered while fetching data from the API (Error fetching data from the API: {error_message}), and returns None to signify an unsuccessful data retrieval.
2.	previous_data Variable:
a.	previous_data is initialized as an empty set (set()). It's used to store the previously fetched data or tickers.
Overall, this code snippet sets up a function to retrieve data from a specified API URL using the requests library and initializes an empty set to store previously fetched data for later comparison, likely to track changes or new additions in the fetched data over time.

B.  Request of Data
 
1.	while True:: Initiates an infinite loop, ensuring continuous execution of the code block it contains.
2.	data = fetch_data(): Calls the fetch_data() function defined earlier to retrieve data from an API endpoint. This function is expected to return JSON data.
3.	if data and "result" in data and "list" in data["result"]:
a.	Checks if the data variable has content, and if it has the required structure.
b.	Specifically, it ensures that the data dictionary has a key named "result", which in turn has a key named "list". This structure allows the code to access a list of items (presumably ticker symbols) inside the fetched data.
4.	current_data = {item["symbol"] for item in data["result"]["list"]}:
a.	Constructs a set (current_data) containing the symbols of items retrieved from the fetched data's "list" field. Each item in this set represents a ticker symbol.
5.	new_tickers = current_data - previous_data:
a.	Compares the current set of ticker symbols (current_data) with the set of previously fetched ticker symbols (previous_data).
b.	Calculates the difference between the current set and the previous set, storing any new ticker symbols in the new_tickers set.
6.	if new_tickers:
a.	Enters this block if there are new ticker symbols detected (i.e., if the new_tickers set is not empty).
7.	if len(new_tickers) >= 2:
a.	Within the block for detecting new tickers, it checks if the number of new tickers detected is greater than or equal to 2.
b.	If at least two new tickers are detected, it prints "List has been loaded". This could be a marker to signify a specific condition or event based on the number of new tickers.
Overall, this portion of the code continuously fetches data from an API endpoint, checks for the presence of new ticker symbols, and performs different actions based on the number of new tickers detected, with a specific condition set for when two or more new tickers are detected.

C. New tickers detection and placing of the order

 

This part of the code is responsible for executing actions when new ticker symbols are detected, particularly when fewer than two new tickers are found.
1.	else: This block is executed when there are new ticker symbols detected, but the number of new tickers is less than two.
2.	print(f"New tickers detected: {', '.join(new_tickers)}")
a.	It prints a message indicating the newly detected ticker symbols in the console.
3.	Discord Notification:
a.	Constructs a Discord embed message to notify about the new ticker(s) detected.
i.	Sets the title of the embed message to indicate the detection of new ticker(s).
ii.	Provides a description containing a link to Bybit's trade platform for the detected ticker(s).
iii.	Specifies a color for the embed message.
b.	Adds the created embed to the Discord webhook.
c.	Executes the webhook to send the notification to the configured Discord channel.
4.	Price Calculation and Order Placement:
a.	Converts the set of new ticker symbols (new_tickers) into a comma-separated string (we = ','.join(new_tickers)).
b.	Searches for the last price of the new ticker symbol(s) in the fetched data.
c.	Calculates the quantity of the order to place based on a predefined value of 200 divided by the last price of the new ticker(s).

5.	try Block:
a.	Tries to place a market buy order on the Bybit Exchange for the new ticker symbol(s) using the Bybit API (session.place_order()).
b.	The order details include the symbol(s), order type (Market), buy side, and calculated quantity.
6.	except Block:
a.	If there's an exception during the order placement (e.g., API failure, invalid data, etc.), it catches the exception.
b.	Executes a Discord webhook to send an error message notifying about the order placement failure.
This part of the code finalizes the loop and performs necessary actions after processing the fetched data.

D. Finalization

        
This part of the code finalizes the loop and performs necessary actions after processing the fetched data.
1.	else: (Outside the block checking for new tickers)
a.	This block is executed if no new tickers are detected (i.e., the new_tickers set is empty).
2.	print("No new tickers")
a.	Prints a message in the console indicating that no new ticker symbols were detected in the current data.
3.	previous_data = current_data
a.	Updates the previous_data variable with the current set of ticker symbols (current_data). This is done to store the current data for comparison in the next iteration of the loop. It ensures that in the subsequent loop iteration, the comparison is made against the most recent set of ticker symbols fetched from the API.
4.	time.sleep(0.5)
a.	Pauses the script execution for 0.5 seconds before initiating the next iteration of the loop.
b.	This time.sleep() function call creates a half-second delay before re-executing the loop to fetch data again from the API.
c.	The purpose of this delay is to prevent excessive API requests and control the rate of querying the API to avoid hitting any rate limits or overwhelming the server.
The code does not liquidate the positions, therefore it is necessary for the user to do this independently in Bybit. 


Rationale and results

The reasons behind this program lie behind some of our observations.
Additionally, we've observed a distinction between Bybit spot and futures listings. While spot listings are usually pre-announced, futures listings, particularly in recent months, are often revealed just moments after the trading pair goes live. Recognizing this timing difference, we have chosen to focus on monitoring the launch of new trading pairs and capitalizing on the brief bullish phase immediately following the announcement. Within a few minutes of the announcement, we promptly close our position to seize the potential gains.


As you can see in the three charts above, thanks to this code we made more than 450 USD as net profit by investing only 500 USD. This means a total return of 90%.

Secondly, we found and reported a bug on the Bybit system. 

Bla bla



















