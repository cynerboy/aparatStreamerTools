from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlite3
import json
import os
import threading

#channel page
channelPage = "miladpage"

#sql connection
conn = sqlite3.connect('aparatDB.db', check_same_thread=False)
cursor = conn.cursor()

#init ruby and follower count
followerCount = 0
rubyCount = 0

#function write json File
def jsonFileCreator(filePath, data):
      with open(filePath, 'w') as json_file:
            json.dump(data, json_file)
          
#function checkNew
def findNewEvent(soup):
       global followerCount
       global rubyCount
      #follower
       usernameElement = soup.find_all("span", attrs={"class": "username"}) #primary
       #ruby donator
       channelElement = soup.find_all("a", attrs={"class": "channel"}) #primary
       if len(usernameElement) > followerCount:
          for x in range(followerCount, len(usernameElement)):
                followerCount = followerCount + 1
                print("flower count: ", followerCount)
                print("username len count: ", len(usernameElement))
                # add to sqlite
                print("follower added: ", usernameElement[followerCount-1].text)
                new_record = (usernameElement[followerCount-1].text, 'follower', '0', 0)
                cursor.execute("INSERT INTO eventlist (username, role, ruby, show) VALUES (?, ?, ?, ?)", new_record)
                # commit data in sqlite
                conn.commit()
       else:
             print("no follower")

       if len(channelElement) > rubyCount:
          coinElement = soup.find_all("span", attrs={"class": "coin-count"})
          #rubyMessageElement = soup.find_all("div", attrs={"class": "ruby-message"})
          for x in range(rubyCount, len(channelElement)):
                rubyCount = rubyCount + 1
                # add to sqlite
                print("donator added: ", channelElement[rubyCount-1].text)
                new_record = (channelElement[rubyCount-1].text, 'donator', coinElement[rubyCount-1].text, 0)
                cursor.execute("INSERT INTO eventlist (username, role, ruby, show) VALUES (?, ?, ?, ?)", new_record)
                # commit data in sqlite
                conn.commit()
       else:
             print("no ruby donator")

#function source checker     
def sourceCheck():
      while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            findNewEvent(soup)
            time.sleep(5)

#function register record
def registerRecord(show, id):
      record_to_update = (show, id)  # Example values for update
      cursor.execute("UPDATE eventlist SET show = ? WHERE id = ?", record_to_update)
      conn.commit()

#function check database
def checkDB():
      while True:
            if not os.path.exists("data.json"):
                  cursor.execute("SELECT * FROM eventlist WHERE show=0 ORDER BY id ASC LIMIT 1")
                  rows = cursor.fetchall()
                  for row in rows:
                        if(row[2] == 'donator'):
                              data = {
                                    "role": row[2],
                                    "username": row[1],
                                    "ruby": row[3]
                              }
                        else:
                              data = {
                                    "role": row[2],
                                    "username": row[1]
                              }
                        registerRecord(1, row[0])
                        jsonFileCreator("data.json", data)
            
            time.sleep(5)


options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
driver = webdriver.Chrome(options=options)
driver.get('https://www.aparat.com/' + channelPage + '/live/chat')


thread1 = threading.Thread(target=sourceCheck)
thread2 = threading.Thread(target=checkDB)

time.sleep(5)

thread1.start()
thread2.start()
thread1.join()
thread2.join()