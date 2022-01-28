from threading import Thread 
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import requests
import json
from PyQt5 import QtMultimedia
from requests_barrage import *
from url_wangyi import *

global song_diange
song_diange = []
class Music_Ui(object):
    def setupUi(self, Form):
        self.form = Form
        Form.setObjectName("Form")                          # 窗口标识符
        Form.resize(354, 120)                                # 窗口大小
        '''窗口图标'''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("小电视.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        ''' 创建表格视图控件 '''
        self.tableView = QtWidgets.QTableView(Form)                 
        self.tableView.setObjectName("tableView")                               # 控件标识符
        ''' 创建表格 ''' 
        self.model = QtGui.QStandardItemModel(1,1)                              # 存储任意层次结构的数据（行，列）
        self.model.setHorizontalHeaderLabels(['状态','歌曲名','点歌人','歌手'])   # 表头标题
        self.tableView.verticalHeader().setVisible(False)                       # 隐藏垂直表头
        for x in range(self.model.columnCount()):  
            headItem = self.model.horizontalHeaderItem(x)                       # 获得水平方向表头的Item对象  
            headItem.setFont(QtGui.QFont('微软雅黑',11,QtGui.QFont.Black))       # 设置字体，这里的粗体可以用字体方式设置
        self.tableView.horizontalHeader().setFixedHeight(45)                    # 设置横向表格高度
        self.tableView.setModel(self.model)                                     # 关联视图控件与表格 
        '''设置表格显示列宽行宽格式''' 
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)                    # 自适应窗口大小
        self.tableView.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)         # 第一列内容自适应大小
        self.tableView.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeToContents)         # 第四列内容自适应大小

        Form.setCentralWidget(self.tableView)                   # 设置中央部件（主窗口，Qt中心窗口）
        ''' 创建线程 '''                                                            
        self.thread = Thread_main()
        self.thread.start()                                     # 启动线程  
        ''' 创建线程 '''
        self.thread_paly = Thread_paly() 
        self.thread_paly.update.connect(self.ui_play)           # 关联槽函数
        self.thread_paly.update_add.connect(self.ui_add)        
        self.thread_paly.update_delete.connect(self.ui_delete)  
        self.thread_paly.start()                         
        ''' 使用Qt Designer自动生成 '''
        QtCore.QMetaObject.connectSlotsByName(Form)           
        self.retranslateUi(Form)                                
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate          
        Form.setWindowTitle(_translate("Form", "NPC_V1.0"))
    '''Ui更新播放界面''' 
    def ui_play(self):
        item11 = QtGui.QStandardItem('正在播放')
        item11.setFont(QtGui.QFont('微软雅黑',11,QtGui.QFont.Black))   # 样式 字体大小 
        item11.setForeground(QtGui.QBrush(QtGui.QColor(80,161,79)))   # 颜色
        item12 = QtGui.QStandardItem(song_diange[0]['songName'])
        item12.setFont(QtGui.QFont('宋体',11,QtGui.QFont.Black)) 
        item12.setTextAlignment(QtCore.Qt.AlignCenter)                # 设置文字居中
        item12.setForeground(QtGui.QBrush(QtGui.QColor(255,110,109)))
        item13 = QtGui.QStandardItem(song_diange[0]['nickname'])
        item13.setFont(QtGui.QFont('宋体',11,QtGui.QFont.Black)) 
        item13.setTextAlignment(QtCore.Qt.AlignCenter)           
        item13.setForeground(QtGui.QBrush(QtGui.QColor(31,152,223)))     
        item14 = QtGui.QStandardItem(song_diange[0]['singerName'])
        item14.setFont(QtGui.QFont('宋体',10,QtGui.QFont.Black))            
        item14.setForeground(QtGui.QBrush(QtGui.QColor(255,155,92)))          
        self.model.setItem(0,0,item11)        # 这里是覆盖写入
        self.model.setItem(0,1,item12)
        self.model.setItem(0,2,item13)
        self.model.setItem(0,3,item14)
    '''Ui更新点歌增加界面'''
    def ui_add(self):
        item11 = QtGui.QStandardItem('等待播放')
        item11.setFont(QtGui.QFont('微软雅黑',10,QtGui.QFont.Black))   # 样式 字体大小 
        item11.setForeground(QtGui.QBrush(QtGui.QColor(134,12,234)))  # 颜色
        item12 = QtGui.QStandardItem(song_diange[-1]['songName'])
        item12.setTextAlignment(QtCore.Qt.AlignCenter) 
        item12.setFont(QtGui.QFont('宋体',11,QtGui.QFont.Black))            
        item12.setForeground(QtGui.QBrush(QtGui.QColor(255,110,109)))         
        item13 = QtGui.QStandardItem(song_diange[-1]['nickname'])
        item13.setFont(QtGui.QFont('宋体',11,QtGui.QFont.Black))            
        item13.setForeground(QtGui.QBrush(QtGui.QColor(31,152,223)))     
        item14 = QtGui.QStandardItem(song_diange[-1]['singerName'])
        item14.setFont(QtGui.QFont('宋体',10,QtGui.QFont.Black))            
        item14.setForeground(QtGui.QBrush(QtGui.QColor(255,155,92)))  
        self.model.appendRow([
                                QtGui.QStandardItem(item11),
                                QtGui.QStandardItem(item12),
                                QtGui.QStandardItem(item13),
                                QtGui.QStandardItem(item14)
                            ])
        ins=self.form.size().height()
        self.form.resize(354, ins+30)
    '''Ui更新删除增加界面'''
    def ui_delete(self):
        self.model.removeRow(1)   # 删除第2行，这里自动递减上
        ins=self.form.size().height()
        self.form.resize(354, ins-30)
