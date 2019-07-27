#encoding='utf-8'
#author :鲁旭
import socket
from lib.funcslib import log, Ioput
def socket_client(host, send_dict, key="index", send=None):

    """
    :param host: host:目标地址
    :param send_dict: send_dict消息内容，类型为dict
    :param key: 返回内容存放的键值,send!=None 时必须带上key
    :param send: 一个实例 Ioput(),或"web"
    :return: 
    """
    HOST = host
    cfg =Ioput.output("cfg")
    PORT=cfg["node"]["localport"]
    PORT=int(PORT)

    s_ds = str(send_dict)
    b_ds = bytes(s_ds, encoding='utf-8')
    log().info(("send data",type(b_ds) ,  b_ds))
    log().info(("object 'send' is ",send))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b_ds)
        log().info(("send dict success ", send_dict))
        data = s.recv(1024)
    k1=(eval(data))
    log().info(("get result dict sucess ",k1))

    if  send == None:
        pass

    elif send == "web":
        """
        接受注入的返回消息，存入类属性中
        """
        Ioput.input(keys=key, value=k1)
        log().info(("write  {", key, ":",  k1,"}  to  'Webdata,  success"))

    elif send != None and send != "web":
        """
        send 是一个实例，用于远程机器返回的数据写入实例中
        """
        send.write_dict(key, value=k1)
        log().info(("write  {", key, ":",  k1,"}  to  send.put_dict success"))

    return k1

if __name__ =="__main__":
    add_live = {"action": "exe_streamer", "streamer_act": "stop"}
    host="192.168.3.191"
    kkk=socket_client(host, add_live)
    print(type(kkk),kkk)


