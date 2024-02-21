"""
    author:Shuai Guo
    tool:pycharm
"""
from typing import Callable


class ArrayOperation:
    @staticmethod
    def binary_insert_sort(values: list, sort_rule: Callable=lambda x:x) -> None:
        """
        折半-插入排序
        :param values: 待排序数组
        :param sort_rule: 排序规则
        :return:
        """
        for i in range(1,len(values)):
            if sort_rule(values[i]) < sort_rule(values[i-1]):
                temp = values[i]
                low,high = 0,i-1
                while low <= high:
                    mid = (low + high)//2
                    if sort_rule(temp) < sort_rule(values[mid]):
                        high = mid - 1
                    else:
                        low = mid + 1
                #  集中进行元素后移
                for j in range(i-1,high,-1):
                    values[j+1] = values[j]
                values[high+1] = temp

    @staticmethod
    def merge_sort(values: list, sort_rule: Callable) -> list:
        """
        归并排序
        :param values: 待排序数组
        :param sort_key: 排序关键字
        :return: None
        """
        pass

    @staticmethod
    def qucik_sort(values: list, sort_rule: Callable) -> list:
        """
        快速排序
        :param values: 待排序数组
        :param sort_key: 排序关键字
        :return: None
        """
        pass

    @staticmethod
    def inverse_num(values: list, sort_rule: Callable) -> int:
        """

        :param values: 待计算逆序数的数组
        :param compare_rule: 比较的规则
        :return:逆序数大小
        """

    @staticmethod
    def reverse_order(values: list):
        """
        逆转数组的顺序
        :param values: 待操作数组
        :return:
        """
        pass

    @staticmethod
    def binary_search(values: list, target: object, compare_rule: Callable) -> int:
        """
        二分查找
        :param values: 待查找数组
        :param compare_key: 比较关键字
        :return: 查找到的数据下标
        """
        pass

    @classmethod
    def remove_duplication(cls,values:list) -> list:
        """
        数组去重
        :param values: 待去重的数组，元素是基本数据类型
        :return: 去重后的数组——有序
        """
        single_values = list()
        for i in values:
            if i not in single_values:
                single_values.append(i)
        cls.binary_insert_sort(single_values)
        return single_values

    @classmethod
    def two_array_union(cls,values1:list,values2:list)->list:
        pass

    @classmethod
    def more_array_union(cls,*values:list)->list:
        if len(values) == 2:
            return cls.two_array_union(values[0].copy(),values[1].copy())
        else:
            union = values[0]
            for i in range(1,len(values)):
                union = cls.two_array_union(union.copy(),values[i].copy())
            return union

    @classmethod
    def more_array_intersection(cls,*values:list)->list:
        if len(values) == 2:
            return cls.two_array_intersection(values[0].copy(),values[1].copy())
        else:
            intersection = values[0]
            for i in range(1,len(values)):
                intersection = cls.two_array_intersection(intersection.copy(),values[i].copy())
            return intersection


    @classmethod
    def two_array_intersection(cls,values1:list,values2:list)->list:
        cls.binary_insert_sort(values1, lambda x: x)
        cls.binary_insert_sort(values2, lambda x: x)
        intersection = []
        i, j = 0, 0

        while i < len(values1) and j < len(values2):
            if values1[i] == values2[j]:
                # 如果两个数组中的元素相同，则加入到交集中
                intersection.append(values1[i])
                i += 1
                j += 1
            elif values1[i] < values2[j]:
                i += 1
            else:
                j += 1
        return intersection

if __name__ == "__main__":
    arr1 = [1,2,4,5,6,7]
    arr2 = [3,4,1,5,7]
    arr3 = [4,5,6,7]
    print(ArrayOperation.more_array_intersection(arr1,arr2,arr3))


