"""
    author:Shuai Guo
    tool:pycharm
"""
from dbfiles.dataobject.Table import Table
from abc import ABCMeta,abstractmethod


class Index(metaclass=ABCMeta):
    def __init__(self,index_name:str,table:Table,column:str):
        """
        :param index_name: 索引的名称
        :param table: 索引的关联表
        :param column: 基于哪个列建立的索引
        """
        self.__index_name = index_name
        self.__table_name = table.table_name
        self.__column = column

    @property
    @abstractmethod
    def index_type(self) -> str:
        pass

    @property
    def index_name(self)->str:
        return self.__index_name

    @property
    def table_name(self)->str:
        return self.__table_name

    @property
    def column(self)->str:
        return self.__column

    @abstractmethod
    def insert(self)->bool:
        pass

    @abstractmethod
    def delete(self,key:object)->bool:
        pass

    @abstractmethod
    def update(self)->bool:
        pass

    @abstractmethod
    def search(self) -> bool:
        pass

    def __str__(self):
        return f"名字：{self.index_name},关联表名：{self.table_name}，列名：{self.column}"