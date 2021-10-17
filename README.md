# Amazon Price Alert Bot

### Description
A Telegram chatbot that helps you set price alerts for amazon products. The bot checks the price of your watchlisted products every hour and sends you an alert message when it reaches the target price. It is developed using the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and deployed on Replit.<br> 

[Link to the Telegram Bot](https://telegram.me/PriceA1ertBot)

![skdms](https://github.com/rittikbasu/pricealert-telegrambot/blob/941963a2147f73482bb31c149b59684198f5032b/images/Screenshot%20from%202021-10-17%2020-01-55.png)


### Requirements
* pyTelegramBotAPI

    ```
       pip install pyTelegramBotAPI
    ```
* Google Sheets API

    ```
      pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
  [Refer this page on how to get the api key for Google Sheets](https://developers.google.com/sheets/api/guides/authorizing)
* gspread

    ```
       pip install gspread
    ```
### How it works?
* You send an Amazon URL to the bot
* It checks whether it is a valid Amazon product URL.
* Then it asks you for a price alert.
* Finally using the Google Sheets API it adds the details of your product to an excel sheet.
* It checks every hour if the product has reached the alert price.
* Once it reaches the alert price the bot sends you an alert message.

### Links to Replit
* [Telegram Bot](https://replit.com/@RittikBasu/amazonPriceAlertp1)
* [Amazon Scraper](https://replit.com/@RittikBasu/amazonPriceAlertp2)
