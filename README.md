# IoTFinal
A simple game to treasure hunting

使用時，記得把裡面的linebot的資訊改成自己的，還有client的userID，要改成自己的tracking app的名字

server使用方式:
1.IOTTalk連線，Tracking ------> Final_treasure
2.ngrok 打開  ngrok http 32768
3.linebot設定照之前講義，做一做
4.新增兩張QRcode ，URL分別是 ngrok的 url 加上 /0 和 /1  (代表第一個寶藏跟第二個寶藏的URL)
5.把程式的config改完，run DAI.py
6.Iottalk的ODF把他掛上去


client使用方式:
1.加上linebot的好友
2.使用 !update username ，來新增用戶名，username隨便填你想填的名字
3.run Tracking app ，名字使用上面設定的username
4.可以開始打指令: !position --> 查詢現在位置
                  !distance --> 跟各寶藏的位置
				  !treasure --> 已經找到哪些寶藏
				  !update username --> 更新用戶名
				  
5.掃描QRcode ，就會找到寶藏，然後會將找到寶藏的訊息廣播給大家