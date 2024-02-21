"""
    author:Shuai Guo
    tool:pycharm
"""
import json
import os
from dbfiles.interfaces.IInitable import IInitable
from abc import ABCMeta,abstractmethod


class InitConfig(IInitable,metaclass=ABCMeta):
    #  配置文件的路径
    configuration = dict()

    #  1.测试用
    # __root_dir = os.path.abspath(".")

    #  2.开发用
    __root_dir = os.path.abspath(r"./dbfiles")

    def __init__(self):
        super(IInitable, self).__init__()
        self.load_config()

    @property
    def root_dir(self)->str:
        return self.__root_dir

    """加载、保存配置"""
    #  加载配置文件
    def load_config(self):
        """加载配置文件"""
        with open(self.__root_dir+"\\config.json","r",encoding="UTF-8") as config_f:
            #  将config.json文件里面的信息加载到 __configuration之中
            self.configuration = json.load(config_f)
        print("初始化配置成功！！")

    #  保存配置信息至配置文件
    def save_config(self):
        print("我被调用了")
        with open(self.__root_dir+"/config.json","w",encoding="utf-8") as config_f:
            json.dump(self.configuration,config_f,indent=4)
        print("配置保存成功！")

    """用户登录选项"""
    #  用户注册
    def register(self,username:str,password:str,verifyCode:str)->bool:
        users:list = self.configuration["users"]
        last_index = 0
        for i in range(0,len(users)):
            user = users[i]
            if username == user["username"]:
                return True
            last_index = i

        users.append({"index":last_index+1,"username":username,"password":password})
        self.save_config()
        return False

    #  用户登录
    def log_in(self,username:str,password:str,isRemember:bool) ->bool:
        users:list = self.configuration["users"]
        for i in range(0,len(users)):
            user:dict = users[i]
            if username == user["username"] and password == user["password"]:
                self.configuration["saved_user"] = i if isRemember else -1
                self.save_config()
                return True
        return False



    #  留给DBMS类来实现
    @abstractmethod
    def load_tables(self) -> None:
        pass

    #  加载索引
    @abstractmethod
    def load_indexes(self) -> None:
        pass

    #  加载视图
    @abstractmethod
    def load_views(self):
        pass


