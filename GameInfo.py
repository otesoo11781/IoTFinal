import math

clients = { }    #client info key is lineID

user_map = {}    #map username to lineID
treasures = [ {"lung" : 120.2010902 , "lat" : 23.0410212} , {"lung" : 120.20123 , "lat" : 23.0410212} ]  #pos of treasures

unlocked = set() #store the finded treasures

def updatePos(username , lat , lung) :   #return value : lineID is nearby treasure , otherwise , empty string
    nearby = '' 
    if(username in user_map):
        lineID = user_map[username]
        clients[lineID]["lung"] = lung 
        clients[lineID]["lat"] = lat 
        i = 0
        while i < len(treasures):
            dnew =  distance(clients[lineID]["lat"] , clients[lineID]["lung"] , treasures[i]["lat"] , treasures[i]["lung"])
            if nearby == '' and dnew <= 0.03 and dnew >= 0 :
                if clients[lineID]["distance"][i] == None : 
                    nearby = lineID
                elif clients[lineID]["distance"][i] >= 0.03 :
                    nearby = lineID
            clients[lineID]["distance"][i] = dnew 
            i += 1 
    return nearby

def distance(lat1 ,lung1  , lat2,  lung2):    #unit is km
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    a = radlat1 - radlat2
    b = math.radians(lung1) - math.radians(lung2)
    s = 2 * math.asin(math.sqrt(math.sin(a/2)**2 +  math.cos(radlat1)*math.cos(radlat2)*math.sin(b/2)**2 ))
    s = s * 6378.137   #radius of Earth
    s = round(s , 3)
    return s 
	
def addTreasures(index) :
    unlocked.add(index)
	
def getPos(lineID) :    #return position of user when username exists , otherwise , return None
    if clients[lineID]["username"] != None :
        return [clients[lineID]["lat"] , clients[lineID]["lung"]]
    else :
        return None 

def addUser(lineID):
    clients[lineID] = {'username' : None , 'lung' : None , 'lat' : None , 'distance' : [None , None]}
	
def updateUser(lineID , username) : #return true when update successfully , otherwise false
    if clients[lineID]["username"] == username : 
        return True
    elif username  in user_map : #username has existed
        return False
    else :
        user_map.pop(clients[lineID]['username'] , None)
        user_map[username] = lineID	
        clients[lineID]["username"] = username
        return True
	
def getDistance(lineID) :  #return a list of distance from treasures , return None if the username doesn't exist 
    if  clients[lineID]['username'] != None: 
        return clients[lineID]['distance']
    else : 
        return None
		
def getUnlocked(lineID):
    if clients[lineID]['username'] != None :
        msg = 'You guys have hunted ' + str(len(unlocked)) + ' treasure(s) '
        for treasure in unlocked :
            msg += '\nNo.' + str(treasure+1) + ' is found!'
        return msg
    else :
        return None