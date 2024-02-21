"""
    author:Shuai Guo
    tool:pycharm
    function:二叉搜索树
    主码索引：聚簇索引，唯一值索引
"""
from dbfiles.baseclass.Index import Index
from dbfiles.dataobject.Table import Table

import sys

sys.setrecursionlimit(10000)

"""二叉排序树的结点"""


class BSTNode:
    def __init__(self, key: object, data: dict = None):
        """
        :param key: 以什么关键字来建立二叉搜索树，字符串类型
        """
        self.key = key  # 关键字
        self.data_domain = data  # 数据域
        self.left = None  # 左结点
        self.right = None  # 右结点

    def __str__(self):
        return f"{self.key} : {self.data_domain}"


"""二叉排序树索引"""


class BSTIndex(Index):
    def __init__(self, index_name: str, table: Table, column: str = "序号"):
        super().__init__(index_name, table, column)
        self.__root = None
        #  __node_num只在插入和删除的时候更新
        self.__node_num = 0

        """数据加载"""
        if len(table.data):
            self.insert(*table.data)

    """外部属性"""
    @property
    def index_type(self):
        return "BSTIndex"

    @property
    def root(self) -> BSTNode:
        return self.__root

    @property
    def tree_height(self) -> int:
        return self.__tree_height(self.__root)

    @property
    def node_num(self) -> int:
        return self.__node_num

    #  找到最小值结点
    def __min_value_node(self, root: BSTNode) -> BSTNode:
        """
        找到某一颗树的最小值结点（最左边的那一个结点）
        :param root:这棵树的根节点
        :return:找到的结点，BSTNode类型的对象
        """
        current = root
        #  就一直找到其左子树就对了
        while current.left is not None:
            current = current.left
        return current

        #  中序遍历，生成一个单调递增的有序数组

    def inorder_traversal(self, node: BSTNode) -> list:
        sequence = []
        self.__inorder_traversal(node, sequence)
        return sequence

    def __inorder_traversal(self, root: BSTNode, sequence: list) -> None:
        if root:
            self.__inorder_traversal(root.left, sequence)
            #  将其插入到自己中序遍历后的有序数列中
            if len(sequence) < self.node_num:
                sequence.append(root)
            self.__inorder_traversal(root.right, sequence)

    def inorder_traversal_data(self,root:BSTNode):
        return [node.data_domain for node in self.inorder_traversal(root)]

    def __tree_height(self, root: BSTNode) -> int:
        if root is None:
            return 0
        else:
            lchild = self.__tree_height(root.left)
            rchild = self.__tree_height(root.right)
            return max(lchild, rchild) + 1

    def __count_node_num(self, root: BSTNode) -> int:
        if root is None:
            return 0
        else:
            return self.__count_node_num(root.left) + self.__count_node_num(root.right) + 1

    #  给指定关键字结点更新属性
    def update(self, root: BSTNode, key: str, column: str, value: object) -> bool:
        if root is None:
            return False
        node = self.search(key)
        node.data_domain[column] = value
        return True

    #  查找
    def search(self, key: object) -> dict:
        return self.__search(self.__root, key).data_domain

    def __search(self, root: BSTNode, key: object) -> BSTNode:
        #  1.当根节点为空或者是找到了对应的结点
        if root is None or root.key == key:
            return root
        #  2.当关键字小于根节点关键字的值，在左子树中查找
        if key < root.key:
            return self.__search(root.left, key)
        #  3.当关键字大于根节点关键字的值，在右子树中查找
        else:
            return self.__search(root.right, key)

    #  插入操作
    def insert(self, *data: dict) -> None:
        for datum in data:
            key = datum[self.column]
            self.__root = self.__insert(self.__root, key, datum)
        self.__node_num = self.__count_node_num(self.__root)
        self.balance_tree()  # Balance the tree after insertion

    def __insert(self, root: BSTNode, key: object, record: dict) -> BSTNode:
        """
        插入结点
        :param root:
        :param key:
        :return:
        """
        if root is None:
            return BSTNode(key, record)
        if key < root.key:
            root.left = self.__insert(root.left, key, record)
        else:
            root.right = self.__insert(root.right, key, record)
        return root

    # 删除给定关键字的结点
    def delete(self, key: object) -> None:
        self.__root = self.__delete(self.__root, key)
        self.__node_num = self.__count_node_num(self.__root)
        self.__root = self.balance_tree()  # Balance the tree after deletion

    def __delete(self, root: BSTNode, key: object) -> BSTNode:
        """
        删除给定关键字的结点
        :param root: 树的根节点
        :param key: 关键字
        :return: 删除指定结点后的树的根节点
        """
        #  当根节点为空
        if root is None:
            return root  # 什么也不干，就返回根节点
        #  1.当关键字小于根节点的关键字
        if key < root.key:
            root.left = self.__delete(root.left, key)  # 在左子树中进行查找
        #  2.当关键字大于根节点的关键字
        elif key > root.key:
            root.right = self.__delete(root.right, key)  # 在右子树中进行查找
        #  3.当关键字等于根节点的关键字
        else:
            #  当该节点没有左子树,直接把右孩子节点作为其双亲节点的右孩子
            if root.left is None:
                temp = root.right
                root = None
                return temp
            # 当该节点没有右子树，直接把左孩子结点作为其双亲节点的左孩子
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            #  当该结点左右子树都有，找到右子树的值最小的结点，也就是最靠左边的结点
            temp = self.__min_value_node(root.right)
            root.key = temp.key
            root.right = self.__delete(root.right, temp.key)

        return root

    """建立二叉平衡树，始终让搜索次数是logN"""
    def balance_tree(self):
        self.__root = self.__balance(self.__root)

    def __balance(self, root: BSTNode) -> BSTNode:
        if root is None:
            return root

        left_height = self.__tree_height(root.left)
        right_height = self.__tree_height(root.right)

        if abs(left_height - right_height) > 1:
            nodes = self.inorder_traversal(root)
            return self.__build_balanced_tree(nodes)

        root.left = self.__balance(root.left)
        root.right = self.__balance(root.right)

        return root

    def __build_balanced_tree(self, nodes: list[BSTNode]) -> BSTNode:
        if not nodes:
            return None

        mid = len(nodes) // 2

        root = BSTNode(nodes[mid].key, nodes[mid].data_domain)
        root.left = self.__build_balanced_tree(nodes[:mid])
        root.right = self.__build_balanced_tree(nodes[mid + 1:])

        return root




