import pandas as pd
from dbfiles.utilityclass.Parser import Parser
import os

"""读写文件的一个工具类"""
class FileManager:
    #  1.测试用
    # root_dir = r"C:\Users\86173\PyCharmProjects\PyOracle\MyDB\app01\views\dbfiles"

    root_dir:str = os.path.abspath(r"./dbfiles")

    @staticmethod
    def read_file(file_path:str)->list:
        """
        读取csv文件生成一个dataframe
        :param file_path:要读取的文件的路径
        :return:读取后生成的dataframe
        """
        dataframe = pd.read_csv(file_path)
        # index_col = ['序号']决定索引是否使用需要列
        return dataframe.to_dict(orient="records")

    @staticmethod
    def write_file(data:list,file_save_path:str)->None:
        """
        将dataframe写入到csv文件之中去
        :param datas:数据
        :param file_save_path:文件保存路径
        :return:无返回值
        """
        dataframe = Parser.list_to_dataframe(data)
        dataframe.to_csv(file_save_path, index=False)

    @classmethod
    def create_table_file(cls,table_name:str,columns:list):
        table_file_path = cls.root_dir + "/table/" + table_name + ".csv"
        df = pd.DataFrame(columns=columns)
        df.to_csv(table_file_path,index=False)

    @classmethod
    def drop_table_file(cls,table_name)->bool:
        table_file_path = cls.root_dir + "/table/" + table_name + ".csv"
        os.remove(table_file_path)
        return True







