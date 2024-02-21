from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dbfiles.DBMS import DBMS
from dbfiles.utilityclass.Parser import Parser
from collections import defaultdict


def dijkstra(start_node, end_node, nodes, edges):
    graph = defaultdict(dict)
    for edge in edges:
        graph[edge['source']][edge['target']] = edge['weight']

    dist = {node['id']: float('inf') for node in nodes}  # 保存起点到各个节点的最短距离
    prev = {node['id']: None for node in nodes}  # 记录最短路径的前一个节点

    dist[start_node['id']] = 0  # 起点到自身的距离为0

    unvisited_nodes = [node['id'] for node in nodes]  # 未访问节点列表

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node_id: dist[node_id])
        unvisited_nodes.remove(current_node)

        if dist[current_node] == float('inf'):
            break  # 如果剩余节点无法到达，则退出循环

        for neighbor, weight in graph[current_node].items():
            distance = dist[current_node] + weight

            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_node

    # 构建最短路径的边和节点
    shortest_path_nodes = []
    shortest_path_edges = []

    current_node_id = end_node['id']
    while current_node_id is not None:
        shortest_path_nodes.insert(0, {'id': current_node_id})
        prev_node_id = prev[current_node_id]
        if prev_node_id is not None:
            shortest_path_edges.insert(0, {'source': prev_node_id, 'target': current_node_id,
                                           'weight': graph[prev_node_id][current_node_id]})
            current_node_id = prev_node_id
        else:
            break

    return {'nodes': shortest_path_nodes, 'edges': shortest_path_edges}


GlobalDBMS = DBMS.get_instance()

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

"""根路径"""


@app.route('/')
def index():
    return render_template("index.html")  # 返回文本数据


"""1.登录路径"""


@app.route("/log/login", methods=["POST"])
def login():
    login_infos = request.json
    is_login = GlobalDBMS.log_in(**login_infos)
    return jsonify({"isLogin": is_login})


@app.route("/log/register", methods=["POST"])
def register():
    regi_infos = request.json
    print(regi_infos)
    is_repeated = GlobalDBMS.register(**regi_infos)
    return jsonify({"isRepeated": is_repeated})


@app.route("/log/default-login", methods=["GET"])
def default_login():
    saved_user = GlobalDBMS.configuration["saved_user"]
    is_login = saved_user != -1
    return jsonify({"isLogin": is_login, "username": GlobalDBMS.configuration["users"][saved_user]["username"]})


"""2.获取元信息的路径"""


@app.route("/meta/table-name", methods=["GET"])
def table_name():
    return jsonify({"tableNames": GlobalDBMS.table_names})


@app.route("/meta/index-name", methods=["GET"])
def index_name():
    return jsonify({"indexNames": GlobalDBMS.index_names})


@app.route("/meta/view-name", methods=["GET"])
def view_name():
    return jsonify({"viewNames": GlobalDBMS.view_names})


@app.route("/meta/data-name", methods=["GET"])
def data_name():
    return jsonify(
        {
            "tableNames": GlobalDBMS.table_names,
            "indexNames": GlobalDBMS.index_names,
            "view_names": []
        }
    )


@app.route("/meta/table-and-view", methods=["GET"])
def table_and_view():
    tables = [GlobalDBMS.get_table(table_name).accessible_attrs() for table_name in GlobalDBMS.table_names]
    # views = [GlobalDBMS.get_view(view_name).accessible_attrs() for view_name in GlobalDBMS.view_names]
    views = []
    return jsonify({"tables": tables, "views": views})


@app.route("/meta/layer-name", methods=["GET"])
def layer_name():
    layer_names = [table_name.split('_')[0] for table_name in GlobalDBMS.table_names if "layer" in table_name]

    return jsonify({"layerNames": layer_names})


"""3.数据定义"""


@app.route("/create/table", methods=["POST"])
def create_table():
    #   响应体
    body = request.json

    table_name = body["tableName"]
    column_units = Parser.filter_specified_columns_data(body["columnUnits"], ["name", "constraints", "type"])
    primary_key = body["primaryKey"]

    """外码"""
    foreign_units = Parser.filter_specified_columns_data(body["foreignUnits"], ["name", "table", "column"])
    print(foreign_units)

    GlobalDBMS.create_table(
        table_name,
        primary_key,
        column_units,
        foreign_units=foreign_units
    )

    print(GlobalDBMS.get_table(table_name).foreign_units)

    GlobalDBMS.save_config()
    return jsonify({"isCreated": True})


