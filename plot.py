import requests
import yfinance as yf
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
import pytz
from datetime import datetime, timedelta

matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


def plot(data,symbol):
    # Find the maximum and minimum values from the 'Close' column
    max_price = data['Close'].max()
    max_price_index = data['Close'].idxmax() #find index(date) of max value
    min_price = data.loc[max_price_index:].iloc[1:]['Close'].min()

    #if today is at the max (no data after max)
    if pd.isnull(min_price):
        min_price_index = max_price_index # date of max = date of min
        min_price = max_price
    else:
        min_price_index = data.loc[max_price_index:].iloc[1:]['Close'].idxmin() # find index(date) of min value

    # Assign the maximum price to a new column 'max' only for the row with the maximum value
    data.loc[data['Close'] == max_price, 'max'] = max_price
    data.loc[data['Close'] == min_price, 'min'] = min_price
    # Assign the minimum price to a variable or column
    print(max_price)

    fiftypercent=max_price*0.5
    twentyfivepercent=max_price*0.25

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    plt.figure(figsize=(15, 8))
    plt.plot(data['Close'], zorder=0)
    plt.scatter(data.index, data['max'], s=100, label=('High: '+ str(round(max_price,2))), marker='o', facecolor='red', edgecolor='none')
    plt.scatter(data.index, data['min'], s=100, label=('Low from Previous High: '+ str(round(min_price,2))), marker='o', facecolor='green', edgecolor='none')

    # Add a horizontal line at 0.5 of the maximum price
    plt.axhline(y=fiftypercent, color='blue', linestyle='--', label=('50% from High: '+str(round(fiftypercent,2))))
    # Add a horizontal line at 0.75 of the maximum price
    plt.axhline(y=twentyfivepercent, color='green', linestyle='--', label=('75% from High:'+str(round(twentyfivepercent,2))))

    # Connect the two points with a line
    plt.plot([max_price_index, min_price_index], [max_price, min_price], color='black', linestyle='dotted')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.title("{}".format(symbol))
    plt.savefig('static/image/{}.png'.format(symbol))
    plt.close()
    

for symbol in constituents:
    data = yf.download(symbol, period="max")["Close"].astype('object')
    data = pd.DataFrame(data)
    plot(data, symbol.upper())

#get spx chart
symbol = "^spx"
data = yf.download(symbol, period="5y")["Close"].astype('object')
data = pd.DataFrame(data)
plot(data, "S&P 500")