class Thread_main(QtCore.QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        time = '2021-10-12 14:21:19'
        while True: 
            rev = barrage()
            if rev['timeline'] > time:
                time = rev['timeline']
                print(rev['text'])
                Message_pro(rev)                          
class Thread_paly(QtCore.QThread):  # 播放函数
    '''自定义槽函数'''
    update = QtCore.pyqtSignal()  # 可选str，int，dict
    update_add = QtCore.pyqtSignal()  # 可选str，int，dict
    update_delete = QtCore.pyqtSignal()  # 可选str，int，dict     
    def __init__(self):
        super().__init__()
    def run(self):
        ''' 创建QT媒体播放类 '''
        self.player = QtMultimedia.QMediaPlayer()
        self.player_time = 0
        #path = os.path.dirname(os.path.abspath("__file__"))+('\music')
        #path_list = os.listdir(path)
        global ui_state  # 全局变量点歌业务状态更新
        ui_state = False
        paly_state = True # 
        while True:
            ''' 这里添加点歌业务的ui更新 '''
            if ui_state == True:
                self.update_add.emit()
                # 这里可以写怎加窗口长度的问题

                ui_state = False
            if self.player.position() == (0 or self.player_time): # 这里判断播放器是否在工作状态
                self.update_delete.emit() # 这里真聪明，如果没得砍就不砍，就很灵性
                if paly_state == False:
                    song_diange.pop(0)
                if 0 < len(song_diange) <= 6 :
                    self.playMusic()
                else:
                    self.play_random()  # 这里会自动覆盖写入相关的参数
                paly_state = False
            else:
                self.player_time = self.player.position()
            time.sleep(1)
    '''随机函数url请求'''
    def play_random(self):
        url = json.load(open("./config.json", encoding='utf-8'))["bilibili_api"]["random_song"]
        rev = requests.post(url).json()     # 这里用post请求这里有i/o请求
        song_diange.append({"singerName":rev['data']['artistsname'], "songName": rev['data']['name'],"url_mp3":rev['data']['url'],'nickname':'系统随机',"rev_name":rev['data']['name']})
        # 而这里是末尾添加
        self.playMusic()
    '''路径函数'''
    def play_path(self):
        if song_diange[0]['nickname'] == '系统随机':
            self.player_path = song_diange[0]["url_mp3"] # 这里永远会播放列表的第一首
        else:
            self.player_path = song_diange[0]["url_mp3"][1:-1] # 这里有个巨坑！！！ 路径无法识别双引号的url地址，单引号可以！！！
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.player_path)))
        self.update.emit() # 写入数据
        # 这里更新了ui界面
    '''音量控制函数'''
    def play_volume(self):
        self.player.setVolume(50) # 模拟器控制范围int(0—100)音量
    '''播放音乐函数'''
    def playMusic(self):
        self.play_path()    # 加载路径
        self.play_volume()  # 控制音量
        self.player.play()  # 播放
