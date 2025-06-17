import csv
import os
import yaml
from typing import Dict, Any
import openpyxl

def read_csv():
    TCList = []
    with open("../config.csv", 'r', errors="ignore") as f:
        as_csv = csv.DictReader(f)

        for row in as_csv:
            row = dict(row)
            # getLogger().debug("[TCList]"+str(row))
            if row["isRun"] == 'Y':
                TCList.append(row)

def read_json():
    '''
    获取配置文件有效内容并已json格式输出
    '''
    fileNamePath = os.path.abspath(os.path.join(os.getcwd(), ".."))
    configPath = os.path.join(fileNamePath, 'config.json')
    with open(configPath, 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
        # print(json_data)
    return json_data



class YamlReader:
    """
    安全可靠的YAML文件读取工具类
    """

    def __init__(self):
        # 获取项目根目录（向上三级）
        self._project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def read_yaml(self, relative_path: str) -> Dict[str, Any]:
        """
        读取YAML文件并返回字典

        :param relative_path: 相对于项目根目录的路径
        :return: 解析后的字典数据
        :raises: FileNotFoundError, yaml.YAMLError
        """
        # 构建绝对路径
        abs_path = os.path.join(self._project_root, relative_path)

        # 检查文件是否存在
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"YAML文件不存在: {abs_path}")

        # 安全读取文件
        try:
            with open(abs_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML解析错误: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"读取文件失败: {str(e)}")



def read_excel(path,sheet_name):
    file_excel=openpyxl.load_workbook(path)
    sheet_excel=file_excel[sheet_name]
    data_list=[]
    sheet_head=True
    # print(sheet_excel)
    for row in sheet_excel:
        if sheet_head:
            sheet_head=False
            continue
        row_data=[]
        cell_head=True
        for cell in row:
            if cell_head:
                cell_head=False
                continue
            # 处理空单元格
            a = "" if cell.value == None else cell.value
            row_data.append(a)
        data_list.append(row_data)
    return data_list