if __name__ == "__main__":
    # data = FileManager.read_file(r"C:\Users\86173\PyCharmProjects\PyOracle\MyDB\app01\views\dbfiles\table\student.csv")

    data = [{"number":i } for i in range(1,100)]
    table = Table(
        "student",
        "studentid",
        column_units=[
            {
                "name": "studentname",
                "type": "STRING",
                "constraints": [
                    "UNIQUE",
                    "NOT NULL"
                ]
            },
            {
                "name": "studentid",
                "type": "INT",
                "constraints": [
                    "PRIMARY KEY"
                ]
            },
            {
                "name": "grade",
                "type": "INT",
                "constraints": [
                    "NOTHING"
                ]
            },
            {
                "name": "specialityid",
                "type": "INT",
                "constraints": [
                    "NOTHING"
                ]
            },
            {
                "name": "courseid",
                "type": "INT",
                "constraints": [
                    "NOTHING"
                ]
            }
        ],
        data=data,
        foreign_units=[
            {
                "name": "specialityid",
                "table": "speciality",
                "column": "specialityid"
            },
            {
                "name": "courseid",
                "table": "course",
                "column": "courseid"
            }
        ]
    )
    avl_index = BSTIndex("index", table,"number")

    print()
    print("树高",avl_index.tree_height)


    print("结点总数",avl_index.node_num)

    target = avl_index.search(56)
    print(target)