def Message_pro(rev):
    if rev['text'][0:2] =="点歌" :
        number = 0
        NetEase_url(rev,number)
    elif rev['uid'] == "565432543" :
        if rev['text'][0:4] == "列表播放":
            pass
def asyncis(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
@asyncis
def bilibili_send(text):    # 弹幕send
    roomid = json.load(open("./config.json", encoding='utf-8'))["roomid"]
    url = json.load(open("./config.json", encoding='utf-8'))["bilibili_api"]["send_api"]
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
    # 构造请求
    response = requests.post(url,data=data,cookies=cookie)
    print(response.json())  # 这个必须要有，因为可以看到调用函数发送结果所具体的信息
    # 系统对消息的敏感内容有屏蔽措施，且令牌和Cookie会根据计算机不同推送消息，已推送的消息事实为准
@asyncis
def NetEase_url(rve,number):
    song_name_rve = rve['text'][2:].strip()
    '''检查列表点歌数量为7'''
    if len(song_diange) > 6 : # or song_name in song_diange["rev_name"]
        print("超过了数量了呢")
        return
    '''检查列表相同性'''
    for i in song_diange: # 这么写考虑的机器素质
        if song_name_rve == i["rev_name"]:
            print("重复了呢")
            return
    d = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song_name_rve, "type": "1", "offset": "0",
         "total": "true", "limit": "30", "csrf_token": ""}
    d = json.dumps(d) # 👆构造请求，转换为json格式
    random_param = get_random() # 这里是属于网页分析师的起点
    param = get_final_param(d, random_param)
    song_list = get_music_list(param['params'], param['encSecKey']) # 这里已经拿到我们需求的搜过页面列表
    if len(song_list) > 0:
        song_list = json.loads(song_list)['result']['songs'][number]
        singerName = song_list['ar'][0]["name"]
        song_name = song_list["name"]
        item = json.dumps(song_list)
        d = {"ids": "[" + str(json.loads(str(item))['id']) + "]", "level": "standard", "encodeType": "","csrf_token": ""}
        d = json.dumps(d)
        param = get_final_param(d, random_param)
        song_info = get_reply(param['params'], param['encSecKey']) # 这里已经拿到含有url的返回的结果,这里会出现null的问题，可以自己调自己
        if len(song_info) > 0:
            song_info = json.loads(song_info)
            song_url = json.dumps(song_info['data'][0]['url'], ensure_ascii=False)
            if song_url == 'null':
                number += 1 
                NetEase_url(rve,number)  # 多线程相关不受影响
                return
            song_diange.append({"singerName": singerName, "songName": song_name,"url_mp3":song_url,'nickname':rve['nickname'],"rev_name":song_name_rve})
            global ui_state
            print(song_diange)
            ui_state = True         # ui界面添加状态
        else:
            print("该首歌曲解析失败，可能是因为歌曲格式问题")
    else:
        print("很抱歉，未能搜索到相关歌曲信息")


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)  # 外部参数列表
    MainWindow = QtWidgets.QMainWindow()  # 我就是要合体的类哦 如果是空的可以直接定义 
    win=Music_Ui()                        # 啊啊啊，界面类也实例化了
    win.setupUi(MainWindow)               # 我要合体了
    MainWindow.show()                     # 合体后的成功展示喽
    sys.exit(app.exec_())                 # 退出中使用的消息循环，结束消息循环时就退出程序

