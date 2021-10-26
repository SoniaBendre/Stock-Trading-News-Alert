import requests
import datetime as dt
import smtplib

MY_EMAIL = "" #email address
MY_PASSWORD = "" #password

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "XZ5GNH8M8U9IWY2R"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_API = "2470c7041df544a7b31f1e375cad8d48"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API
}
yesterday = dt.datetime.now() - dt.timedelta(1)
yesterday_string = dt.datetime.strftime(yesterday, "%Y-%m-%d")

day_before_yesterday = dt.datetime.now() - dt.timedelta(2)
day_before_yesterday_string = dt.datetime.strftime(day_before_yesterday, "%Y-%m-%d")

stock_response = requests.get(url=STOCK_ENDPOINT,params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

stock_price_yesterday = float(stock_data["Time Series (Daily)"][yesterday_string]["4. close"])
stock_price_day_before_yesterday = float(stock_data["Time Series (Daily)"][day_before_yesterday_string]["4. close"])

difference = float(stock_price_yesterday) - float(stock_price_day_before_yesterday)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(stock_price_yesterday)) * 100)

if abs(diff_percent) > 1:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API
    }
    response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = response.json()
    top_three_articles = news_data["articles"][:3] #list containing first 3 articles

    #Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in top_three_articles]

    body = ""

    for article in formatted_articles:
        body += f"\n\n{article}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:{STOCK} Stock Price Change!\n\n {body}")
