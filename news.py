import requests
from bs4 import BeautifulSoup
import pandas as pd
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


print(constituents)

data = []
user_agent = UserAgent()
for y in constituents:
    url= ("https://finviz.com/quote.ashx?t={}&p=d".format(y))


    response = requests.get(url, headers = {'User-Agent':user_agent.random})
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.find_all("tr", class_="cursor-pointer has-label")
    for news in news:
        # Extract date of news
        td_element = news.find("td", attrs={"width": "130", "align": "right"})
        publication_date =  td_element.get_text(strip=True)

        # Extract the text and URL from the <a> element
        a_element = news.find("a", class_="tab-link-news")
        text = a_element.get_text(strip=True)
        url = a_element["href"]
        #print(publication_date)
        #print("Text:", text)
        #print("URL:", url)

        #create empty temporary list to append to empty data list for pd dataframe
        temp_list =[]
        temp_list.append(y)
        temp_list.append(publication_date)
        temp_list.append(text)
        temp_list.append(url)
        data.append(temp_list)
        print(text)
df=pd.DataFrame(data,columns=['Ticker','Date','News','URL'])
print(df)
df.to_csv('news.csv', index=False)
