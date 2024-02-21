"""
    author:Shuai Guo
    tool:pycharm
"""
from typing import Callable
from itertools import zip_longest
import operator
from dbfiles.baseclass.InitConfig import InitConfig
from dbfiles.interfaces.ISQL import ISQL
from dbfiles.interfaces.ICheckable import ICheckable
from dbfiles.baseclass.Index import Index
from dbfiles.dataobject.Table import Table
from dbfiles.dataobject.View import View
from dbfiles.dataobject.HashIndex import HashIndex
from dbfiles.dataobject.BSTIndex import BSTIndex
from dbfiles.dataobject.GroupIndex import GroupIndex
from dbfiles.utilityclass.FileManager import FileManager
from dbfiles.utilityclass.ArrayOperation import ArrayOperation
import traceback

def condtion_wrapper(column:str,operator:str,value:str) -> Callable:
    """

    :param column: 列名
    :param operator: 操作符
    :param value: 值
    :param key: 关键字
    :param boolSign: 布尔运算符
    :return:
    """
    def condition(value2: dict) -> bool:
        if operator == '=':
            return value == value2[column]
        elif operator == '>=':
            return value2[column] >= value
        elif operator == '>':
            return value2[column] > value
        elif operator == '<=':
            return value2[column] <= value
        elif operator == '<':
            return value2[column] < value

    return condition


