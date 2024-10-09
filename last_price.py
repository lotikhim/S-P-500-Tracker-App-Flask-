import requests
import yfinance as yf
from bs4 import BeautifulSoup
import pandas as pd
import pytz
from datetime import datetime, timedelta

# Set the time zone to US Eastern Time (ET)
us_eastern = pytz.timezone('US/Eastern')

# Get the current datetime in US Eastern Time
current_datetime = datetime.now(us_eastern)

# Send a GET request to the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the components
table = soup.find("table", class_="wikitable sortable")

# Find all the rows in the table (excluding the header row)
rows = table.find_all("tr")[1:51]
# Constituents of DJI
constituents=[]
industry_list=[]

# Extract the company symbol from each row
for row in rows:
    columns = row.find_all("td")
    symbol = columns[0].text.strip().replace(".", "-") #replaces (".") with ("-") 
    industry = columns[2].text.strip()
    constituents.append(symbol)
    industry_list.append(industry)

print(constituents)



gainers = pd.DataFrame()
losers = pd.DataFrame()
for symbol in constituents:
    data = yf.download(symbol, period="5d")
    latest_data = data.iloc[[-1]]  # Most recent trading day
    latest_close = float(latest_data['Close'].iloc[0])
    previous_day_data = data.iloc[[-2]]
    previous_close = float(previous_day_data['Close'].iloc[0])
    percentage_change = ((latest_close) - (previous_close)) / (previous_close) * 100
    percentage_change = round(percentage_change, 2)
    if percentage_change>0:
        data = pd.DataFrame(latest_data)
        data['Ticker'] = symbol
        data['% Change'] = percentage_change
        data = data.drop(['Adj Close'], axis=1)
        gainers = pd.concat([gainers, data])
    elif percentage_change<0:
        data = pd.DataFrame(latest_data)
        data['Ticker'] = symbol
        data['% Change'] = percentage_change
        data = data.drop(['Adj Close'], axis=1)
        losers = pd.concat([losers, data])
    else:
        continue


gainers = gainers.sort_values(gainers.columns[6], ascending=False)
losers = losers.sort_values(losers.columns[6])

gainers.to_csv('gainers.csv', index=False)
losers.to_csv('losers.csv', index=False)