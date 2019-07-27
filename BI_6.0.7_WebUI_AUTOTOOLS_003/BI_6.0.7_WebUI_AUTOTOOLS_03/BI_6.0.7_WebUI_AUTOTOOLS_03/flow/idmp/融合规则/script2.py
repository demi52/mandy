__author__ = "luxu"

"""flow\idpcs\融合规则\script.py  融合规则流程,获取C3数据  """
import re
import time
import requests
from config.conf import Idpcs
from lib.funcslib import log, db_oracle
from lib.listen import ListenServerLog as LS

class Medial(object):

    def __init__(self, rule=""):
        """
        :param rule: 匹配规则 tuple or list  , sample: [("YEAR", "2"),]
        :param timeout: int
        :return:
        """
        log().info("%s start %s" % (" " * 60, " " * 60))
        # 1、定义实例参数
        self.rule = rule

        self.code = Idpcs.code
        self.idpclogpath = Idpcs.idpcs_path
        self.status = "start"
        self.value = ['2018', '陈奕利,韩立', '刘烨,姚晨,陈冲,王喜,青元子', '懒猫，兔子', "5.1", '喜剧,仙侠，少儿', '宁财神,,,', '鸟语']
        self.keys = ['YEAR', 'DIRECTORS', 'CASTS', 'TITLE', 'RATING', 'GENRES', 'WRITERS', 'LANGUAGES']

    def check_c2(self):
        """
        环境校验
        :return:
        """
        strcode = str(self.code).replace("[", "").replace("]", "")
        sql = "select count(*) from WS_MERGEDMEDIA where c2code in ({0})".format(strcode)
        num_MERGEDMEDIA_ = db_oracle(sql)[0][0]
        if num_MERGEDMEDIA_ != len(self.code):
            raise AssertionError("not found %s  in WS_MERGEDMEDIA " % self.code)

        sql = "select count(*) from WS_PROCESS where code in ({0})".format(strcode)
        num_WS_PROCESS_ = db_oracle(sql)[0][0]
        if num_WS_PROCESS_ != len(self.code):
            raise AssertionError("not found %s  in WS_PROCESS " % self.code)

    def _getidfromlog(self):
        with open(self.idpclogpath) as fp:
            strings = fp.read()
        patt = r"(?<=there outside id is: )\w+"
        list_id = re.compile(patt).findall(strings)
        return list_id

    def initialize(self):
        """
        初始化
        1、清空日志
        2、初始化媒资数据
        3、初始化匹配规则表
        """

        #1、获取最初的融合的id
        LS().idpcs_get_id("start")
        #2、初始化c2数据
        for i in self.code:
            sql = "update WS_MERGEDMEDIA set YEAR='{0}', DIRECTORS='{1}', " \
                  "CASTS='{2}', TITLE='{3}', RATING='{4}',GENRES='{5}', WRITERS='{6}',  LANGUAGES='{7}' where c2code='%s'".format(
                *self.value) % i
            db_oracle(sql)
            log().debug("初始化 WS_MERGEDMEDIA表,sql: %s" % sql)

        #3、初始化ws_rule
        sql="DELETE from WS_RULE"
        db_oracle(sql)
        log().debug("clean ws_rule end :sql='%s'" % sql)

    def set_rule(self):
        """设置待匹配的字段，规则"""

        for i in self.rule:
            sql_init = "INSERT INTO WS_RULE VALUES('%d','%s','%s','%s')" % (self.rule.index(i), i[0], i[0], i[1])
            log().debug(sql_init)
            db_oracle(sql_init)

    def get_rules(self):
        """获取待匹配字段，以及规则"""
        sql="SELECT PROPERTY, RULE from WS_RULE"
        getrule=db_oracle(sql)
        log().debug("get rule is %s  send  is %s"%(getrule,self.rule))
        if set(getrule) == set(self.rule):
            self.rule = {x: y for x,y in getrule if x in self.keys}
            self.keys = [i for i in self.rule.keys()]
            log().debug(self.rule)
        elif set(getrule) != set(self.rule):
            log().error("ws_rule getrul != rule test end")
            raise AssertionError("ws_rule getrul != rule test end")

    def _creat_sql(self, other):
        """内部方法"""
        list_k = self.keys
        numbers = "%s" + ", %s" * int(len(list_k) - 1)
        s = ",".join(["list_k[%d]" % i for i in range(0, len(list_k))])
        sql_header = "select %s   %s" % (numbers, other)
        sql = '"%s"%s(%s)' % (sql_header, "%",  s,)
        sql = (eval(sql))
        return sql

    def get_id(self):
        """获取中间表id"""
        if self.status == "stop":
            log().debug("开获取融合ID")

            memgr_id=LS.idpcs_get_id("end")
            if memgr_id != len(self.code):
                raise AssertionError("融合的C3数据条数为 %s，少于总媒资数据条数 %s" % (memgr_id, len(self.code)))
            log().debug("id_code : %s" % memgr_id)
            self.id_code={}
            for i in memgr_id:
                sql="select  c2code, id from WS_PROCESSDETAIL where  id='%s'" %(i)
                r=db_oracle(sql)
                self.id_code[r[0][0]]=r[0][1]


    def search_start(self):
        """融合前查询媒资表"""
        result={}
        for i in self.code:
            WS_MERGEDMEDIA = self._creat_sql(", c2code  from WS_MERGEDMEDIA where c2code='%s'" % i)
            log().debug(WS_MERGEDMEDIA)
            mer = db_oracle(WS_MERGEDMEDIA)
            result[i] = {}
            result[i] = {self.keys[i]: mer[0][i] for i in range(0, len(self.keys)) if mer}
            if not result[i]:
                raise AssertionError("code %s not data in table WS_MERGEDMEDIA" % i)
            log().debug("%s---start--- WS_MERGEDMEDIA %s" % (i, result))
        exec("self.start=result" )

    def activity(self, s):
        """更改ws_process表，触发融合操作"""

        for i in self.code:
            sql="update WS_PROCESS set PROCESSRESULT='%s' where code='%s'" % (s,i)
            db_oracle(sql)
            log().debug([i, db_oracle("select PROCESSRESULT from WS_PROCESS where code='%s' " % i)])
        self.status = "stop"

    def merge_wait(self , timeout=20):
        strcode = str(self.code).replace("[", "").replace("]", "")
        number=0
        sql = "SELECT count(*) from WS_PROCESS where  PROCESSRESULT='2' and  CODE in ({0})".format(strcode)
        log().debug(sql)
        while True:
            rescount=db_oracle(sql)[0][0]
            log().debug("merge over is %s" % rescount)
            if rescount == len(self.code):
                break
            elif number == timeout:
                raise AssertionError("timeout = %s 超时未融合完毕 测试结束" % timeout)
            number += 1
            time.sleep(1)

    def search_stop(self):
        """
        融合后查询数据库,生成字典
        :return:
        """
        self.toals={}
        for i in self.code:
            if self.id_code.get(i, False):
                self.code_element=i
                WS_OUTSIDE = self._creat_sql(", id from WS_OUTSIDE where id='%s'" % self.id_code[i])
                out=db_oracle(WS_OUTSIDE)
                text = " %s  %s WS_OUTSIDE is %s " % (self.status, i, out)
                log().debug(text)

                self.outside = {self.keys[i]: out[0][i] for i in range(0, len(self.keys))}
                log().debug("%s WS_OUTSIDE %s"%(i,self.outside ) )

                WS_MERGEDMEDIA = self._creat_sql(", c2code  from WS_MERGEDMEDIA where c2code='%s'" % i)
                mer = db_oracle(WS_MERGEDMEDIA)
                self.stop = {self.keys[i]: mer[0][i] for i in range(0, len(self.keys))}
                log().debug("%s WS_MERGEDMEDIA %s"%(i,self.stop) )

                self._data()
                self.toals[i]=self.toal
        log().info(self.toals)

    def _data(self):
        """内部方法，相同字段处理"""

        c2 = self.start
        c3 = self.outside
        new =self.stop

        toal = {}
        for k in self.keys:
            toal[k] = {}
            toal[k]["c2"] = c2[self.code_element][k]
            toal[k]["c3"] = c3[k]
            toal[k]["New"] = new[k]

        log().debug(["code=%s" % self.code_element, toal])
        self.toal=toal

    def dujde_c2(self):
        """数据比对"""
        code_pass = 0
        if len(self.toals) == len(self.code):
            for code in self.code:
                key_pass = 0
                for key in self.keys:
                    c2 = self.toals[code][key]["c2"]
                    c3 = self.toals[code][key]["c3"]
                    new = self.toals[code][key]["New"]
                    rule = self.rule[key]
                    if rule == "1":
                        """c2为准"""
                        if c2 == new:
                            key_pass += 1
                        else:
                            log().error("%s_%s fail " % (code, key))
                    elif rule == "2":
                        """c3为准"""
                        if c3 == new:
                            key_pass += 1
                        else:
                            log().error("%s_%s fail " % (code, key))
                    elif rule == "3":
                        """融合"""
                        if c2 != None and c3 != None and new != None:
                            set_c2 = set(re.compile(r"[,，]").split(c2))
                            set_c3 = set(re.compile(r"[,，]").split(c3))
                            set_new = set(re.compile(r"[,，]").split(new))
                            if set_new == set_c2 | set_c3:
                                key_pass += 1
                            else:
                                log().error("%s_%s fail " % (code, key))

                        elif None == c2 or None == c3 or None == new:
                            if new == c2 or new == c3:
                                key_pass += 1

                if key_pass == len(self.keys):
                    code_pass += 1
                elif key_pass != len(self.keys):
                    log().error("code:%s test fail ,pass key is %s  all key is %s" % (code,key_pass,len(self.keys)))
            if code_pass == len(self.code):
                self.status = "pass"

            else:
                self.status = "fail"
                log().error(" test fail ,  pass code is %s  all code is %s" % (len(self.toals), len(self.code)))

        else:
            log().error(" test fail ,  pass code is %s  all code is %s" % (len(self.toals), len(self.code)))
            self.status = "fail"

    def execute_c2(self ):
        """
        1、设置参数
        3、环境校验
        4、初始化
        5、设置融合规则
        6、获取融合规则
        7、查询最初始媒资数据
        8、触发融合动作
        9、获取被融合的c3数据对应的id
        10、获取融合后的媒资数据,及c3数据
        11、依据融合规则，判断融合前后的媒资数据表
        :return: pass  or flase
        """
        self.check_c2()
        self.initialize()
        self.set_rule()
        self.get_rules()
        self.search_start()
        self.activity(s="0")
        self.merge_wait()
        self.get_id()
        self.search_stop()
        self.dujde_c2()
        return self.status


