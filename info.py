
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
    symbol = columns[0].text.strip().replace(".", "-")
    industry = columns[2].text.strip()
    constituents.append(symbol)
    industry_list.append(industry)

info = []
for y in constituents:
    #create Ticker object to access its methods and attributes
    ticker = yf.Ticker(y)
    # Get the stock's info
    stock_info = ticker.info
    #Get specific info
    market_cap = stock_info.get('marketCap')
    eps = stock_info.get('trailingEps')
    revenue = stock_info.get('totalRevenue')
    pe_ratio = stock_info.get('trailingPE')
    forward_pe=stock_info.get('forwardPE')
    Summary = stock_info.get('longBusinessSummary')
    fiftytwolow = stock_info.get('fiftyTwoWeekLow')
    fiftytwohigh = stock_info.get('fiftyTwoWeekHigh')
    bookvalue = stock_info.get('bookValue')
    de_ratio = stock_info.get('debtToEquity')
    quick_ratio= stock_info.get('quickratio')
    current_ratio= stock_info.get('currentratio')
    total_debt= stock_info.get('totalDebt')
    total_cash=stock_info.get('totalCash')
    cps=stock_info.get('totalCashPerShare')
    long_name=stock_info.get('longName')
    volume = stock_info.get('volume')
    shares=stock_info.get('sharesOutstanding')
    float=stock_info.get('floatShares')
    industry=stock_info.get('industry')
    sector=stock_info.get('sector')
    website=stock_info.get('website')
    dividend_rate=stock_info.get('dividend_rate')
    dividend_yield=stock_info.get('dividend_yield')
    price = yf.download(y, period="1d").iloc[-1]["Close"]
    #create empty temporary list to append to empty 'info' list for pd dataframe
    temp_list = [y,market_cap,shares,float,industry,sector,website,revenue,eps,cps,total_debt,total_cash,bookvalue,dividend_rate,dividend_yield,
            pe_ratio,forward_pe,de_ratio,quick_ratio,current_ratio,price,volume,fiftytwolow,fiftytwohigh,long_name]
    info.append(temp_list)




#Printing Info (Not Necessary)
    # Print basic information
    print("Basic Information")
    print("Ticker:",y)
    print("Business Summary:", Summary)
    print("Market Cap:", market_cap)
    print('Shares Outstanding', shares)
    print('Shares Float',float)
    print('Industry',industry)
    print('Sector',sector)
    print('website',website)
    print("\n") 
    #print financials
    print("FINANCIALS")
    print("Revenue:", revenue)
    print("Earnings Per Share:", eps)
    print('Cash Per Share',cps)
    print("Total Debt:",total_debt)
    print('Total Cash',total_cash)
    print("Book Value:", bookvalue)
    print("Dividend Rate", dividend_rate)
    print("Dividend Yield", dividend_yield)
    print("\n") 
    #print ratios
    print("FINANCIALS RATIOS")
    print("PE Ratio:", pe_ratio)
    print("Forward PE Ratio:", forward_pe)
    print("Debt to Equity:",de_ratio )
    print("Quick Ratio:",quick_ratio)
    print("Current Ratio:",current_ratio)
    print("\n") 
    #print price and volume
    print("PRICE & VOLUME")
    print("Price:", price)
    print('Volume',volume)
    print("52 Week Low:", fiftytwolow)
    print("52 Week High:", fiftytwohigh)


    df=pd.DataFrame(info,columns= ['Ticker','Market Cap','Shares Outstanding','Float','Industry','Sector','Website','Revenue','EPS','CPS','Total Debt','Total Cash','Book Value','Dividend Rate','Dividend Yield','PE Ratio','Forward PE Ratio',
                                'Debt to Equity','Quick Ratio','Current Ratio','Price','Volume','52 Week Low','52 Week High','Long Name'])
    df.to_csv('info.csv', index=False)