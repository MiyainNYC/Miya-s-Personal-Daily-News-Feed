##finantial times fund management and capital markets

import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import os
os.chdir(YOUR_HOME_DIR)
home_dir = YOUR_HOME_DIR

pd.set_option('display.max_colwidth', -1)

## Fund Management
url = 'https://www.ft.com/fund-management?page=1'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

labels = [i.parent()[0].text for i in soup.findAll('div',{"class":"o-teaser__heading"})]
news_titles = [i.parent()[2].text for i in soup.findAll('div',{"class":"o-teaser__heading"})]
briefs = [i.parent()[-1].text for i in soup.findAll('div',{"class":"o-teaser__heading"})]
urls = ["https://www.ft.com"+i.findNext()['href'] for i in soup.findAll('div',{"class":"o-teaser__heading"})]

labels_list = []
news_titles_list = []
briefs_list = []
urls_list = []

for i, j, z,u in zip(labels,news_titles,briefs,urls):
    if z == 'Save':
        continue
    labels_list.append(i)
    news_titles_list.append(j)
    briefs_list.append(z)
    urls_list.append(u)
df_fund = pd.DataFrame({'Fund Management':labels_list,
             'Title':news_titles_list,
             'Brief':briefs_list,
             'Link':urls_list})[['Fund Management','Title','Brief','Link']].set_index('Fund Management')

html = df_fund.to_html()
with open("ft1.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
    
html1  = open('ft1.html').read()


## capital markets

url = 'https://www.ft.com/capital-markets'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

dates = [i for i in soup.findAll('time')]

labels = []
titles = []
briefs = []
urls = []
dates_list = []
for date in dates:
    #print(date)
    contents = [i.text for i in date.parent.findNext().findNext().findAll('a')]
    if contents == []:
        continue
    #print(contents)
    labels.append(contents[0])
    titles.append(contents[1])
    briefs.append(contents[2])
    urls.append(
        ['https://www.ft.com'+i['href'] for i in date.parent.findNext(
        ).findNext().findAll('a') if 'content/' in i['href']][0]
    )
    dates_list.append(date.text)
df_capital = pd.DataFrame({'Capital Markets':labels,
              'Date':dates_list,
             'Title':titles,
             'Brief':briefs,
             'Link':urls})[['Capital Markets','Date','Title','Brief','Link']].set_index('Capital Markets')

html = df_capital.to_html()
with open("ft2.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
    
html2  = open('ft2.html').read()



##ipo news

url = "https://seekingalpha.com/market-news/ipos"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
s = requests.Session()
r = s.get(url,headers={'User-Agent':user_agent})
page = r.content
soup = BeautifulSoup(page,'html.parser')
today = soup.findAll('li', {"class":"date-title item-date-today"})[0]
RUN = 0
list_title = []
list_desc = []
list_url = []

while RUN<2:

    #if today['class'] == ['mc', 'marketnews-piano-placeholder']:
      
    today = today.nextSibling
    
    if today['class'] == ['date-title']:#.findAll('li',{"class":"date-title"}) == []:
        RUN+=1
    
    try:
        symbol = today.find('a').text
    except:
        today = today.nextSibling
    #print(symbol)
    list_title.append(symbol)
    desc = today.text
    #print(desc)
    list_desc.append(desc)
    try:
        url = [i['href'] for i in today.findAll('a') if 'https://seekingalpha.com/news/' in i['href']][0]
    except:
        url = today.findAll('a')[1]['href']
    list_url.append(url)
df = pd.DataFrame({'title':list_title,
              'desc':list_desc,
              'url':list_url})[['title','desc','url']].set_index('title')


html = df.to_html()
with open("ipo_news.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
    
html3  = open('ipo_news.html').read()



## send the email

sender_email = 'mwang@deepmacro.com' 
receiver_email = "wsjformiya@gmail.com"
password = 'Shirley2027'#input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "FT Capital Markets+Fund Management"
message["From"] = sender_email
message["To"] = receiver_email

html = os.linesep.join([html1,html2, html3])
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
    



