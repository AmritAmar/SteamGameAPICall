import sys
import numpy as np
import requests
import json
import datetime
import copy
import time
import re

# Get filenames from Command Line
startingI = int(sys.argv[1])
endingI = int(sys.argv[2])

def getGames():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    r = requests.get(url)
    data = r.json()
    appList = data["applist"]["apps"]

    tupleList = np.array([(0, "")] * len(appList), dtype='object')
    for i, app in enumerate(appList):
        tupleList[i] = tuple([int(app['appid']), str(app['name'])])  
        
    return tupleList

allSteamApps = getGames()
while(len(allSteamApps) == 0):
    allSteamApps = getGames()
    
print(len(allSteamApps))
allSteamApps = sorted(allSteamApps, key=lambda tup: tup[0])[:94100]
print(len(allSteamApps))
print(startingI, endingI)
allSteamApps = allSteamApps[startingI:endingI]
print(len(allSteamApps))     

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#Given ID, return description of game IF it is a game. If not, return Not Valid
def getGamesDescription(id):
    url = "https://store.steampowered.com/api/appdetails?appids=" + str(id)
    r = requests.get(url)
    if r.text == "null":
        return "Yikes"
    else:
        data = r.json()
        if (data[str(id)]['success']):
            if data[str(id)]['data']['type'] == 'game':
                if 'genres' not in data[str(id)]['data'].keys() or 'detailed_description' not in data[str(id)]['data'].keys():
                    return "Not Valid"
                else:
                    return remove_tags(data[str(id)]['data']['detailed_description']), data[str(id)]['data']['genres']
            else:
                return "Not Valid"
        else:
            return "Not Valid"
            
steamGames = []

def getGamesFromApp(apps, gamesArray):
    i = 0
    for app in apps:
        app_id = app[0]
        result = getGamesDescription(app_id)
        
        #clear_output(wait=True)
        print(i)
        print(app_id)
        print(app[1])
        print(result)
        print("==============")
        
        time.sleep(1.5)
        
        i+=1
        if i % 100 == 0:
            print(i, "Done", len(gamesArray))
            
        if result == "Not Valid":
            continue
        elif result == "Yikes":
            continue
        else:
            gamesArray.append(  (app_id, app[1], result[0], result[1])  )
            
getGamesFromApp(allSteamApps, steamGames)

with open("steamGamesChunk" + str(startingI) + "_" + str(endingI) + ".txt", 'w', encoding='utf8') as w:
    for g in steamGames:
        w.write("ThisIsNewID$ " + str(g[0]) + "\n")
        w.write("ThisIsNewNa$ " + g[1] + "\n")
        w.write("ThisIsNewDs$ " + g[2] + "\n")
        genres = ""
        for genre in g[3]:
            genres += genre['description'] + ";"
        w.write("ThisIsNewGs$ " + genres + "\n")