@app.route("/create/index", methods=["POST"])
def create_index():
    body = request.json
    print(body)
    GlobalDBMS.create_index(**body)

    GlobalDBMS.save_config()
    return jsonify({"isCreated": True})


@app.route("/create/view", methods=["POST"])
def create_view():
    body = request.json
    print(body)
    GlobalDBMS.save_config()
    return jsonify({"isCreated": True, "message": "视图创建失败！"})


@app.route("/drop/object", methods=["POST"])
def drop_object():
    body = request.json
    data_type = body.get("dataObjType")
    if data_type == "tableNames":
        table_name = body.get("dataObjName")
        GlobalDBMS.drop_table(table_name)
    elif data_type == "indexNames":
        index_name = body.get("dataObjName")
        GlobalDBMS.drop_index(index_name)
    else:
        view_name = body.get("dataObjName")
        GlobalDBMS.drop_view(view_name)

    GlobalDBMS.save_config()
    return jsonify({"isDrop": True})


"""4.数据查询"""


@app.route("/query/single", methods=["POST"])
def query_single():
    body = request.json
    table_name = body.get("tableName", "student")
    table = GlobalDBMS.get_table(table_name)

    query_items = body.get("queryItems", [])

    addrs = GlobalDBMS.single_condition_query(
        table=table,
        query_items=query_items
    )

    table_dict = {
        "name": table.table_name,
        "columns": body.get("columns", [f'{table_name}id']),
        "data": [table.data[addr] for addr in addrs]
    }
    return jsonify(table_dict)


@app.route("/query/multiple", methods=["POST"])
def query_multiple():
    body = request.json
    print(body)

    table_dict = {
        "name": "student",
        "columns": GlobalDBMS.get_table("student").columns,
        "data": GlobalDBMS.get_table("student").data
    }

    return jsonify(table_dict)


@app.route("/query/nested", methods=["POST"])
def query_nested():
    body = request.json
    print(body)

    table_dict = {
        "name": "student",
        "columns": GlobalDBMS.get_table("student").columns,
        "data": GlobalDBMS.get_table("student").data
    }

    return jsonify(table_dict)


"""5.数据操作"""


@app.route("/manipluate/insert", methods=["POST"])
def manipulate_insert():
    body = request.json

    table_name = body.get("tableName", "我是不存在的表")
    columns = body.get("columns", "我是空列")
    values = body.get("values", "可能没有值")

    if len(values) == 0:
        print("数据记录数目不能为0")
        return jsonify({"isInserted": False, "message": "插入失败，插入数据数目不能为0！"})
    else:
        is_inserted: bool = GlobalDBMS.insert_record(table_name, columns, values)
        message: str = "插入成功！" if is_inserted else "插入失败，请检查插入数据！"
        return jsonify({"isInserted": is_inserted, "message": message})


@app.route("/manipluate/nested", methods=["POST"])
def manipulate_delete():
    body = request.json

    table_name = body.get("tableName", "我是不存在的表")
    query_items = body.get("queryItems", [])

    print(query_items)

    is_deleted: bool = GlobalDBMS.delete_record(table_name, query_items)
    message = "数据删除完毕！" if is_deleted else "删除出错，请检查输入！"
    return jsonify({"isDeleted": is_deleted, "message": message})


@app.route("/manipluate/update", methods=["POST"])
def manipulate_update():
    body = request.json

    table_name = body.get("tableName")
    update_item = body.get("updateItem")
    query_items = body.get("queryItems")

    is_updated = GlobalDBMS.update_record(table_name, update_item, query_items)
    message = "更新成功！" if is_updated else "更新失败，请检查输入！"
    return jsonify({"isUpdated": True, "message": message})


"""6.空间数据"""


@app.route("/spatial/get-layer", methods=["POST"])
def get_layer():
    body = request.json
    layer_name = body.get("layerName")
    print(layer_name)
    nodes = GlobalDBMS.get_table(f"{layer_name}_nodes").data
    edges = GlobalDBMS.get_table(f"{layer_name}_edges").data
    return jsonify({"nodes": nodes, "edges": edges})


@app.route("/spatial/shortest-path", methods=["POST"])
def shortest_path():
    body = request.json
    layer_name = body.get("layerName")
    start_node = body.get("start")
    end_node = body.get("end")
    print(layer_name)
    print(start_node, end_node)

    nodes = GlobalDBMS.get_table(f"{layer_name}_nodes").data
    edges = GlobalDBMS.get_table(f"{layer_name}_edges").data

    shortest_path = dijkstra(start_node, end_node, nodes, edges)
    print(shortest_path)

    return jsonify(shortest_path)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
