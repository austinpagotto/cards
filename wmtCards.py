#%%
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from datetime import datetime
import time
import smtplib
import credentials


# %%

link = credentials.link

while True:
    if str((datetime.now().minute) / 5)[-1] == "0":
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get(link)

        htmlData = BeautifulSoup(driver.page_source, "html.parser")

        # Search for product Names
        productNames = []

        for name in htmlData.find_all(class_="css-1c6n0sl eudvd6x0"):
            productNames.append(name.get_text())

        # Search for stock status
        stockStatus = []

        for status in htmlData.find_all(class_="css-1pjxmn6 epettpn4"):
            stockStatus.append(status.get_text())

        # send email flag if there is anything other than oos
        sendEmailBool = False
        for text in stockStatus:
            if text != "Out of stock":
                sendEmailBool = True
            else:
                print(sendEmailBool)

        if sendEmailBool:
            # Build Message
            message = ''
            for i in range(len(productNames)):
                message = "\n".join([message,link,productNames[i], stockStatus[i].upper()])

            # Send Email
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login(credentials.username, credentials.pw)
            s.sendmail(credentials.username, credentials.username, message)
            s.quit()

        time.sleep(30)
    else:
        print("notTime!")
        time.sleep(10)

#%%

# %%

# %%
