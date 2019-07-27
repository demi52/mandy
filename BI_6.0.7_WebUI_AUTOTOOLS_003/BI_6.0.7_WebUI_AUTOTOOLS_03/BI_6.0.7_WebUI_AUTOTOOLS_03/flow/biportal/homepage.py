"""
首页概况
"""
from flow.biportal.base import Base ,Base实时数据

__autor__ = "鲁旭"

class HomePage(Base,Base实时数据):

    Pararm = \
        {
            "开机率": {"table_id": "peruserCount", "tabletype": "count_user"},
            "在线用户数": {"table_id": "onlineUserCount", "tabletype": "count_user"},
            "全网用户数": {"table_id": "allUserCount", "tabletype": "count_user"},
            "曲线图": {"table_id": "people", "tabletype": "count_user"},
        }

    def _first(self, **kwargs):
       super()._first()
       self.frame_change(-1)

    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "开机率")
        self.table_id = self.Pararm[self.buttontext].get("table_id")
        self.apiqdi = "queryuserarea"
        self.tabletype = self.Pararm[self.buttontext].get("tabletype")
        self.text = ""
        self.down_text = {"by": "id", "value": self.table_id}

    def f_search(self, **kwargs):
        """
        查询流程
        :param :
        :return
        """
        self.pararms(**kwargs)
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.move_detaildata()
        self.get_data()



if __name__ == "__main__":
    pass