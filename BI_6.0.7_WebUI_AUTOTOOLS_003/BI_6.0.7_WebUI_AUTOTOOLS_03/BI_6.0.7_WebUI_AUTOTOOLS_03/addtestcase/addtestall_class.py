#author='鲁旭'
"""
动态控制用例执行
"""
import os
import re
import importlib
import unittest
from config.conf import Suite as s


def case_list(case_dir=s.case_dir, suite_dir=s.suite_dir,rmdir=s.remove_dirs,only=s.only_dirs):

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

    onleydirs=[]
    for i in only:
        """获取仅执行的用例"""
        i = re.compile(r"\\|/").sub("\.", i)
        if i not in ("", "*", "\w") and i != ".":
            modles = re.compile(r".+?%s\..*?%s.*?py" % (case_dir, i), re.I).findall(test_case_modle)
            onleydirs += modles
    test_case_modle = "\n"+"\n".join(set(onleydirs))
    for i in rmdir:
        """去除不执行的用例"""
        i = re.compile(r"\\|/").sub("\.", i)
        if i not in ("",  "*", "\w") and i != ".":
            test_case_modle = re.compile(r".+?%s\..*?%s.*?py" % (case_dir, i), re.I).sub("", test_case_modle)

    if s.onlyC3:
            test_case_modle = re.compile(r".+?%s\..*?%s.*?py" % (case_dir, "C3"), re.I).findall(test_case_modle)
            test_case_modle="\n".join(test_case_modle)

    pat2 = r"%s.+?(?=\.py)" % (case_dir,)
    test_case_modle_list = re.findall(pat2, test_case_modle)
    return test_case_modle_list


def suite(**kwargs):
    """
    添加用例目录树下，所有用例
    :param casedir: 用例目录
    :param suite_dir:当前文件的上级目录
    :return:
    """
    suites = unittest.TestSuite()
    loader = unittest.TestLoader()
    test_case_script_list = case_list(**kwargs)

    #获取所有测试用例脚本文件
    if test_case_script_list:
        for test_case_name in test_case_script_list:
            modle_name = importlib.import_module(test_case_name)
            test_class_list=[c for c in dir(modle_name) if c.startswith("Test")]
            for test_class_name in test_class_list:
                if "详情" in test_class_name and not s.detail:
                    continue
                suites.addTest(loader.loadTestsFromTestCase(eval("modle_name.%s" % (test_class_name))))
    return suites









