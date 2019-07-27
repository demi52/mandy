import requests

__autor__ = "鲁旭"

import os
import re
import smtplib
import threading
import time
import inspect
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql
import cx_Oracle
import configparser
import xlrd
import xlwt
import http.server as hs
from config.dataoftest import *

from config.conf import LOG, Oracle_p as CO, Mysql as C, Suite, report, backage, BI_protal


# from logging.handlers import TimedRotatingFileHandler
# from logging.handlers import RotatingFileHandler

class Ioput():
    Cfgdata={}
    Webdata={}

    def __init__(self):
        self.outherdata={}


    @classmethod
    def function_name(cls, classname, casennumber=""):
        funcname = inspect.stack()[1][3]
        cls.input(keys="funcname", value="%s.%s_%s" % (classname, funcname, casennumber))
        log().info("{0} test start {0}".format("=" * 50))

    @classmethod
    def input(cls,keys="web",value=None):
        """
        写入
        :param keys:
        :param value:
        :return:
        """
        if keys == "cfg":

            "读取配置文件local.config,转为字典存放到类属性Cfgdata"

            cfg = configparser.ConfigParser()
            absconfig=os.path.abspath(__file__)
            dirname = absconfig.replace(os.path.basename(absconfig), "")

            if "/" in absconfig:
                cfgname =r"%s/../config/local.conf" % dirname
            else :
                cfgname = r"%s\..\config\local.conf" % dirname
            cfg.read(cfgname,encoding="utf-8")
            secs = cfg.sections()
            Ioput.Cfgdata = {secstion: {key: values for key, values in cfg.items(secstion)} for secstion in secs}

        else:
            "存放返回通知结果,字典类型"
            Ioput.Webdata[keys] = value

    @classmethod
    def output(cls,key="funcname",timeout=60):
        """
        :param key:
        :param timeout:
        :return:
        """
        starttime = int(time.time())
        if key == "cfg":
            "返回配置文件内容"
            result_dict=Ioput.Cfgdata
        elif key == "web":
            "返回接受的新的用例名称通知结果"
            while True:
                if int(time.time()) - starttime >=timeout:
                    result_dict = {key: "not found key do not have values"}
                    break
                elif key in Ioput.Webdata:
                    result_dict = Ioput.Webdata.get(key)
                    Ioput.Webdata.pop(key,"please Waiting for the wirte value")
                    break
                time.sleep(1)


        else:
            result_dict = Ioput.Webdata.get(key, "null")


        return result_dict


    def write_dict(self, key, value):
        """
        线程通信input  str
        :param key:
        :param value:
        :return:
        """
        self.outherdata[key] = value

    def read_dict(self, key, timeout=60):
        """
        线程通信output  dict
        :param key:
        :param timeout:
        :return:
        """
        starttime = int(time.time())
        while True:
            if int(time.time()) - starttime >= timeout:
                result_dict = {key: "not found key do not have values"}
                break
            elif key in self.outherdata:
                result_dict = self.outherdata.get(key)
                self.outherdata.pop(key,"please Waiting for the wirte value")
                break
            time.sleep(1)
        return result_dict


def getparamnow(func):
    def wrapper(*args, **kwargs):
        """获取传入的参数"""
        func(*args, **kwargs)
        outdict = args[0].__dict__.copy()
        outdict = dict(outdict)
        remove = ("ele_tables", "driver", "ele_Table", "table_firstline_list", "data", "datatext")
        [outdict.pop(i, None) for i in remove if i in outdict]
        args[0].kws = kwargs

        if Ioput.output("pathstatus") == "exit":
            text = "setupClass 不通过，当前用例判为失败： {0}".format(Ioput.output("patherror"))
            log().critical(text)
            assert False, text
        log().debug("前置环境校验通过,next")
        log().debug("function:{1} 当前参数 :{0} ".format(outdict, func.__name__))
    return wrapper

def get_token(func):

    def wrapper(*args, **kwargs):
        """实时获取token"""
        url = "{0}login?userid=test1&qdi=login&password=e10adc3949ba59abbe56e057f20f883e".format(
            BI_protal.token_server_url)
        result = requests.get(url).text
        token = re.compile(r"(?<=\"token\":\").+?(?=\")").search(result).group()
        args[0].token = token
        func(*args, **kwargs)
    return wrapper

