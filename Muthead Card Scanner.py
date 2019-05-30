import csv
import bs4
import requests
import re
import os


###
FILE_PATH = "ENTER PATH TO STORE CSV FILE"
###


#Determines how many pages need to be scanned
link = 'https://www.muthead.com/19/players?filter-market=3&page=1'
sause = requests.get(link)
soup = bs4.BeautifulSoup(sause.text, 'html.parser')
for player in soup.find_all("a", {"class": "b-pagination-item"}):
    gdata = (player.text)
    gdata = re.split('>|<', gdata)
    if int(gdata[0]) > 10:
        muthead_pages = int(gdata[0])

#Variables
overalls =['6','7','8','9']
database = 0
index = 1

#Link Variables
link_text = 'https://www.muthead.com/19/players?filter-market=3&page='
link_number = 1

#Database Key
player_info = ['Name', 'Position', 'Overall', 'Program']
with open(FILE_PATH, 'a', newline='') as file:
    wr = csv.writer(file, dialect='excel')
    wr.writerow(player_info)

while link_number <= muthead_pages:
    #Prints current page
    #print("Page: " + str(link_number))

    #Scans pages for players
    link = link_text + str(link_number)
    sause = requests.get(link)
    soup = bs4.BeautifulSoup(sause.text, 'html.parser')
    for player in soup.find_all('table'):
        gdata = (player.text)
        gdata = re.split('\n', gdata)
        for player in gdata:
            if any(c.isalpha() for c in player):
                if database == 1:
                    #Adds Program to Player Info
                    if index == 2:
                        player_info[3] = player
                        index = 3

                    #Adds Name to Player Info
                    if player.startswith(' '):
                        player_info[0] = player.lstrip(' ')
                        index = 2
                        
                    for overall in overalls:
                        #Adds Overall to Player Info
                        if player.startswith(overall):
                            player_info[2] = player[:2]
                            index = 4

                        #Adds Position to Player Info
                        if 'CB' in player:
                            player_info[1] = player[2:4]
                        elif player[2] == 'C' or player[2] == 'K' or player[2] == 'P':
                            player_info[1] = player[2]
                        elif 'MLB' in player:
                            player_info[1] = player[2:5]
                        elif 'LOLB' in player or 'ROLB' in player:
                            player_info[1] = player[2:6]
                        else:
                            player_info[1] = player[2:4]

                #Adds Info to CSV file           
                if index == 4:
                    with open(FILE_PATH, 'a', newline='') as file:
                        wr = csv.writer(file, dialect='excel')
                        wr.writerow(player_info)
                    player_info = ['', '', '', '']

                #Database Check
                if player == 'PS4':
                    player_info = ['', '', '', '']
                    database = 1
    #Resets Variables after current page                
    link_number += 1
    database = 0
    index = 1
