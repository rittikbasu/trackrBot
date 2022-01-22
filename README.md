# TrackrBot ``` v2.0 ```
<a href="https://www.buymeacoffee.com/rittik" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
### Description
A Telegram chatbot that helps you set price alerts for amazon products. The bot checks the price of your watchlisted products every day and sends you an alert message when it reaches the target price. After adding a product to the watchlist you recieve a product price chart every 30 days until the product reaches its target price. It is deployed on Replit and developed using the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI), [ScraperAPI](https://www.scraperapi.com/) and [Google Sheets API](https://developers.google.com/sheets/api).<br> 

[Telegram link for TrackrBot](https://telegram.me/PriceA1ertBot)

### Demo
![Demo](https://ik.imagekit.io/zwcfsadeijm/ezgif.com-gif-maker__1__NlR250szt.webp?ik-sdk-version=javascript-1.4.3&updatedAt=1642803781317)

### Price Chart
![Demo](https://github.com/rittikbasu/trackrBot/blob/d07adcb48965b287a1528bcf971e3728d26fd3da/images/newplot%20(2).png)

<!-- <img src="https://ik.imagekit.io/zwcfsadeijm/newplot__2__INf1gWU4nVp.png?ik-sdk-version=javascript-1.4.3&updatedAt=1642878776534" alt="Price Chart" width="1000">
 -->
### APIs Used:
* <b>Telegram Bot API</b>

  The Bot API is an HTTP-based interface created for developers to build bots for Telegram.
  
  [Refer this page on how to get the api key for Telegram Bots](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
  
* <b>ScraperAPI</b>

  This version of TrackrBot improves over the last one by using ScraperAPI which provides anti-bot detection and IP geolocation which helps scrape amazon without being blocked.
  
  [Refer this page on how to get the api key for ScraperAPI](https://www.scraperapi.com/)
  
* <b>Google Sheets API</b>

  This API is used to record price changes for a product in Google Sheets which is used to create a product price chart every 30 days.

    ```
    $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
  [Refer this page on how to get the api key for Google Sheets](https://developers.google.com/sheets/api/guides/authorizing)
  
* <b>pyTelegramBotAPI</b>

  A simple, but extensible Python implementation for the Telegram Bot API.


    ```
    $ pip install pyTelegramBotAPI
    ```

### How it works?
#### Telegram Bot
    * User sends a URL to the bot.
    * Bot validates the URL and then sends it to ScraperAPI.
    * ScraperAPI returns a response object which is then parsed using BeautifulSoup.
    * Bot displays the product name and price then asks the user for a price alert.
    * On success the details are added to the Replit Database which is a simple key value store.
    
#### Price Tracker
    * Checks if any new products are added to the Replit DB and then adds them to Google Sheets.
    * Checks if any products are deleted from the Replit DB and then deletes them from Google Sheets.
    * Scrapes amazon for every product in the Replit DB and updates the sheet with the current price.
    * If current price <= target price it sends the user a price alert on telegram.
    * If a product column has 30 price values on Google Sheets it sends a price chart to the user. 
    
### How to contribute?
<i>Contributions, issues and feature requests are welcome. For major changes, please open an issue first to discuss what you would like to change.</i>
* Fork this repository on GitHub and clone it on your local machine.

  ```
  $ git clone https://github.com/<your-username>/trackrBot.git
  ```
* <b>Recommended:</b> Fork this project on Replit. This saves you the trouble of setting up the environment and installing the libraries.

#### Links to Replit
* [Telegram Bot](https://replit.com/@RittikBasu/trackr)
* [Price Tracker](https://replit.com/@RittikBasu/subtrackr)

### How to Support?
Currently this project uses the free tier of ScraperAPI which only provides a 1000 requests a month. If you like this project consider making a donation at [Buy Me a Coffee](https://www.buymeacoffee.com/rittik) so I can buy the paid plan which costs $29.

<!-- To bypass amazon's bot detection this project uses ScraperAPI. The free tier only allows upto a 1000 requests a month therefore the users are only allowed to add upto 3 products to their watchlist since the more products they add the more number of requests need to be made.   -->

Features I plan to add once I'm able to switch to the paid plan:
* Increasing the watchlist capacity from 3 to 30 products.
* Increasing the number of times the bot checks amazon for change in price of a product from 1 to 24 times a day.
* Making the price chart feature more customisable.
