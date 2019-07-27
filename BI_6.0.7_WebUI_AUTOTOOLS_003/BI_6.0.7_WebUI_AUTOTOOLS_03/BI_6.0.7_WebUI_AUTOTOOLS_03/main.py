__autor__ = "鲁旭"

import time
import os
import sys
from lib.driver import InitTest
from addtestcase.addtestall_class import suite

def run():

    report_name = "index"
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(path)
    os.chdir(path)
    InitTest.active(suite, report_name=report_name)
    InitTest.end()
    InitTest.write(report_name)
    InitTest.search_ui_api()

if __name__ == "__main__":
    run()
