"""
    author:Shuai Guo
    tool:pycharm
"""
from dbfiles.dataobject.Table import Table

class View():
    def __init__(self,view_name:str,table:Table,columns:list,define_items:list):
        """

        :param view_name: 视图名
        :param table: 基表名
        :param columns: 列数
        :param define_items:视图定义查询语句
        """
        self.__view_name = view_name
        self.__table = table
        self.__columns = columns
        self.__define_items = define_items

    @property
    def view_name(self)->str:
        return self.__view_name


    @property
    def columns(self) -> list:
        return self.__columns


    #  返回视图定义的查询语句
    @property
    def define_items(self)-> list :
        return self.__define_items



