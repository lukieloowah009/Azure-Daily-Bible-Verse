import datetime
import logging
import requests
from bs4 import BeautifulSoup
import smtplib, ssl

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:


    #Webscraping bible verse
    URL = "https://www.biblestudytools.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    chapterVerseObj = soup.find("a", {"class": "blue-link"})
    contentObj = soup.find("span", {"class": "verse"})

    chapterVerse = (chapterVerseObj.text).strip()

    content = (''.join([i for i in contentObj.text if not i.isdigit()])).strip()


    #Sending Email
    sender = 'bibleversedaily785@gmail.com'
    receivers = [
        'lukieloowah009@gmail.com',
        'octoberkheeler@gmail.com',
        'sawloowah@gmail.com',
        'yadanarhinata.10@gmail.com'
    ]

    message = """From: Daily Bible Verse <bibleversedaily785@gmail.com>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: Daily Bible Verse

    Daily Bible Verse\n
    {}: {}\n
    Source: {}
    """.format(chapterVerse, content, URL)

    port = 465
    password = '<removed for security purpose>'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("bibleversedaily785@gmail.com", password)
        server.sendmail(sender, receivers, message)
        print("Successfully sent.")


