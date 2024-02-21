"""
    author:Shuai Guo
    tool:pycharm
"""
import pandas as pd
from pandas import DataFrame

""" 数据格式的转换"""
class Parser:
    @staticmethod
    def dataframe_to_list(data: DataFrame,columns:list,item_type:str) -> list:
        data_list = list()
        for record in data.values:
            if item_type == "list":
                data_list.append(list(record))
            else:
                index = 0
                record_dict = dict()
                for column in columns:
                    record_dict[column] = record[index]
                    index += 1
                data_list.append(record_dict)
        return data_list


    @staticmethod
    def list_to_dataframe(data: list) -> DataFrame:
        return pd.DataFrame(data)

    @staticmethod
    def filter_specified_columns_data(data:list,columns:list)->list:
        result_data = list()
        for record in data:
            result_data.append({column:record[column] for column in columns})
        return result_data