def exef(status = False):
    """
    装饰函数
    :param status: True执行，False 不执行
    :return:
    """
    def bac(func):
        def war(*args, **kwargs):
            if status:
                func(*args, **kwargs)
            else:
                log().info("跳过步骤{0}".format(str(func)))
        return war
    return bac



def exeassert(text=""):
    """
    装饰函数
    :param text: 在执行前首先判断
    :return:
    """
    def bac(func):
        def war(self,*args,**kwargs):
            try:
                self.checktext(1,element=text)
            except:
                Ioput.input("pathstatus","exit")
            else:
                self.func(*args,**kwargs)

        return war
    return bac

def exe(func):
    def war(*args,**kwargs):
        obj=func(*args,**kwargs)
        func.out()
        return obj

    return war

@exe
class Log():
    name = "null"
    object = None

    def __new__(cls, *args, **kwargs):
        if cls.name != Ioput.output("funcname"):
            cls.name = Ioput.output("funcname")
            cls.object = super().__new__(cls, *args, **kwargs)
        return cls.object

    @classmethod
    def out(cls):

        level = LOG.loglevel
        logoutput = LOG.logoutput
        name = Ioput.output( "funcname" )
        logger = logging.getLogger( name )
        if not logger.handlers:
            # 设置日志显示级别
            if level == "info":
                logger.setLevel( logging.INFO )
            elif level == "debug":
                logger.setLevel( logging.DEBUG )
            elif level == "warning":
                logger.setLevel( logging.WARNING )
            elif level == "error":
                logger.setLevel( logging.ERROR )
            else:
                logger.setLevel( logging.INFO )

            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s' )

            fh = logging.FileHandler( LOG.logpath )
            ch = logging.StreamHandler()
            fh.setFormatter( formatter )
            ch.setFormatter( formatter )

            # log_file_handler = TimedRotatingFileHandler(filename=logpath, when="M", interval=1, backupCount=1)
            # log_file_handler.suffix = "%Y-%m-%d_%H-%M.userlog"
            # log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.userlog$")
            # logger.addHandler(log_file_handler)

            # 设置日志输出位置
            if logoutput == "file":
                logger.addHandler( fh )
            elif logoutput == "console":
                logger.addHandler( ch )
            else:
                logger.addHandler( fh )
                logger.addHandler( ch )

        return logger

def log():

    level = LOG.loglevel
    logoutput = LOG.logoutput
    name= Ioput.output("funcname")
    logger = logging.getLogger(name)
    if not logger.handlers:
        #设置日志显示级别
        if level == "info":
            logger.setLevel(logging.INFO)
        elif level == "debug":
            logger.setLevel(logging.DEBUG)
        elif level == "warning":
            logger.setLevel(logging.WARNING)
        elif level == "error":
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s.%(funcName)s:%(lineno)d] - %(message)s')

        fh = logging.FileHandler( LOG.logpath ,encoding="utf-8")
        ch = logging.StreamHandler()
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # log_file_handler = TimedRotatingFileHandler(filename=logpath, when="M", interval=1, backupCount=1)
        # log_file_handler.suffix = "%Y-%m-%d_%H-%M.userlog"
        # log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.userlog$")
        # logger.addHandler(log_file_handler)

        #设置日志输出位置
        if logoutput == "file":
            logger.addHandler(fh)
        elif logoutput == "console":
            logger.addHandler(ch)
        else:
            logger.addHandler(fh)
            logger.addHandler(ch)

    return logger

def getdata(file=None,sec=None):
    path = re.compile(r"lib.+py").sub(r"data\%s" % file, r"%s" % __file__)
    path = os.path.realpath(path)
    cfg = configparser.ConfigParser()
    cfg.read(path,encoding="utf-8")
    parms = [eval(cfg.get(sec, x)) for x in cfg.options(sec)]
    return parms

