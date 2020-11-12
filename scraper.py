# %% MODULE IMPORTS

import requests, smtplib
import sys

# email module imports
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# %% GLOBALS
global tf, q, f
ems = []


# %% ARTICLE CLASS DEFINTION

class Article:
    def __init__(self):
        self.title = []
        self.link = []
        self.date = []
        self.source = []
        self.desc = []

    def print_contents(self):
        return (str(self.title) + '\t' + str(self.source) + '\t' + str(self.date) + '\n' + str(self.desc)
                + '\n' + str(self.link) + '\n\n')


def submit(query, emails, timeframe):

    global tf, q
    tf = timeframe
    q = query

    # Zenserp API parameters
    headers = {'apikey': 'ENTERAPIKEYHERE'}
    # queries to run through the API
    search_query = q



    global f
    f = "FROM_EMAIL_HERE"

    MailServer = smtplib.SMTP('smtp.office365.com', 587)
    MailServer.ehlo()
    MailServer.starttls()
    MailServer.login(f, "FROM_EMAIL_PW_HERE")
    # no pw encryption, so use with that in mind


    msg = MIMEMultipart()
    msg['From'] = f
    msg['To'] = emails
    msg['Subject'] = 'News Articles: ' + q

    params = (
        ("q", search_query),
        ("tbm", "nws"),
        ("device", "desktop"),
        ("gl", "US"),
        ("hl", "en"),
        ("location", "United States"),
        ("num", "5"),
        ("timeframe", "w"),
    )

    response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)

    # %%
    articles = []

    processed_response = response.json()
    results = processed_response['news_results']
    for result in results:
        article = Article()
        article.title = result['title']
        article.date = result['date']
        article.source = result['source']
        article.desc = result['description']
        article.link = result['link']
        articles.append(article)

    # %% Formatting Email Body and Sending Email

    body = ""
    for article in articles:
        body += article.print_contents()

    msg.attach(MIMEText(body, 'plain'))

    print(MailServer.sendmail(msg['From'],msg['To'].split(", "),msg.as_string()))
    MailServer.quit()


if __name__ == "__main__":
    query = sys.argv[1]
    timeframe = sys.argv[2]
    emails = ""
    for n in range(3,len(sys.argv)):
        emails += sys.argv[n] + ", "
    submit(query,emails,timeframe)
