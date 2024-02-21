"""
    author:Shuai Guo
    tool:pycharm
    适用于整数单元，例如成绩之类的
"""


from dbfiles.baseclass.Index import Index
from dbfiles.dataobject.Table import Table

"""基于拉链法构造哈希表的运算算法"""

"""哈希表单元"""
class HashUnit:
    def __init__(self):
        """
        :param key: 关键字
        :param data: 数据域，列表
        """
        self.key = -1
        self.data = []  #  装的是原本数组每一个元素的下标
        self.count = 0 #  查找次数

    def __str__(self):
        return f"key:{self.key},data:{self.data}"

"""哈希索引"""
class HashIndex(Index):
    def __init__(self,index_name:str,table:Table,column:str):
        super().__init__(index_name,table,column)

        self.__table_length:int = len(table.data)

        self.__hash_table:list[HashUnit] = [HashUnit() for i in range(0,self.__table_length)]

        if bool(table.data):
            for i in range(0, len(table.data)):
                if table.column_type(column) == "INT":
                    self.insert(table.data[i][column],i)
                else:
                    self.insert(table.data[i][column].__hash__(),i)

    @property
    def index_type(self) -> str:
        return "HashIndex"

    @property
    def table_length(self)->int:
        return self.__table_length

    @property
    def hash_table(self):
        return self.__hash_table

    #  将数据元素插入哈希表
    def insert(self,key:int,i:int) -> None:
        adr = key % self.__table_length
        if self.__hash_table[adr].key == -1:
            self.__hash_table[adr].key = key
            self.__hash_table[adr].data.append(i)

        elif self.__hash_table[adr].key == key:
            self.__hash_table[adr].data.append(i)

        else:
            while self.__hash_table[adr%self.__table_length] != -1:
                adr += 1
            self.__hash_table[adr].key = key
            self.__hash_table[adr].data.append(i)


    def delete(self, key: int) -> bool:
        adr: int = key % self.__table_length
        init_addr:int = adr
        while self.__hash_table[adr].key != key and adr != init_addr:
            adr = (adr + 1) % self.__table_length
        if adr == init_addr:
            return False
        else:
            self.__hash_table[adr].key = -1
            self.__hash_table[adr].data.clear()
            return True

    def update(self) -> bool:
        pass

    def search(self,key:int) -> list:
        adr:int = key % self.__table_length
        while self.__hash_table[adr].key != key:
            adr = (adr + 1)%self.__table_length
        return self.__hash_table[adr].data









