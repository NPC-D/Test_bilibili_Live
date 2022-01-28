
import requests
import json

room = json.load(open("./config.json", encoding='utf-8'))["roomid"]
url_accept = json.load(open("./config.json", encoding='utf-8'))["bilibili_api"]["accept_message"]

def barrage():
    try:
        res = requests.get(url_accept+room).json()
        #res_json = json.loads(res)
        #res_json = json.loads(response.text)
        #ins = res['data']['room'][-1]
        return barrage_rules(res)
    except Exception as e:
        print("啊这，api函数出了亿点点问题呢\n"+str(e))

def barrage_rules(res):
    try:
        res = res['data']['room'][-1]
        if res == None :
            barrage()
            print("...好像出了点问题，铲屎官快来看下")
        return (res)              
    except Exception as e:
        print("啊这，弹幕处理函数出了亿问题呢\n"+str(e))


    
# 20.10.18在少数弹幕消息发送的情况下会报错
#
# response.json() 是requests这个第三方库提供的, 将json数据转换成python 字典的方法.
# json.loads(text) 是 python 内置的将json数据转换成python字典的方法, 跟requests库没关系.
#
# url_inf = 'https://api.bilibili.com/x/space/acc/info?mid='+str(UID)
# # url = "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=4250752" # 这里对接房间号