class Get2():
    Datas=""
    datapath = re.compile(r"lib.+py").sub(r"data%s%s" % (os.sep, "Public"), r"%s" % __file__)
    for dirnow, dirs, files in os.walk(datapath):
        for file in files:
            Datas += "\n{0}{2}{1}".format(dirnow, file, os.sep)

    datapath = re.compile(r"lib.+py").sub(r"data%s%s" % (os.sep, Suite.area), r"%s" % __file__)
    for dirnow, dirs, files in os.walk(datapath):
        for file in files:
            Datas += "\n{0}{2}{1}".format(dirnow, file, os.sep)

    Datas=re.compile(r"/|\\").sub(r"/", r"%s" % Datas)

    def todict(self, file):
        file = re.compile(r"/|\\").sub("/", file)
        paths = re.findall(r".+?%s.*" % (file), self.__class__.Datas)
        if len(paths) > 1:
            path=[i for i in paths if Suite.area in i][0]
        elif len(paths) == 1:
            path=paths[0]
        if not os.path.exists(path):
            path = re.findall(r".+?%s.*%s.*" % ("Public", file), self.__class__.Datas)[0]

        cfg = configparser.ConfigParser()
        cfg.read(path, encoding="utf-8")
        file_dict = {secstion: [eval(cfg.get(secstion, option)) for option in cfg.options(secstion)] for secstion in cfg.sections()}
        return file_dict

    @staticmethod
    def out(file, sec=None):
        obj=Get()
        file_dict = obj.todict(file)
        out_dict = {}
        if "parent" in file_dict:
            parent_file = file_dict["parent"]
            for i in parent_file:
                    out_dict = dict(out_dict, **obj.todict(i))

        out_dict = dict(out_dict, **file_dict)
        if sec == None:

            return out_dict
        elif sec and type(sec) == str:
            return out_dict[sec]

        elif len(sec) >= 2 and type(sec) == tuple:
            """多参数排列组合"""
            all=[]
            for s in sec:
                if not all:
                    all=out_dict[s]
                elif all:
                    temp=[]
                    for x in out_dict[s]:
                        for y in all:
                            t=dict(x,**y)
                            temp.append(t)
                    all = temp
            return all

class Get():
    area = Suite.area
    c = eval(area)
    name = [n for n in dir(c) if not n.startswith("__")]
    menupath = []
    for x in name:
        classname = eval("""{0}.{1}""".format(area, x))
        classlist = [n for n in dir(classname) if not n.startswith("__")]
        for y in classlist:
            menupath.append("%s.%s.%s" % (area, x, y))
    menupath = "#".join(menupath)

    inexecution_case = set()
    for i in ["day", "week", "month", "year"]:
        if not getattr(Suite, i, None):
            inexecution_case.add("test_%s" % i)

    @classmethod
    def todict(cls, file="cHannellive.ini", sec="Channel"):
        file = file.split(".")[0].capitalize()
        sec = sec.split(".")[0].capitalize()
        case_moudle = re.compile(r"[^#]+%s" % ("%s" % file), flags=re.I).findall(cls.menupath)[0]
        case_class = eval("%s.%s" % (case_moudle, sec))
        case_list = {n for n in dir(case_class) if not n.startswith("__")}
        case_list = case_list.difference(cls.inexecution_case)
        case_values = [eval("""%s.%s.%s""" % (case_moudle, sec, v)) for v in case_list]

        return case_values

    @classmethod
    def out(cls, file, sec=None):
        if sec == None:
            pass
        elif sec and type(sec) == str:
            """获取单个"""
            return cls.todict(file, sec)

        elif len(sec) >= 2 and type(sec) == tuple:
            """多参数排列组合"""
            all = []
            for s in sec:
                if not cls.todict(file,s):
                    """去除无参数的节点"""
                    return []

                if not all:
                    all = cls.todict(file, s)
                elif all:
                    temp = []
                    for x in cls.todict(file,s):
                        for y in all:
                            """轮询合并"""
                            t = dict(x, **y)
                            temp.append(t)
                    all = temp
            return all