class GetC3Data(Medial):

    def init(self):
        """初始化环境"""
        strcode = str(self.id_list).replace("[", "").replace("]", "")
        clean_side= "delete  WS_OUTSIDE where id in ({0})".format(strcode)
        db_oracle(clean_side)

        clean_tail = "delete  WS_PROCESSDETAIL where id in ({0})".format(strcode)
        db_oracle(clean_tail)
        log().info("clean  WS_PROCESSDETAIL and WS_OUTSIDE  sucess")

    def useapi(self,timeout=10):
        """调用实时获取第三方数据接口"""
        try:
            result=requests.get(Idpcs.urlc3, timeout=timeout*len(self.code))
        except Exception as e:
            raise AssertionError ("调用实时请求第三方数据接口失败 %s" % e)
        else:
            if result.status_code != 200:
                raise AssertionError("get C3 data fail")

    def getc3_wait(self,timeout=10):
        """等待爬取完毕，每条等待时间为  timeout*3"""
        strcode = str(self.code).replace("[", "").replace("]", "")
        number = 0
        sql = "select count(*) FROM WS_PROCESSDETAIL where SOURCE='3' and  C2CODE in ({0})".format(strcode)
        while True:
            rescount = db_oracle(sql)[0][0]
            log().debug("get over is %s" % rescount)
            if rescount >= len(self.code):
                break
            elif number == timeout*3*len(self.code):
                raise AssertionError("超时未获取C3数据 测试结束")
            number += 1
            time.sleep(1)

    def search_c3(self):
        """查询C3数据"""
        strcode = str(self.code).replace("[", "").replace("]", "")
        sql_id = "select ID FROM WS_PROCESSDETAIL where SOURCE='3' and  C2CODE in ({0})".format(strcode)
        resid = db_oracle(sql_id)
        id_list=[i[0] for i in resid]
        strid_list = str(id_list).replace("[", "").replace("]", "")
        sql_outside="SELECT count(*) from  WS_OUTSIDE where  ID in  ({0})".format(strid_list)
        res_side=db_oracle(sql=sql_outside)

        self.id_list=id_list
        self.side=res_side[0][0]
        log().info("%s WS_PROCESSDETAIL ID  have %s, WS_OUTSIDE ID have %s  " % (self.status ,self.id_list, self.side))

    def dujde(self):
        """判断"""
        if self.side==len(self.id_list):
                self.status = "pass"
        else :
            self.status = "fail"

    def execute_notc3(self):
        """
        未存在C3数据时，实时获取第三方数据流程
        1、设置参数
        2、校验环境
        3、查询垃圾数据
        4、初始化环境
        5、设置待爬去的内容
        6、调用接口，爬去
        7、查询爬取后的数据
        8、判断
        :param kwargs:
        :return:
        """
        self.check_c2()
        self.search_c3()
        self.init()
        self.activity(s="1")
        self.useapi()
        self.getc3_wait()
        self.search_c3()
        self.dujde()
        return self.status

    def execute_exitsc3(self):
        """
            已经存在C3数据时，再次实时获取第三方数据流程
            1、校验环境
            2、查询垃圾数据
            3、初始化环境
            4、设置待爬去的内容
            5、调用接口，爬去
            6、查询爬取后的数据
            7、判断
            :return:
                """
        self.execute_notc3()
        self.status = "start"
        self.activity(s="1")
        self.useapi()
        self.getc3_wait()
        self.search_c3()
        self.dujde()
        return self.status

    def execute_c2c3(self):
        """
        1、校验媒资表
        2、查询扩展数据
        3、初始化C3
        4、
        :return:
        """
        self.check_c2()
        self.search_c3()
        self.init()
        self.initialize()
        self.set_rule()
        self.get_rules()
        self.search_start()
        self.activity(s="1")
        self.useapi()
        self.getc3_wait()
        self.merge_wait()
        self.get_id()
        self.search_stop()
        self.dujde_c2()
        return self.status

if __name__ == "__main__":
    pass