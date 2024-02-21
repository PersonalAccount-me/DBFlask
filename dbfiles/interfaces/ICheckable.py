"""
    author:Shuai Guo
    tool:pycharm
"""
from abc import ABCMeta,abstractmethod
from dbfiles.dataobject.Table import Table

class ICheckable(metaclass=ABCMeta):
    @abstractmethod
    def check_entity_integrity(self,table:Table)->bool:
        pass

    @abstractmethod
    def check_refer_integrity(self,table1:Table,table2:Table,*table3:Table)->bool:
        pass

    @abstractmethod
    def is_unqiue(self,table:Table,column:str)->bool:
        pass

    @abstractmethod
    def is_null(self,table:Table,column:str)->bool:
        pass

    @abstractmethod
    def is_primary_key(self,table:Table)->bool:
        pass