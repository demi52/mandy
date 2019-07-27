#author='鲁旭'
"""
默认执行test_case 目录下的所有用例，可根据配置过滤

"""
import os
import re
import importlib
import unittest
from config.conf import Suite as s


def case_list(case_dir=s.case_dir, suite_dir=s.suite_dir):

    """
    获取待执行的目录下的所有测试用例脚本
    :param casedir: 测试用例所在目录
    :param suite_dir: 测试套件所在的目录
    :return: 返回所有测试用例脚本名列表
    """
    pat = r"%s.+?py" % suite_dir
    root_path = re.compile(pat).sub("", os.path.realpath(__file__))
    case_path = "%s%s" % (root_path, case_dir)

    test_case_modle = ""
    for dirnow, dirs, files in os.walk(case_path):
        for file in files:
            if file.endswith("py") and file != "__init__.py":
                test_case_modle += "\n%s/%s" % (dirnow, file)
    test_case_modle = re.compile(r"\\|/").sub(".", test_case_modle)
    for i in s.remove_dirs:
        i = re.compile(r"\\|/").sub("\.", i)
        if i not in ("",  "*") and i != ".":
            test_case_modle=re.compile(r".+?%s\..*?%s\..*?py" % (case_dir, i)).sub("", test_case_modle)
        if i == "C3":
            test_case_modle = re.compile(r".+?%s\..*?%s.*?py" % (case_dir, i) ).sub("", test_case_modle)

    pat2 = r"%s.+?(?=\.py)" % (case_dir)
    test_case_modle_list = re.findall(pat2, test_case_modle)
    # print(test_case_modle_list)
    return test_case_modle_list



def suite(**kwargs):

    """
    添加用例目录树下，所有用例
    :param casedir: 用例目录
    :param suite_dir:当前文件的上级目录
    :return:
    """
    suites = unittest.TestSuite()
    test_case_script_list = case_list(**kwargs)

    #获取所有测试用例脚本文件
    if test_case_script_list:
        for test_case_name in test_case_script_list:
            modle_name = importlib.import_module(test_case_name)
            test_class_list=[ c  for c in dir(modle_name) if c.startswith("Test")]

            #获取当前用例脚本下的所有测试类
            if test_class_list:
                for test_class_name in test_class_list:
                    test_func_list = [f for f in dir(eval("modle_name.%s" % test_class_name)) if f.startswith("test_")]

                    #获取当前模块下，该测试类下的，所有测试函数
                    if test_func_list:
                        for test_func_name in test_func_list:
                            #添加测试函数
                            suites.addTest(eval("modle_name.%s('%s')" % (test_class_name, test_func_name)))
    return suites


if __name__ == "__main__":
    sui=suite()
    [print( i) for i in list(iter(sui))]
    print(len(list(iter(sui))))





