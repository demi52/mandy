import xlrd


def parserxlsx(file):
    book = xlrd.open_workbook(file)
    t=[]
    tag=["订购分析","结算数据","手机","专题分析","自定义报告","数据维护","用户","数据字典"]
    b=3233
    for s in tag:
        # print(s)
        sheet1=book.sheet_by_name(s)
        ncols_总列数 = sheet1.ncols
        # print( u'表格总列数 ', ncols_总列数)
        for n in range(0, ncols_总列数):
            col3_values = sheet1.col_values(n)
            # c3=[i.strip() for i in col3_values if i ]
            cache=[]
            if col3_values[0]:
                nc=col3_values[0].split("-")
            for t2 in col3_values[1:]:
                    if t2:
                        if "Headline" in t2:
                            cache_list=["{:0>4d}".format(b),nc[0],nc[1].strip(),t2.strip()]
                            t.append(cache_list)
                            b+=1
            # print('第%s列值 ' % n, len(c3), c3)
            # t=t+c3
    return t
x=parserxlsx(r"D:\case.xlsx")
for i in x:
        print(i)
print(len(x))