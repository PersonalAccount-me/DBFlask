"""
    author:Shuai Guo
    tool:pycharm
"""

from abc import abstractmethod,ABCMeta
from dbfiles.dataobject.Table import Table
from dbfiles.baseclass.Index import Index
from dbfiles.dataobject.View import View



class IDefinable(metaclass=ABCMeta):
    @abstractmethod
    def create_table(self,table_name:str,primary_key:str or tuple,column_units:list):
        pass

    @abstractmethod
    def create_index(self,table_name:str,column:str):
        pass

    @abstractmethod
    def create_view(self,table_name:str,columns:list):
        pass

    @abstractmethod
    def drop_table(self,table_name:str):
        pass

    @abstractmethod
    def drop_index(self,index_name:str):
        pass

    @abstractmethod
    def drop_view(self,view_name:str):
        pass


class IQueryable(metaclass=ABCMeta):

    @abstractmethod
    def get_table(self, table_name: str) -> Table:
        pass

    @abstractmethod
    def get_index(self, index_name: str) -> Index:
        pass

    @abstractmethod
    def get_view(self, view_name: str)->View:
        pass

    @abstractmethod
    def single_condition_query(self,table:Table,query_items:list)->list:
        """
        单表选择查询
        :param table: 表名
        :param condition1:条件一
        :param conditions: 更多条件
        :return: 查询到的记录列表
        """
        pass

    @abstractmethod
    def multiple_connect_query(selfself,table1:Table,table2:Table,query_items:list)->list:
        """
        多表连接查询
        :param values1: 表一
        :param values2: 表二
        :param condition1: 条件一
        :param contions: 更多条件
        :return:查询到的记录列表
        """
        pass

    @abstractmethod
    def nested_query(self,values:list)->list:
        #待定
        pass

    @abstractmethod
    def materialize_view(self,view:View) -> Table:
        pass


class IManipulate(metaclass=ABCMeta):

    @abstractmethod
    def insert_record(self) -> bool:
        pass

    @abstractmethod
    def update_record(self) -> bool:
        pass

    @abstractmethod
    def delete_record(self) -> bool:
        pass

class ISQL(IDefinable,IManipulate,IQueryable):
    pass