import yaml
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, ValidationError


class TestCaseModel(BaseModel):
    """测试用例基础模型（可根据需要扩展）"""
    case_id: str
    description: str
    req_data: Dict[str, Any]
    expected: Union[Dict, List, str, int]
    enabled: bool = True


class TestDataLoader:
    """
    基于第三方库的测试数据加载器

    依赖：
    - pyyaml (处理YAML)
    - pydantic (数据验证)

    功能特点：
    1. 自动类型验证
    2. 支持多环境配置
    3. 智能变量替换
    4. 内置缓存机制
    5. 支持JSON/YAML
    """

    def __init__(self,
                 env: str = "test",
                 testdata_dir: str = "testdata",
                 base_config: str = "config.yaml"):
        self.env = env
        self.cache = {}  # 简单缓存
        self.base_dir = self._find_project_root() / testdata_dir
        self.config = self._load_config(base_config)

        # 初始化变量池（合并系统环境变量+配置文件）
        self.variables = {
            **os.environ,
            **self.config.get("variables", {}),
            "env": self.env
        }

    @staticmethod
    def _find_project_root(marker: str = "pyproject.toml") -> Path:
        current = Path(__file__).absolute().parent
        while current != current.parent:
            if (current / marker).exists():
                return current
            current = current.parent
        raise FileNotFoundError(f"Project root not found with marker: {marker}")

    def _load_config(self, filename: str) -> Dict[str, Any]:
        """加载配置文件（带缓存）"""
        if filename in self.cache:
            return self.cache[filename]

        path = self.base_dir / filename
        with open(path, encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
            self.cache[filename] = config
            return config

    def _resolve_value(self, value: Any) -> Any:
        """递归解析变量（支持${var}格式）"""
        if isinstance(value, dict):
            return {k: self._resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_value(i) for i in value]
        elif isinstance(value, str):
            return re.sub(
                r'\$\{(.+?)\}',
                lambda m: str(self.variables.get(m.group(1), ""),
                              value)
            )
        return value

    def load_cases(
            self,
            module: str,
            file: str = "cases.yaml",
            validate: bool = True
    ) -> List[TestCaseModel]:
        """加载测试用例（支持自动验证）"""
        path = self.base_dir / module / file
        if path in self.cache:
            return self.cache[path]

        with open(path, encoding='utf-8') as f:
            raw_cases = yaml.safe_load(f) or []

        processed = []
        for case in raw_cases:
            try:
                # 变量替换
                resolved = self._resolve_value(case)
                # 数据验证
                if validate:
                    processed.append(TestCaseModel(**resolved).dict())
                else:
                    processed.append(resolved)
            except ValidationError as e:
                raise ValueError(f"Invalid test case {case.get('case_id')}: {e}")

        self.cache[path] = processed
        return processed


# 使用示例
if __name__ == "__main__":
    loader = TestDataLoader(env="staging")
    try:
        cases = loader.load_cases("user_module")
        for case in cases:
            print(f"Loaded case: {case['case_id']}")
    except Exception as e:
        print(f"Error loading cases: {e}")