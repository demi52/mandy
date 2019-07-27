
def excute(status=True):
    def kk(func):
        def testfuncs(*args,**kwargs):
            return func(*args,**kwargs)
        return testfuncs
    return kk


class M:

    @excute()
    @excute()
    @excute()
    @staticmethod
    def a(self):
        pass
print(M.a.__name__)