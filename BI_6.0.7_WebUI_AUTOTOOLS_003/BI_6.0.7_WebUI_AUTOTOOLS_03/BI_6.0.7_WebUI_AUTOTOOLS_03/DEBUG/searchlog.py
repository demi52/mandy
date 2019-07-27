
import re

def write1(text):
    outpath = r"D:\Script\BI_6.0.7_WebUI_AUTOTOOLS_02\report\out.log"
    with    open(outpath,encoding="utf-8",mode="a") as fp:
        fp.write(text)

def search_ui_api():
    logpath=r"D:\Script\BI_6.0.7_WebUI_AUTOTOOLS_02\report\logs.log"

    fp=open(logpath, encoding="utf-8")
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
                write1(ra1)
                continue
        if "table content is" in i:
            rw = re.compile(r"(\[Test.+?\.test.+?\]).+?table content is(.+?)\n").findall(i)

            if rw:
                rw1=" %s web %s\n" % (rw[0][0], rw[0][1])
                print(rw1)
                write1(rw1)
                continue
    fp.close()

search_ui_api()