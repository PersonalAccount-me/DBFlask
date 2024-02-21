"""
    author:Shuai Guo
    tool:pycharm
"""
from abc import abstractmethod,ABCMeta

class IInitable(metaclass=ABCMeta):

    @abstractmethod
    def load_config(self)->None:
        """
        读取配置文件（config.json），初始化项目参数
        :param config_file: 配置文件的路径(Json文件)
        :return:无返回值
        """
        pass

    @abstractmethod
    def save_config(self)->None:
        """
        保存配置到配置文件
        :return:
        """
        pass

    @abstractmethod
    def register(self,username:str,password:str,verifyCode:str)->bool:
        """
        用户注册
        :param username: 用户名
        :param password: 密码
        :return:
        """
        #  倘若用户已存在，不可再次注册
        if 1:
            return False
        #  用户名不存在，创建用户
        else:
            return True

    @abstractmethod
    def log_in(self,username:str,password:str,isRemember:bool)->bool:
        pass

    @abstractmethod
    def load_tables(self)->None:
        pass

    @abstractmethod
    def load_indexes(self)->None:
        pass

    @abstractmethod
    def load_views(self)->None:
        pass