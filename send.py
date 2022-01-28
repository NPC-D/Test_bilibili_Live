import requests
import json
import time


roomid = json.load(open("./config.json", encoding='utf-8'))["roomid"]
url = json.load(open("./config.json", encoding='utf-8'))["bilibili_api"]["send_api"]
def send_bilibili(text):
    now = time.time()
    data = {
        'color': '16777215',         # 颜色           
        'fontsize': '25',            # 字体大小
        'mode': '1',                 # 模式
        'msg': text,                 # 消息内容
        'rnd': str(int(now)),        # 这个是时间戳
        'roomid': roomid,            # 这里必须是直播房间的id号
        'bubble': '0',               # 泡沐
        'csrf_token': 'b74539dbfc9af7c71ef5045d83443a09',    # 令牌在不同的电脑上会不同，但都可以用
        'csrf': 'b74539dbfc9af7c71ef5045d83443a09',        
        }
    # cookie的信息也会根据不同的电脑改变
    cookie = {
        'Cookie':"_uuid=B6D5AFA8-E4B5-0674-A0CE-89D3D3E0AE8575623infoc; buvid3=7BAEF105-B970-4BCA-8700-97EBCF7E8E36143075infoc; blackside_state=1; rpdid=|(J|~|)|Y~RJ0J'uY|)YJmJ~u; buvid_fp=7BAEF105-B970-4BCA-8700-97EBCF7E8E36143075infoc; buvid_fp_plain=7BAEF105-B970-4BCA-8700-97EBCF7E8E36143075infoc; LIVE_BUVID=AUTO3316222130607020; CURRENT_QUALITY=120; CURRENT_BLACKGAP=1; sid=i07bzwd8; DedeUserID=100711328; DedeUserID__ckMd5=26931068a84ff8c7; SESSDATA=ce9a4a13%2C1644008413%2Cc49ca*81; bili_jct=b74539dbfc9af7c71ef5045d83443a09; bp_t_offset_100711328=580063297859781313; bp_video_offset_100711328=580063297859781313; CURRENT_FNVAL=80; innersign=0; bfe_id=5db70a86bd1cbe8a88817507134f7bb5; PVID=1; fingerprint3=c66cefcfd9e20678af3b4e43fa893bd6; fingerprint=276c637e30a8178d804b4a5d7b96f159; fingerprint_s=bb33e4788370041daa7c8366a54dade6"
        }
    #构造请求
    response = requests.post(url,data=data,cookies=cookie)
    print(response.json())  # 这个必须要有，因为可以看到调用函数发送结果所具体的信息

# 系统对消息的敏感内容有屏蔽措施，且令牌和Cookie会根据计算机不同推送消息，已推送的消息事实为准