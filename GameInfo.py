import math

client = {"userID" : None , "lung" : None , "lat" : None , "treasure" : set() , "distance" : [None , None] }    #client info

treasures = [ {"lung" : 123.456 , "lat" : 23.5} , {"lung" : 123.789 , "lat" : 23.6} ]  #pos of treasures


def updatePos(userID , lat , lung) :   #return value : true is nearby treasure , otherwise , false
    if(userID == client["userID"]):
        client["lung"] = lung 
        client["lat"] = lat 
        i = 0
        dmin = 1e9
        while i < len(treasures):
            client["distance"][i] = distance(client["lung"] , client["lat"] , treasures[i]["lung"] , treasures[i]["lat"])
            dmin = min(client["distance"][i] , dmin)
        if(dmin <= 500 and dmin >= 0 ) :
            return true
        else :
            return false
    else :
        return false 	

def distance(lat1 ,lung1  , lat2,  lung2):    #unit is km
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    a = radlat1 - radlat2
    b = math.radians(lung1) - math.radians(lung2)
    s = 2 * math.asin(math.sqrt(math.sin(a/2)**2 +  math.cos(radlat1)*math.cos(radlat2)*math.sin(b/2)**2 ))
    s = s * 6378.137   #radius of Earth
    s = round(s , 3)
    return s 
	
def findTreasures(index) :
    client["treasure"].add(index)
	
def getPos(userID) :    #return position of user when userID is exist , otherwise , return None
    if(userID == client["userID"]) :
        return [client["lat"] , client["lung"]]
    else :
        return None 