class DBMS(InitConfig,ICheckable,ISQL):
    __only_instance = None  # 设置一个私有变量，默认没有被实例化

    """一个装的是Table对象，一个装的是Index对象，还有一个是View对象"""
    __tables = dict()
    __indexes = dict()
    __views = dict()

    """实现单例模式"""
    @classmethod
    def get_instance(cls):
        if cls.__only_instance == None:
            cls.__only_instance = DBMS()
        return cls.__only_instance

    def __init__(self):
        super().__init__()
        self.load_tables()
        self.load_indexes()

        self.save_config()

    """完整性检查"""
    def check_entity_integrity(self, table: Table, value:int) -> bool:
        node = table.main_index.search(value)
        return node == None

    def check_refer_integrity(self, table1: Table, table2: Table, *table3: Table) -> bool:
        pass

    def is_unqiue(self, table: Table, column: str) -> bool:
        pass

    def is_null(self, table: Table, column: str) -> bool:
        pass

    def is_primary_key(self, table: Table) -> bool:
        pass

    """实现SQL语言的操作 ISQL"""
    """单表、连接、嵌套查询 """
    def single_condition_query(self,table:Table,query_items:list) -> list:
        if len(query_items) == 0:
            print("返回全部了")
            return [i for i in range(0,table.length)]
        else:
            result_addrs = []
            for i in range(0, len(query_items)):
                query_item = query_items[i]
                print(query_item)
                bool_sign = query_item["boolSign"]
                column = query_item["column"]
                operator = query_item["operator"]
                value = query_item["value"]

                temp_addrs = []
                print(f"第{i+1}个条件")
                if operator == "=":
                    if column == table.primary_key:
                        if len(query_items) == 1:
                            return table.main_index.search(value)
                        else:
                            return []
                    else:
                        if column in table.secondary_indexes.keys():
                            temp_addrs = table.secondary_indexes[column].search(value)
                        else:
                            for j in range(0,table.length):
                                if table.data[j][column] == value:
                                    temp_addrs.append(j)
                else:
                    condition = condtion_wrapper(column,operator,value)
                    for j in range(1, table.length):
                        if condition(table.data[j]):
                            temp_addrs.append(j)

                if bool_sign == "AND":
                    print("执行")
                    result_addrs = ArrayOperation.two_array_intersection(result_addrs,temp_addrs)

                else:
                    result_addrs = ArrayOperation.two_array_union(result_addrs,temp_addrs)
                print(result_addrs)

            #  根据地址取出数据
            return result_addrs
    # 还需补充 异常处理 空返回值 参数验证

    def multiple_connect_query(self, select: list, fr_om: list, connection: dict, operators: list, bool_signs: list,
                               value: list, query_list: list, tables: list) -> list:
        """
        索引连接查询
        看你王爹的
        :param select:表名：列名  组成的字典
        :param fr_om:表名组成的列表
        :param connection:链接方式 用于连接两个表的字段不能重名！！！ 好像重名也没啥？o.0
        :param operators:
        :param bool_signs:
        :param value:
        :param tables:
        :return:
        """
        index = BSTIndex(tables[1].table_name + '_index', tables[1], connection[tables[1].table_name])
        data = tables[0].data
        for d in data:
            keys = d.keys()
            for key in keys:
                new_key = tables[0].table_name + '.' + key
                x = d.pop(key)
                d[new_key] = x

        columns = tables[0].table_name + '.' + connection[tables[0].table_name]
        for d in data:
            con = index.search(d[columns])
            keys = con.keys()
            for key in keys:
                new_key = tables[1].table_name + '.' + key
                x = con.pop(key)
                con[new_key] = x
            d.update(con)
        # 连接成功后就是单表查询逻辑
        operator_dict = {
            'and': operator.and_,
            'or': operator.or_
        }
        query_res = []
        bool_res: bool = True
        for d in data:
            d_copy = d
            res_lis: list = []
            for col, o, v in zip_longest(query_list, operators, value, fillvalue=None):
                if o is None:
                    break
                elif o == '=':
                    o = '=='
                if type(v) == str:
                    res = d[col] == v
                else:
                    res = eval(str(d[col]) + o + str(v))
                # 注意，eval() 函数有一些安全问题，因为它会执行任何传入的字符串。如果你在不受信任的环境中使用 eval()，它可能会被用来执行恶意代码。因此，除非你完全信任输入的来源，否则最好不要使用 eval()。
                # 针对字符串型数据运算符只能是=
                res_lis.append(res)
            for i, b in zip_longest(range(len(res_lis)), bool_signs):
                if b is None:
                    break
                if i == 0:
                    bool_res = operator_dict[b](res_lis[i], res_lis[i + 1])
                else:
                    bool_res = operator_dict[b](bool_res, res_lis[i])
            if bool_res:
                query_res.append(d_copy)
        filtered_data = []
        for d in query_res:
            filtered_row = {key: value for key, value in d.items() if key in select}
            filtered_data.append(filtered_row)
        del index
        return filtered_data

    def nested_query(self, select: list, fr_om: list, connection: dict, operators: list, bool_signs: list,
                     value: list, query_list: list, tables: list) -> list:
        """
        嵌套连接查询
        :param select:
        :param fr_om:
        :param connection:
        :param operators:
        :param bool_signs:
        :param value:
        :param query_list:
        :param tables:
        :return:
        """
        data = tables[0].data
        for d in data:
            keys = d.keys()
            for key in keys:
                new_key = tables[0].table_name + '.' + key
                x = d.pop(key)
                d[new_key] = x
        data2 = tables[1].data
        for d in data2:
            keys = d.keys()
            for key in keys:
                new_key = tables[1].table_name + '.' + key
                x = d.pop(key)
                d[new_key] = x

        columns = tables[0].table_name + '.' + connection[tables[0].table_name]
        for d in data:
            for tar in tables[1].data:
                if d[columns] == tar[tables[1].table_name + '.' + connection[tables[1].table_name]]:
                    d.update(tar)
        # 连接成功后就是单表查询逻辑
        operator_dict = {
            'and': operator.and_,
            'or': operator.or_
        }
        query_res = []
        bool_res: bool = True
        for d in data:
            d_copy = d
            res_lis: list = []
            for col, o, v in zip_longest(query_list, operators, value, fillvalue=None):
                if o is None:
                    break
                elif o == '=':
                    o = '=='
                if type(v) == str:
                    res = d[col] == v
                else:
                    res = eval(str(d[col]) + o + str(v))
                # 注意，eval() 函数有一些安全问题，因为它会执行任何传入的字符串。如果你在不受信任的环境中使用 eval()，它可能会被用来执行恶意代码。因此，除非你完全信任输入的来源，否则最好不要使用 eval()。
                # 针对字符串型数据运算符只能是=
                res_lis.append(res)
            for i, b in zip_longest(range(len(res_lis)), bool_signs):
                if b is None:
                    break
                if i == 0:
                    bool_res = operator_dict[b](res_lis[i], res_lis[i + 1])
                else:
                    bool_res = operator_dict[b](bool_res, res_lis[i])
            if bool_res:
                query_res.append(d_copy)
        filtered_data = []
        for d in query_res:
            filtered_row = {key: value for key, value in d.items() if key in select}
            filtered_data.append(filtered_row)
        return filtered_data

    def materialize_view(self, view: View) -> Table:
        pass



    """数据对象定义"""
    def get_table(self, table_name: str) -> Table:
        return self.__tables.get(table_name,None)

    def get_index(self, index_name: str) -> Index:
        return self.__indexes.get(index_name,None)

    def get_view(self, view_name: str) -> View:
        return self.__views.get(view_name,None)

    @property
    def table_names(self) -> list:
        return list(map(lambda table:table.get("name"),self.configuration["tables"]))

    @property
    def index_names(self)->list:
        return list(map(lambda index:index.get("name"),self.configuration["indexes"]))

    @property
    def view_names(self)->list:
        return list(map(lambda view:view.get("name"),self.configuration["views"]))

    def create_table(self, table_name: str,primary_key:str or tuple,column_units:list,data:list=[],foreign_units:list=[]):
        print("创建基本表")
        #  更新配置文件
        if table_name not in self.table_names:
            self.configuration["tables"].append({
                "name": table_name,
                "column_units": column_units,
                "foreign_units":foreign_units
            })

            #  磁盘上创建表文件
            columns = [column_unit["name"] for column_unit in column_units]
            FileManager.create_table_file(table_name, columns)

        #  添加到内存中的表集合
        table = Table(
            table_name=table_name,
            primary_key=primary_key,
            column_units=column_units,
            data = data,
            foreign_units=foreign_units
        )
        self.__tables.setdefault(table_name,table)

        #  为表建立它的主码索引（聚簇索引）
        self.create_index("BSTIndex", "cluster_{0}".format(table_name), table_name, primary_key)

        # table.main_index = index_primary_key  #  设置主索引
        # table.data = index_primary_key.inorder_traversal_data(index_primary_key.root)

        print("表创建完毕")


    def create_index(self,index_type:str,index_name:str, table_name: str, column: str):
        print("创建索引")

        #  更新配置文件
        if index_name not in self.index_names:
            self.configuration["indexes"].append({
                "name": index_name,
                "type": index_type,
                "table_name": table_name,
                "column": column
            })

        table: Table = self.get_table(table_name)
        if index_type == "BSTIndex":
            index = BSTIndex(
                    index_name=index_name,
                    table=table,
                    column=column
                )
            table.main_index = index
        elif index_type == "HashIndex":
            index = HashIndex(
                    index_name=index_name,
                    table=table,
                    column=column
                )
            self.__indexes.setdefault(
                index_name,
                index
            )
            table.secondary_indexes.setdefault(index_name,index)
        else:
            distinct_num = 10
            index = GroupIndex(
                index_name=index_name,
                table=table,
                column=column,
                distinct_num=distinct_num
            )
            self.__indexes.setdefault(
                index_name,
                index
            )
            table.secondary_indexes.setdefault(index_name, index)
        print("索引创建完毕！")

    def create_view(self, table_name: str, columns: list):
        pass

    def drop_table(self, table_name: str) -> None:
        print("删除基本表")

        #  删除内存中的Table表
        self.__tables.pop(table_name)
        #  删除基于这个表建立的索引
        # for index_name,index in self.__indexes:
        #     if index.table_name == table_name
        #         del self.__indexes[index_name]

        #  删除配置中的表
        table_names:list = self.table_names
        del self.configuration["tables"][table_names.index(table_name)]
        #  删除配置中基于这个表建立的索引
        index_names = self.index_names
        for index_name,index in self.__indexes.items():
            if index.table_name == table_name:
                del self.configuration["indexes"][index_names.index(index_name)]



        #  删除磁盘上的表文件
        FileManager.drop_table_file(table_name)
        self.save_config()

    def drop_index(self, index_name: str) -> None:
        print("删除索引")
        self.__indexes.pop(index_name)

        index_names:list = self.index_names
        print(index_names)
        del self.configuration["indexes"][index_names.index(index_name)]

        self.save_config()

    def drop_view(self, view_name: str):
        pass

    """加载数据对象"""
    #  加载表
    def load_tables(self) -> None:
        root_dir = self.root_dir
        for table_dict in self.configuration["tables"]:
            """测试读取文件的效果"""
            table_name = table_dict["name"]
            column_units = table_dict["column_units"]
            primary_key = ""
            for column_unit in column_units:
                if "PRIMARY KEY" in column_unit["constraints"]:
                    primary_key = column_unit["name"]
                    break
            foreign_units = table_dict["foreign_units"]
            data = FileManager.read_file(root_dir+ "/table/" + table_dict["name"] + ".csv")

            """试试生成表对象"""
            self.create_table(table_name, primary_key, column_units, data,foreign_units)

    #  加载索引
    def load_indexes(self) -> None:
        root_dir = self.root_dir
        for index_dict in self.configuration["indexes"]:
            """根据表来加载索引"""
            index_type = index_dict["type"]
            index_name = index_dict["name"]
            table_name = index_dict["table_name"]
            column = index_dict["column"]
            self.create_index(index_type, index_name, table_name, column)

    #  加载视图
    def load_views(self) -> None:
        pass

    """数据对象操作——插入、更新、删除"""

    def insert_record(self,table_name:str,columns:list,values:list[dict]) -> bool:
        try:
            table = self.get_table(table_name) #  获取表对象
            print(table.main_index)
            filter_values = []
            """更新主索引"""
            for value in values:
                print(value)
                primary_value = value.get(table.primary_key)
                if bool(primary_value) and self.check_entity_integrity(table,primary_value):
                    table.main_index.insert(value) #  更新主索引
                    filter_values.append(value)

            """更新辅助索引"""
            for value in filter_values:
                table.data.append(value)
                if len(table.secondary_indexes) != 0:
                    for index_name, index in table.secondary_indexes.items():
                        index.insert(value.get(index.column), table.length)


            FileManager.write_file(table.data,self.root_dir+f"/table/{table_name}.csv")
            return len(filter_values) != 0
        except Exception:
            traceback.print_exc()
            return False

    def update_record(self,table_name:str,update_item:dict,query_items:list) -> bool:
        table = self.get_table(table_name)
        addrs = self.single_condition_query(table, query_items)

        column = update_item["column"]
        value = update_item["column"]

        for addr in addrs:
            table.data[addr][column] = value

        FileManager.write_file(table.data, self.root_dir + f"/table/{table_name}.csv")
        return True


    def delete_record(self,table_name:str,query_items:list)->bool:
        table = self.get_table(table_name)
        addrs = self.single_condition_query(table,query_items)
        print("查找到的地址",addrs)

        for addr in addrs:
            table.data[addr].clear()
        FileManager.write_file(table.data,self.root_dir+f"/table/{table_name}.csv")
        return True








