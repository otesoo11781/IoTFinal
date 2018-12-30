import time, DAN, requests, random ,GameInfo

from io import open
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, request, abort , render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import threading

line_bot_api = LineBotApi('vLiLtCXjeAzDCVB7IuihygLrCwCThANorDPXy2qX0ZZH9kW7GK4OzscbVrt4kzzT5mRIFF7FybOfUCOznr81Q8pS60UYxCaoOc/oqb9EYHRBGxjGgqz5Y409Szkrk/GUjx7JBl6Relhnvb48Gy5gJAdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('e51ad3f66a7f7cf89f79cd0dce3ae816')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)


def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))
	
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)
        GameInfo.addUser(userId)
		
    cmd = Msg.split()
    if cmd[0] == '!update' and len(cmd) >= 2  :
        if GameInfo.updateUser(userId ,cmd[1]) :
            line_bot_api.push_message(userId, TextSendMessage(text='Update username : "' + cmd[1] + '"Successfully!!'))
        else :
            line_bot_api.push_message(userId, TextSendMessage(text='Username is duplicated !!'))
    elif cmd[0] == '!position' : 
        pos = GameInfo.getPos(userId) 
        if pos == None :
            line_bot_api.push_message(userId, TextSendMessage(text='Please set your username first by typing !update <your_name>'))
        elif pos[0] != None and pos[1] != None : 
            line_bot_api.push_message(userId, TextSendMessage(text='lat : ' + str(pos[0]) + '\nlung : ' + str(pos[1])))      	
        else : 
            line_bot_api.push_message(userId, TextSendMessage(text='Please confirm your tracking app or GPS work properly!!'))      
    elif cmd[0] == '!distance' : 
        d = GameInfo.getDistance(userId)
        if d == None : 
            line_bot_api.push_message(userId, TextSendMessage(text='Please set your username first by typing !update <your_name>'))
        elif d[0] != None and d[1] != None : 
            line_bot_api.push_message(userId, TextSendMessage(text='From 1st treasure : ' + str(d[0]) + ' km\nFrom 2nd treausre : ' + str(d[1]) +' km'))
        else : 	
            line_bot_api.push_message(userId, TextSendMessage(text='Please confirm your tracking app or GPS work properly'))
    elif cmd[0] == '!treasure' : 
        unlocked = GameInfo.getUnlocked(userId)
        if unlocked == None :
            line_bot_api.push_message(userId, TextSendMessage(text='Please set your username first by typing !update <your_name>'))
        else :
            line_bot_api.push_message(userId, TextSendMessage(text= unlocked ) )
    else : 
        line_bot_api.push_message(userId, TextSendMessage(text='Invalid command!!'))


@app.route('/<int:index>' , methods = ['GET'])
def treasure(index) :
    if index < len(GameInfo.treasures) : 
        GameInfo.addTreasures(index)
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='Congradulation!! Someone find No.' + str(index+1) + ' treausre!!'))
        return render_template('treasure'+str(index+1)+'.html')   #return a description(html) about the treasure
    else :
        return 'Oops! You find a imitation! >_<'

ServerURL = 'https://test.iottalk.tw' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = "0416205" #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Final_treasure'
DAN.profile['df_list']=['position']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

def Iottalk_message():
    while True:
        try:
            value1=DAN.pull('position')
            if value1 != None :  
                nearby = GameInfo.updatePos(value1[0] , float(value1[1]) , float(value1[2]) )
                if nearby :
                    line_bot_api.push_message(nearby, TextSendMessage(text='Treasure is nearby!!'))  # Push API example
				
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)
        time.sleep(0.2)


if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
            GameInfo.addUser(userId)
    except Exception as e:
        print(e)
    t = threading.Thread(target=Iottalk_message)
    t.daemon = True     # this ensures thread ends when main process ends
    t.start()
	
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)