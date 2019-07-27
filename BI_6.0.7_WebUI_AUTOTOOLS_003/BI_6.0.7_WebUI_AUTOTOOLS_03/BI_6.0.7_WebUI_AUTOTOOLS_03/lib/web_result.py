import web
import os
from lib.sendmessenger import socket_client


class cacheresult:
    def GET(self):
        print("", 'Not support')
        print("222222", web._data(), web.ctx.path, web.ctx.fullpath)
        #uid = web.input().uid
        #if uid is not None:
            #if uid == '1':
                #for i in range(0, 1000):
                    #time.sleep(0.1)
                    #continue
                #return 'uid is 1'
            #else:   	
                #return 'uid is %s' % (uid)
        #else:
        return 'Not found uid'


    def POST(self):
        try:
            web.header('Content-Type', len("text/html"))
            dd=str(web._data(), encoding="utf-8")
            dd=eval(dd)
            key=dd["videos"][0]['contentID']
            print(key,":::::",dd)
            datas = {"action": "input", "key": key, "value": dd}
            socket_client("127.0.0.1", datas)


            return (web._data())

        except Exception as e:
            print("",str(e))
        return

def urlweb():
    print("urlweb pid is ", os.getpid())
    urls = (
            '/.*', 'cacheresult',
           )
    app = web.application(urls, globals())
    web.httpserver.runsimple(app.wsgifunc(), ("localhost", 8088))
    #app.run()




if __name__ == "__main__":
    urlweb()


