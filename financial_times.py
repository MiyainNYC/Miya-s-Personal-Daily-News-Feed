##finantial times fund management and capital markets

import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import os

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
with open("/home/jupyter/juzi/ft1.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
    
html1  = open('/home/jupyter/juzi/ft1.html').read()


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
with open("/home/jupyter/juzi/ft2.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
    
html2  = open('/home/jupyter/juzi/ft2.html').read()


## send the email

sender_email = 'mwang@deepmacro.com' 
receiver_email = "***formiya@gmail.com"
password = '***********'#input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "FT Capital Markets+Fund Management"
message["From"] = sender_email
message["To"] = receiver_email

html = os.linesep.join([html1,html2])
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
    


