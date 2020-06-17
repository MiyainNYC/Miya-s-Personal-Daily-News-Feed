##wsj top news and barron market data schedule

import pandas as pd
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import os

env = dict(os.environ)
output_dir = env['OUTPUT_DIR']

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
login_url = "https://accounts.wsj.com/login?target="
login_data = {'username':'miya******@gmail.com',
              'password':'**********'}
s = requests.Session()
s.post(login_url,data=login_data,headers={'User-Agent':user_agent})


url_list = ["https://www.wsj.com/news/markets",
'https://www.wsj.com/news/business',
'https://www.wsj.com/news/technology',
'https://www.wsj.com/news/economy']

list_df = []
result_dict = {}
for url in url_list:
    topic = url.split('/')[-1]
    r = s.get(url,headers={'User-Agent':user_agent})
    page = r.content
    soup = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame({'wsj_daily':[topic.upper()]+ [i.text for i in soup.findAll(
         'p', {'class':"WSJTheme--summary--lmOXEsbN "})] + [' ']+ [' ']})
    list_df.append(df)

final_df = pd.concat(list_df)#,ignore_index=True)
pd.set_option('display.max_colwidth', -1)
html = final_df.to_html(index=False)#.replace('border="1"','border="0"')
with open(output_dir+"/wsj.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
html1  = open(output_dir+'/wsj.html').read()

    
sender_email = '********' 
receiver_email = "wsjformiya@gmail.com"
password = '************'#input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "WSJ Selected Daily"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
#text = """\
#Hi,
#How are you? 
#"""
# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")


###----barron -----

url = 'https://www.barrons.com/market-data?'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
table = [i.findNext().findNext() for i in soup.findAll("span",{"class":""}
                                              ) if i.text=='Calendars & Economy'][0]


table = [i.text.split('Coordinated Universal Time') for i in table]
dates = [i[0] for i in table]
table = [i[1] for i in table]
table = [i.split('Period') for i in table]
events = [i[0] for i in table]
table = [i[1] for i in table]
table = [i.split('Forecast') for i in table]
periods = [i[0] for i in table]
table = [i[1] for i in table]
table = [i.split('Actual') for i in table]
forecasts = [i[0] for i in table]
final = [i[1] for i in table]

final_df = pd.DataFrame({'Dates':dates,
             'Events':events,
             'Periods':periods,
             'Forecasts':forecasts,
             'Actual':final})[['Dates','Events','Periods','Forecasts','Actual']]#.set_index('dates')


html = final_df.to_html(index=False)#.replace('border="1"','border="0"')
with open(output_dir+"/barron.html", "w", encoding="utf-8") as file:
    file.writelines('<meta charset="UTF-8">\n')
    file.write(html)
html2  = open(output_dir+'/barron.html').read()


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
    
