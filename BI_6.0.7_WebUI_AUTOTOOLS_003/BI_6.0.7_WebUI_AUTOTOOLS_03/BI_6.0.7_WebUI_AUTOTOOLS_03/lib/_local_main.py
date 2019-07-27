#encoding='utf-8'
#author :鲁旭
#filename:"socket-service"
import socket
import os
import pymysql
import configparser
import sys

def get_localconf(file):
    try:
        Cfg = configparser.ConfigParser()
        Cfg.read(file)
        section="node"
        Me = {x:y for x,y in Cfg.items(section)}
        # print(Me)
        del section,Cfg,file
        return Me
    except:
        print("read local.conf  error")
        sys.exit()

class Exos():
    try:
        Me=get_localconf("config/local.conf")
        localhost = Me['localhost']
        localport =int(Me['localport'])
        streamer_path =Me['streamer_path']
        streamer_conf = Me["streamer_conf"]
        actor=Me["actor"]
        dbhost=Me["dbhost"]
        database=Me["database"]
        dbuser=Me["dbuser"]
        dbpasswd=Me["dbpasswd"]
        dbport=int(Me["dbport"])
    except:
        print("chick local.conf ")
        sys.exit()


    def _exe_mysql(self, sql):
        """
        #操作mysql
        :param sql:
        :return:
        """
        try:
            connect = pymysql.connect(host=Exos.localhost, user=Exos.dbuser, passwd=Exos.dbpasswd, db=Exos.database, port=Exos.dbport)
        except:
            print("数据库连接异常，请核配置文件")
            return "error"
        try:
            cursor = connect.cursor()
            cursor.execute_c2(sql)
            fetch = cursor.fetchall()
            connect.commit()
            cursor.close()
            connect.close()
            return fetch
        except:
            cursor.close()
            connect.close()
            return "error"


    def clean_db(self):
        """
        #清数据库环境
        :return:
        """
        tables=('gmrt', 'live_channel', 'live_cnt', 'live_segments', 'live_url', 'record_task',
                  'rtmp_channel', 'tstv_content', 'tstv_count', 'tstv_gmrt', 'vod_cnt', 'vod_content',
                  'vod_count', 'vod_segments', 'vod_task')

        for table in tables:
            sql="truncate %s" %(table)
            r=Exos()._exe_mysql(sql)
            if r == 'error':
                return {"status": "fail", "action": "clean_db"}
        return {"status": "success", "action": "clean_db"}

    def clean_disk(self):
        """
        #清理磁盘
        :return:
        """
        dirnames = ("/home/http1/storage", "/home/http2/storage",
                  "/home/http3/storage", "/home/http4/storage",
                  "/home/http0/live", "/home/cache/", "/home/tstv_cache")
        for dir in dirnames:
            if os.path.exists(dir) and os.path.isdir(dir):
                a = "rm -rf %s/*"%(dir)
                os.system(a)
        return {"status": "success", "action": "clean_disk"}

    def exe_streamer(self, staus):
        """
        #启动或停止业务
        :param staus:
        {"action":"exe_streamer","streamer_act":"run "}
        :return:
        """
        now_path = os.getcwd()
        a = {"status": "success", "action": "exe_streamer_stop"}
        try:
            os.chdir(Exos.streamer_path)
            if staus == "stop":
                os.system("./run.sh stop")
                action= "exe_streamer_stop"
            elif staus == "start":
                os.system("./run.sh start")
                action = "exe_streamer_start"
            elif staus == "restart":
                os.system("./run.sh stop")
                os.system("./run.sh start")
                action= "exe_streamer_restart"
            a['action']=action
            return a
        except:
            print('run..sh路径错误')
            os.chdir(now_path)
        a["status"]= "fail"
        a["text"]="notfound execute file"
        return a


    def select_config(self, sec, key, value=""):
        """
        查询或修改配置文件
        :param sec: sections
        :param key: options
        :param value: value
        {"action":"select_config","sec":"ID","key":"arear","value":"456"}
        :return: got new values
        """
        cfg = configparser.ConfigParser()
        a = {"status": "fail", "action": "select_config"}
        try:
            abs_file = Exos.streamer_path+"/conf/"+str(Exos.streamer_conf)
            cfg.read(abs_file)
            if value == "":
                '''查询配文件'''
                value2 = cfg.get(sec,key)
            elif value != "":
                '''修改配置文件'''
                cfg.set(sec,key,value)
                with open(abs_file,'w') as fp:
                    cfg.write(fp)
                cfg.read(abs_file)
                value2 = cfg.get(sec, key)
            a['status'] = "success"
            log="pass"
            a["value"] = value2
        except:
            log="filename tpye error or notfound file chick param and config"
        a["text"]=log
        return a


    def _chick_live(self,contentID):
        a = {"status": "fail", "type": "LIVE", "action": "select_content"}
        try:
            sql = "select internal_path from live_segments where contentID=(select contentID from " \
                  "live_channel where  contentID=\'%s\') ORDER by local_seq DESC LIMIT 1,3" % (contentID)
            files = Exos()._exe_mysql(sql)
            if files != "error" and len(files) != 0:
                countts = 0
                for i in files:
                    i = i[0]
                    if os.path.exists(i):
                        if os.path.isfile(i):
                            countts += 1
                if countts == len(files):
                    a['status']="success"
                    log="pass"
                else:
                    log="lose part, not found any part"
            elif files == "error" or len(files) == 0:
                log="db error, or not found content in db"
        except:
            log= "param error"
        a["text"] = log
        return a


    def _chick_playlist(self, contentID ):
        a={"status": "fail", "type": "TS",  "action": "select_content"}
        try:
            sql = "select internal_path from vod_content where " \
                  "contentID=\'%s\' and media_type=\'TS\' and status=1" % (contentID)
            files = Exos()._exe_mysql(sql)
            if files != "error" and len(files) != 0:
                internal_path=files[0][0]
                if Exos.actor == "ecs":
                    internal_path = "/home/http/cache/"+contentID
                if os.path.exists(internal_path):
                    if "playlist.m3u8" in internal_path :
                        with open(internal_path, 'r') as fp:
                            line = fp.readline()
                            while line:
                                line = fp.readline()
                                if 'ts' in line:
                                    ts = line.split('/')[1].split('?')[0]
                                    ts_path = internal_path.replace("playlist.m3u8",ts)
                                    if os.path.exists(ts_path) :
                                        if os.path.isfile(ts_path):
                                           pass
                                        else:
                                            log="not a file"
                                            a["text"]=log
                                            return a
                                    else:
                                        log="lose part"
                                        a["text"] = log
                                        return a
                        log="pass"
                        a["status"]="success"
                    else:
                        log="this is not TS m3u8"
                else:
                    log="not found file  playlist.m3u8 "

            elif files == "error" or len(files) == 0:
                log="db error, or not found content in db"
        except:
            log="other error "
        a["text"]=log
        return a

    def _chick_mp4(self,contentID):
        a={"status": "fail", "type": "MP4",  "action": "select_content"}
        try:
            sql = "select internal_path from vod_content where " \
                  "contentID=\'%s\' and media_type=\'MP4\' and status=1" % (contentID)
            files = Exos()._exe_mysql(sql)
            if files != "error" and len(files) != 0:
                internal_path = files[0][0]
                if Exos.actor == "ecs":
                    internal_path = "/home/http/cache/" + contentID
                if "media.mp4" in internal_path:
                    path=internal_path.replace("media.mp4","")
                    mp4s=os.listdir(path)
                    success=0
                    for i in mp4s:
                        if "media.mp4" in i:
                            success += 1
                    if success == len(mp4s):
                        log="pass"
                        a["status"] = "success"
                    else:
                        log="lose part"
                else:
                    log="this is not  'media.mp4' file"
            elif files == "error" or len(files) == 0:
                log = "db error, or not found content in db"
        except:
            log="param error"
        a["text"]=log
        return a

    def _chick_flv(self,contentID):
        a = {"status": "fail", "type": "FLV", "action": "select_content"}
        try:
            sql = "select internal_path from vod_content where contentID=\'%s\' and " \
                  "media_type=\'FLV\' and status=1" % (contentID)
            files = Exos()._exe_mysql(sql)
            if files != "error" and len(files) != 0:
                internal_path = files[0][0]
                if Exos.actor == "ecs":
                    internal_path = "/home/http/cache/" + contentID
                if "media.flv" in internal_path:
                    path = internal_path.replace("media.flv", "")
                    flvs = os.listdir(path)
                    success = 0
                    for i in flvs:
                        if "media.flv" in i:
                            success += 1
                    if success == len(flvs):
                        log = "pass"
                        a["status"] = "success"
                    else:
                        log = "lose part"
                else:
                    log = "this is not  'media.flv' file"
            elif files == "error" or len(files) == 0:
                log = "db error, or not found content in db"
        except:
            log = "param error"
        a["text"] = log
        return a


    def select_content(self, contentID, type):
        """
         TS、MP4、LIVE、FLV 查询与判断
        :param name: : name is from mysql internal_path or "
        {"action":"select_disk"，"contentID":"TS/10001/3000K","type":"TS"}
        :return: none
        """
        try:
            if type == "TS":
                ret = Exos()._chick_playlist(contentID)
            elif type == "MP4":
                ret = Exos()._chick_mp4(contentID)
            elif type == "FLV":
                ret = Exos()._chick_flv(contentID)
            elif type == "LIVE":
                ret = Exos()._chick_live(contentID)
            return ret
        except:
            return {"status": "fail", "text": "param type error or notfound key 'type'", "action": "select_content"}

    def select_cache(self):
        pass

    def _recv_and_send(self, dict2):
        """
        :param dict: type(bytes,str ,dict)
                      {"action":"clean_disk"}
        :return:
        """
        try:
            action = dict2['action']
        except:
            print("ERROR :param type error or notfound key 'action' ")
            return {"status": "fail", "text": "param type error or notfound key 'action'"}
        #初始化磁盘环境
        if action == 'clean_disk':
            ret = Exos().clean_disk()
        #初始化数据库环境
        elif action == 'clean_db':
            ret = Exos().clean_db()
        #初始化数据库与磁盘环境
        elif action == 'clean':
            ret1= Exos().clean_disk()
            ret2=Exos().clean_db()
            if ret1["status"] == "success" and ret2["status"] == "success":
                ret={"status": "success", "action": "clean_db_disk"}
            else:
                ret={"status": "fail", "action": "clean_db_disk"}
        #业务进程启动、停止
        elif action == 'exe_streamer':
            try:
                streamer_act = dict2['streamer_act']
            except:
                return {"status": "fail", "text": "not found key streamer_act", "action":"exe_streamer"}
            ret=Exos().exe_streamer(streamer_act)
        #业务内容查询与判断
        elif action == 'select_content':
            try:
                contentID=dict2['contentID']
                type=dict2['type']
            except:
                return {"status": "fail", "text": "not found key 'contentID' or 'type'","action":"select_content"}
            ret = Exos().select_content(contentID, type)
        #配置文件读写
        elif action == "scelect_config":
            try:
                sec=dict2["sec"]
                key=dict2["key"]
                value=dict2["value"]
            except:
                return {"status": "fail", "text": "notfound key 'sec' or 'key' or 'value'", "action":"scelect_config"}
            ret = Exos().select_config(sec, key, value)

        if Exos.localhost == "127.0.0.1":
            from lib.funcslib import Ioput
            from lib.funcslib import log
            try:
                key = dict2["key"]
                if action == "input":
                    value =dict2["value"]
                    Ioput.input(keys=key,value=value)
                    log().info(("write sucess",key,value))
                    ret={"status": "sucess","action": "input", "key": key,"value":value}
                elif action == "output":
                    result=Ioput.output(key=key,timeout=60)
                    log().info(("read sucess", key, result))
                    ret={"status": "sucess","action": "output", "key": key,"value":result}
            except:
                ret={"status": "fail","text":"please need correct 'key';'status',value "}
        return ret


    @staticmethod
    def socket_service():
        """
        :return:
        recv dict {}
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Exos.localhost, Exos.localport))
            s.listen(2)
            while True:
                conn, addr = s.accept()
                try:
                    data = eval(conn.recv(10240))

                    m = Exos()._recv_and_send(data)
                except:
                    n = bytes(str({"status": "fail", "text": "input data error please send bytes dict"}), encoding='utf-8')
                    conn.sendall(n)
                    # continue

                else:
                    try:
                        n = bytes(str(m), encoding='utf-8')
                        conn.sendall(n)
                    except:
                        n = bytes(str({"status": "fail","text":"output data error please send bytes dict"}), encoding='utf-8')
                        conn.sendall(n)



if __name__ == "__main__":
    Exos().socket_service()