def sendmail():

    msg_from = '869403472@qq.com'
    passwd = "fouenezecrbdbehc"
    # msg_from = '18682292896@163.com'
    # passwd = "luxu123456"
    msg_to = ["",""][1]

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = "鲁旭"
    message['To'] = "me"
    message['Subject'] = '测试报告'
    message["CC"] = '123'

    # 邮件正文内容
    text=MIMEText('冒烟测试1个失败，请重新发包', 'plain', 'utf-8')
    message.attach(text)

    # 构造附件1，传送 test.html 文件
    abs_tsethtml = os.path.abspath(__file__)
    dirname = abs_tsethtml.replace(os.path.basename(abs_tsethtml), "")
    repor_tgname = dirname + "/../report/test.html"
    att1 = MIMEText(open(repor_tgname, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    multipart_name='attachment; filename="TestReport.html"'
    att1["Content-Disposition"] = multipart_name
    message.attach(att1)



    try:
        w163=("smtp.163.com", 465)
        qq=("smtp.qq.com", 465)
        s = smtplib.SMTP_SSL(*w163)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, message.as_string())
        print("send  success")
    except :
        print("Error: 无法发送邮件")
    finally:
        s.quit()

def db_oracle(sql, database=CO.url):

    os.environ["NLS_LANG"] = "SIMPLIFIED CHINESE_CHINA.UTF8"
    sql_header = sql.split(" ")[0].lower()
    sql = r"%s" % sql
    try:
        connect = cx_Oracle.connect(database)
    except Exception as e:
        log().error(e)
    else:
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            log().error(e)
        else:
            if sql_header.startswith("select"):
                result = cursor.fetchall()
                if result == []:
                    result = [[""]]
                return result
            else:
                connect.commit()
        finally:
            cursor.close()
            connect.close()

def db_mysql(sql, host=C.host, dbcontent="content", dbport=3306, dbuser="root", dbpasswd="111111"):
    """
    #操作mysql
    :param sql:
    :return:
    """
    sql_header = sql.split(" ")[0].lower()
    sql = r"%s" % sql
    try:
        connect = pymysql.connect(host=host, user=dbuser, passwd=dbpasswd, db=dbcontent,
                                  port=dbport)
    except Exception as e:
        log().error(e)
        return "connect error"
    else:
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            if sql_header.startswith("select"):
                fetch = cursor.fetchall()
                return fetch
            else:
                connect.commit()
        except Exception as e:
            log().error(e)
            fetch = [[""]]
            return fetch
        finally:
            cursor.close()
            connect.close()

class Mythreading(threading.Thread):
    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target:
                self.result=self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def get_result(self):
        try:
            return self.result
        except:
            return None


def writexlsx(filename,data):
    sheetname="无数据汇总"
    wb = xlwt.Workbook()
    sheet = wb.add_sheet(sheetname)  # sheet的名称为test

    # 单元格的格式
    # style = 'pattern: pattern solid, fore_colour yellow; '  # 背景颜色为黄色
    # style += 'font: bold on; '  # 粗体字
    # style += 'align: horz centre, vert center; '  # 居中
    # header_style = xlwt.easyxf(style)
    datas = data
    for col in range(len(datas)):
        for row in range(len(datas[col])):
            sheet.write(col,row, datas[col][row])
    wb.save(filename)




def parserxlsx(file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    sheet_name = sheet.name
    sheet_nrows = sheet.nrows
    sheet_ncols = sheet.ncols

    # row_1 = sheet.row_values(0) #第一行
    # col_1 = sheet.col_values(0) #第一列
    all = [sheet.row_values(m) for m in range(0, sheet_nrows)]
    if not all:
        all=[[]]
    return all

class POST( hs.CGIHTTPRequestHandler, hs.BaseHTTPRequestHandler ):
    def do_GET(self):
        self.protocal_version = "HTTP / 1.1"
        self.send_response( 205 )
        self.send_header( "Welcome", "Contect" )
        self.end_headers()

    def do_POST(self):
        """Server method"""
        self.send_response( 201, {"a": "b"} )
        print( "Receiving new data ..." )
        content_length = int( self.headers['Content-Length'] )
        post_data = self.rfile.read( content_length )
        print(post_data)
        self.end_headers()
        addres = self.address_string()
        print( addres )

    @staticmethod
    def main():
        server = hs.HTTPServer(("127.0.0.1", 8000), POST).serve_forever()

class RTime():

    def retime(self):
        localtime=time.localtime(time.time())

        print(localtime)




class CreatReportXlsx:

    @classmethod
    def creatReportXlsx(cls,input):

        r"D:\Script\BI6.0.6_BI_PORTAL_003_version_6_综合\report\index.log"
        p=r"%s\report\%s.log" % (backage,input)
        fp = open(p, mode="r", encoding="utf-8")
        s = fp.readlines()
        s="".join(s[-10000:])

        res = re.compile(r"(Pass|Fail|Error)\s+test_(.+?)\s*\(test_case\.bi\.(.+?)\.case(.+?)\.Test(.+?)\)").findall(s)
        new=list()
        count_case=[0,0,0]
        for i in res:
            temp = i[2:]+i[1:2]+i[0:1]
            temp = list(temp)
            if temp[-1] == "Pass":
                temp = temp +["1", "0", "0"]
                count_case[0]+=1
            elif temp[-1] =="Fail":
                temp = temp +["0", "1", "0"]
                count_case[1] += 1
            elif temp[-1] =="Error":
                temp = temp + ["0", "0", "1"]
                count_case[2] += 1
            new.append("##".join(temp))
        new.sort()
        new=[i.split("##") for i in new]
        new.insert(0, ["页面一级菜单", "页面二级菜单", "测试项", "测试项", "测试结果", "通过", "失败", "错误"])
        new.append(["合计", sum(count_case), "", "", "", ] + count_case)
        return new

    @classmethod
    def write(cls,input,outxlsx_path="测试报告.xls"):

        workbook = xlwt.Workbook()  # Create workbook
        worksheet = workbook.add_sheet('My sheet')

        pattern_yellow = xlwt.Pattern()  # Create the pattern
        pattern_yellow.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern_yellow.pattern_fore_colour = 5  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
        style_yellow = xlwt.XFStyle()  # Create the pattern
        style_yellow.pattern = pattern_yellow  # Add pattern to style

        pattern_green = xlwt.Pattern()
        pattern_green.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern_green.pattern_fore_colour = 3
        style_Green = xlwt.XFStyle()  # Create the pattern
        style_Green.pattern = pattern_green  # Add pattern to style

        pattern_red = xlwt.Pattern()
        pattern_red.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern_red.pattern_fore_colour = 2
        style_Red = xlwt.XFStyle()  # Create the pattern
        style_Red.pattern = pattern_red  # Add pattern to style

        clor={"Pass":style_Green,"Fail":style_Red,"Error":style_yellow}

        datas=cls.creatReportXlsx(input)

        row_count = len(datas)
        for row in range(0, row_count):
            col_count = len(datas[row])
            for col in range(0, col_count):
                if 4<=col<=7:  # 设置表头单元格的格式
                    if datas[row][-4] in clor.keys():
                        worksheet.write(row, col, datas[row][col],clor[datas[row][-4]])
                    else:
                        worksheet.write(row, col, datas[row][col], )
                else:  # 表头下面的数据格式
                    worksheet.write(row, col, datas[row][col],)


        # worksheet.write(2, 5, 'Cell contents', style_Red)
        r'D:\Script\BI6.0.6_BI_PORTAL_003_version_6_综合\report\测试告.xls'
        outxlsx_path = r"%s\report\%s" %(backage,outxlsx_path)
        workbook.save(outxlsx_path)

    @classmethod
    def write1(cls,text):
        outpath=r"%s\report\前后端数据.txt" % backage
        with open(outpath, encoding="utf-8", mode="a") as fp:
            fp.write(text)

    @classmethod
    def search_ui_api(cls):
        logpath = r"%s\report\logs.log" % backage
        fp = open(logpath, encoding="utf-8")
        for i in fp:
            if "result subject data is" in i:
                ra = re.compile(r"(\[Test.+?\.test.+?\]).+?result subject data is(.+?)\n").findall(i)
                if ra:
                    ravalue = ra[0][1].strip()
                    ravalue = eval(ravalue)
                    print(ra)
                    if ravalue:
                        ra1 = " %s api  %s\n" % (ra[0][0], [[x for x in i.values()] for i in ravalue if i != None])
                    else:
                        ra1 = " %s api  %s\n" % (ra[0][0], ravalue)
                    print(ra1)
                    cls.write1(ra1)
                    continue
            if "table content is" in i:
                rw = re.compile(r"(\[Test.+?\.test.+?\]).+?table content is(.+?)\n").findall(i)

                if rw:
                    rw1 = " %s web %s\n" % (rw[0][0], rw[0][1])
                    print(rw1)
                    cls.write1(rw1)
                    continue
        fp.close()


if __name__ == "__main__":

    # x=1
    # a=db_oracle("select * from  CATEGORYMAP;", r"credb/oss@10.50.108.17:1521/ORCL")
    # print(a)

    p=Get.out("UserSurvey", ("time", "viewtable"))
    print(p)