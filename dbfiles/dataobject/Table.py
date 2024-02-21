"""
    author:Shuai Guo
    tool:pycharm
"""
import uuid

import json
def generate_key(length:int)->str:
    return uuid.uuid4().__str__()[:length]


class Table:
    def __init__(self,table_name:str,primary_key:str or tuple,column_units:list,data:list,foreign_units:list):
        """

        :param table_name: 表名
        :param primary_key: 主码
        :param columns_units: 限制条件
        :param data: 数据集，在新建表的时候不必传入，在从磁盘上加载的时候则需要传入
        """
        self.__table_name:str = table_name
        self.__primary_key:str or tuple = primary_key
        self.__column_units:list = column_units
        self.data:list = data
        self.foreign_units = foreign_units


    @property
    def table_name(self)->str:
        return self.__table_name

    @property
    def primary_key(self)->str or tuple:
        return self.__primary_key

    @property
    def columns(self)->list:
        return [columnUnit["name"] for columnUnit in self.__column_units]

    @property
    def length(self)->int:
        return len(self.data)

    def column_type(self,column:str)->str:
        for column_unit in self.__column_units:
            if column_unit["name"] == column:
                return column_unit["type"]

    def column_constraints(self,column:str)->str:
        for column_unit in self.__column_units:
            if column_unit["name"] == column:
                return column_unit["constraints"]

    def __str__(self):
        return json.dumps(self.__dict__)

    def accessible_attrs(self)->dict:
        return {
            "name":self.table_name,
            "columns":self.columns,
            "columnUnits":self.__column_units,
            "key":generate_key(16)
        }