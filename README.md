# TrackrBot ``` v2.0 ```
<a href="https://www.buymeacoffee.com/rittik" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
### Description
A Telegram chatbot that helps you set price alerts for amazon products. The bot checks the price of your watchlisted products every day and sends you an alert message when it reaches the target price. After adding a product to the watchlist you recieve a product price chart every 30 days until the product reaches its target price. It is deployed on Replit and developed using the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI), [ScraperAPI]() and [Google Sheets API]().<br> 

[Telegram link for TrackrBot](https://telegram.me/PriceA1ertBot)

### Demo
![Demo](https://ik.imagekit.io/zwcfsadeijm/ezgif.com-gif-maker__1__NlR250szt.webp?ik-sdk-version=javascript-1.4.3&updatedAt=1642803781317)

### Price Chart
<img src="https://ik.imagekit.io/zwcfsadeijm/pricechart_NqWajh4Mm.png?ik-sdk-version=javascript-1.4.3&updatedAt=1642799747998" alt="Price Chart" width="800">
<!-- ![Demo](https://ik.imagekit.io/zwcfsadeijm/pricechart_NqWajh4Mm.png?ik-sdk-version=javascript-1.4.3&updatedAt=1642799747998) -->

### How to Support?
To bypass amazon's bot detection I'm using ScraperAPI. The free tier only lets me make a 1000 requests a month therefore I can only let users add upto 3 products to their watchlist. If you like this project consider making a donation at [Buy Me a Coffee](https://www.buymeacoffee.com/rittik) so I can buy the paid plan which costs $29.

Features I plan to add once I'm able to switch to the paid plan:
* Increasing the watchlist capacity from 3 to 30 products.
* Increasing the number of times the bot checks amazon for change in price of a product from 1 to 24 times a day.
* Making the price chart feature more customisable.

### APIs
* Telegram Bot API

  [Refer this page on how to get the api key for Telegram Bots](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
  
* Google Sheets API

    ```
      pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
  [Refer this page on how to get the api key for Google Sheets](https://developers.google.com/sheets/api/guides/authorizing)
  
* pyTelegramBotAPI

    ```
       pip install pyTelegramBotAPI
    ```

### How it works?
#### Telegram Bot
    * User sends a URL to the bot.
    * Bot validates the URL and then sends it to ScraperAPI.
    * ScraperAPI returns a response object which is then parsed using BeautifulSoup.
    * Bot displays the product name and price then asks the user for a price alert.
    * On success the details are added to the Replit Database which is a simple key value store.
    * The amazon scraper checks every hour if the product has reached the alert price.
    * Once it reaches the alert price the bot sends you an alert message.
    
#### Price Tracker
    * User sends a URL to the bot.
    * Bot validates the URL and then sends it to ScraperAPI.
    * ScraperAPI returns a response object which is then parsed using BeautifulSoup.
    * Bot displays the product name and price then asks the user for a price alert.
    * On success the details are added to the Replit Database which is a simple key value store.
    * The amazon scraper checks every hour if the product has reached the alert price.
    * Once it reaches the alert price the bot sends you an alert message.

### Links to Replit
* [Telegram Bot](https://replit.com/@RittikBasu/amazonPriceAlertp1)
* [Amazon Scraper](https://replit.com/@RittikBasu/amazonPriceAlertp2)
