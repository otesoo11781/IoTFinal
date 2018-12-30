import math

client = {"username" : None , "lung" : None , "lat" : None  , "distance" : [None , None] }    #client info

treasures = [ {"lung" : 120.2010902 , "lat" : 23.0410212} , {"lung" : 120.20123 , "lat" : 23.0410212} ]  #pos of treasures

unlocked = set() #store the finded treasures

def updatePos(username , lat , lung) :   #return value : true is nearby treasure , otherwise , false
    nearby = False 
    if(username == client["username"]):
        client["lung"] = lung 
        client["lat"] = lat 
        i = 0
        while i < len(treasures):
            dnew =  distance(client["lat"] , client["lung"] , treasures[i]["lat"] , treasures[i]["lung"])
            if nearby == False and dnew <= 0.03 and dnew >= 0 :
                if client["distance"][i] == None : 
                    nearby = True
                elif client["distance"][i] >= 0.03 :
                    nearby = True 
            client["distance"][i] = dnew 
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
	
def getPos() :    #return position of user when username exists , otherwise , return None
    if client["username"] != None :
        return [client["lat"] , client["lung"]]
    else :
        return None 

def updateUser(username) : #return true when update successfully , otherwise false
    client["username"] = username
    return True
	
def getDistance() :  #return a list of distance from treasures , return None if the username doesn't exist 
    if  client['username'] != None: 
        return client['distance']
    else : 
        return None
		
def getUnlocked():
    if client['username'] != None :
        msg = 'You have hunted ' + str(len(unlocked)) + ' treasure(s) '
        for treasure in unlocked :
            msg += '\nNo.' + str(treasure+1) + 'is found!'
        return msg
    else :
        return None