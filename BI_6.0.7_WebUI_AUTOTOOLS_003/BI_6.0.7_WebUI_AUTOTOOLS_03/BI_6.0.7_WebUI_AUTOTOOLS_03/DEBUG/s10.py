#
# from multiprocessing import Process
# def run():
#     pass
#
# if __name__ == '__main__':
#     p=Process(target=run)
#     if  isinstance(p,Process):
#         print(1111111111)
#     print(p.is_alive())


def a():
    return 1,2,3
x,y,z=a()
print(x,y,z)