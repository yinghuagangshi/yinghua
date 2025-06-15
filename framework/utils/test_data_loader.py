import yaml
from pathlib import Path
from common.VariableActionLib import VariableActionLib  # 确保该类包含变量解析功能


def get_test_data(module_name: str, data_file: str = "cases.yaml") -> list:
    """
    按模块加载并处理测试数据（支持变量替换、多层级数据解析）

    Args:
        module_name: 模块名称（对应 testdata 目录下的子目录）
        data_file: 数据文件名，默认为 "cases.yaml"

    Returns:
        处理后的测试用例列表（包含变量替换后的请求数据）

    Raises:
        FileNotFoundError: 测试数据文件或公共配置文件不存在时抛出
        ValueError: 变量替换失败时抛出
    """
    try:
        # 获取项目根目录（假设 test_data_loader.py 位于项目/tests/common 目录）
        project_root = Path(__file__).parent.parent.parent
        testdata_base_dir = project_root / "testdata"

        # 构建文件路径（支持环境变量或配置文件动态获取路径）
        case_path = testdata_base_dir / module_name / data_file
        base_config_path = testdata_base_dir / "base_config.yaml"

        # 验证文件存在性
        for path in [case_path, base_config_path]:
            if not path.exists():
                raise FileNotFoundError(f"文件未找到：{path}")

        # 读取数据文件
        with open(case_path, "r", encoding="utf-8") as f:
            cases = yaml.safe_load(f) or []

        with open(base_config_path, "r", encoding="utf-8") as f:
            base_config = yaml.safe_load(f) or {}

        # 初始化变量处理工具
        var_action = VariableActionLib(base_config=base_config)

        # 递归处理多层级变量替换（支持字典、列表、嵌套结构）
        def recursive_replace(data):
            if isinstance(data, dict):
                return {k: recursive_replace(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [recursive_replace(item) for item in data]
            elif isinstance(data, str) and data.startswith("${"):
                return var_action.parse_variable(data)  # 使用工具类解析变量
            else:
                return data

        # 对每个用例执行变量替换（覆盖原数据）
        for case in cases:
            case["req_data"] = recursive_replace(case.get("req_data", {}))

        return cases

    except Exception as e:
        raise RuntimeError(f"测试数据加载失败：{str(e)}") from e