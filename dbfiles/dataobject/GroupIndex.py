"""
    author:Shuai Guo
    tool:pycharm
"""
from dbfiles.baseclass.Index import Index
from dbfiles.dataobject.Table import Table


class GroupUnit:
    def __init__(self):
        self.key = None
        self.data = []

    def __str__(self)->str:
        return f"{self.key}:{self.data}"

class GroupIndex(Index):
    def __init__(self,index_name:str,table:Table,column:str,distinct_num:int):
        super().__init__(index_name,table,column)
        self.group_units = [GroupUnit() for i in range(0,2*distinct_num)]  #   创建一个表长为不重复元素数目的两倍的数组
        self.unit_number = distinct_num
        self.key_addr_mapping = {}
        self.pointer = -1

        if bool(table.data):
            for i in range(0,len(table.data)):
                self.insert(table.data[i][column],i)

    @property
    def index_type(self) -> str:
        return "GroupINdex"

    def insert(self,key:object,i:int) -> bool:
        if self.key_addr_mapping.get(key,-1) == -1:
            self.pointer = (self.pointer+1)%self.unit_number
            self.key_addr_mapping.setdefault(key,self.pointer)
            self.group_units[self.pointer].key = key
            self.group_units[self.pointer].data.append(i)
            return True
        else:
            addr = self.key_addr_mapping.get(key)
            self.group_units[addr].data.append(i)

    def delete(self, key: object) -> bool:
        addr = self.key_addr_mapping.get(key,-1)
        if addr == -1:
            return False
        self.group_units[addr].key = None  #  重置键
        self.group_units[addr].data.clear()  #  清除所有数据
        return True

    def update(self) -> bool:
        pass

    def search(self,key:object) -> list:
        addr = self.key_addr_mapping.get(key,-1)
        if addr == -1:
            return []
        return self.group_units[addr].data