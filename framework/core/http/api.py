import requests
from functools import wraps
from typing import Dict, Callable, Any, Optional
import base64


class APIResponse:
    """
    封装API响应，提供更友好的接口
    """

    def __init__(self, response: requests.Response):
        self._response = response
        self.status_code = response.status_code
        self.headers = dict(response.headers)

        try:
            self._json = response.json()
        except ValueError:
            self._json = None

    @property
    def json(self) -> Optional[Dict]:
        """获取响应的JSON数据"""
        return self._json

    @property
    def text(self) -> str:
        """获取响应的文本内容"""
        return self._response.text

    @property
    def data(self) -> Any:
        """获取响应数据中的data字段"""
        return self._json.get('data') if self._json else None

    @property
    def code(self) -> str:
        """获取响应数据中的code字段"""
        return self._json.get('code') if self._json else None


class API:
    """
    API类，整合HTTP方法装饰器和核心功能
    优化后支持第一段代码中的使用场景
    """

    def __init__(self):
        # 初始化支持的HTTP方法
        self.methods = ['get', 'post', 'put', 'delete', 'patch']
        self.http = self  # 为了支持 api.http.post 的调用方式
        self._marks = {}  # 用于存储mark装饰器的信息

        # 动态创建各种HTTP方法装饰器
        for method in self.methods:
            setattr(self, method, self._create_http_decorator(method.upper()))

    def mark(self, module=None):
        """mark装饰器工厂方法"""

        def decorator(func):
            func.api_mark = {'module': module}
            return func

        return decorator

    def _create_http_decorator(self, method: str) -> Callable:
        """
        创建HTTP方法装饰器的工厂方法
        """

        def decorator(path: str, *, base_url: str = None, headers: Dict = None):
            def wrapper(func: Callable):
                # 保存API元数据到函数属性中
                func.api_metadata = {
                    'method': method,
                    'path': path,
                    'base_url': base_url,
                    'headers': headers or {}
                }

                @wraps(func)
                def inner_wrapper(*args, **kwargs):
                    # 获取self实例(通常是测试类实例)
                    instance = args[0] if args else None

                    # 获取请求数据 - 支持多种参数传递方式
                    data = kwargs.get('data', kwargs.get('json', {}))
                    if not data and len(args) > 1:
                        data = args[1]

                    # 获取完整URL
                    final_base_url = (
                            base_url or
                            (getattr(instance, 'base_url', None) if instance else None)
                    )
                    url = f"{final_base_url}{path}" if final_base_url else path

                    # 合并headers
                    final_headers = {
                        **(headers or {}),
                        **(getattr(instance, 'default_headers', {}) if instance else {})
                    }

                    # 处理文件上传 (支持第一段代码中的base64图片上传)
                    if 'faceImg' in data or 'cardImg' in data:
                        # 如果数据中包含图片字段，直接发送JSON
                        response = requests.request(
                            method=method,
                            url=url,
                            headers=final_headers,
                            json=data
                        )
                    else:
                        # 普通请求
                        response = requests.request(
                            method=method,
                            url=url,
                            headers=final_headers,
                            json=data
                        )

                    # 返回封装后的响应对象
                    return APIResponse(response)

                return inner_wrapper

            return wrapper

        return decorator


# 创建全局api实例
api = API()

# 示例使用方式 (模拟第一段代码中的使用场景)
if __name__ == "__main__":
    class FaceDB:
        def __init__(self):
            self.base_url = "http://example.com/api"
            self.default_headers = {"Content-Type": "application/json"}

        @api.http.post("/facedb/insert")
        def facedb_insert(self, data):
            pass


    class FaceDBFace:
        def __init__(self):
            self.base_url = "http://example.com/api"
            self.default_headers = {"Content-Type": "application/json"}

        @api.http.post("/facedb/face/insert")
        def facedbface_insert(self, data):
            pass


    # 模拟第一段代码的调用
    facedb = FaceDB()
    facedbface = FaceDBFace()

    # 新增人像库
    res = facedb.facedb_insert({"test_facedb_insert_01": {}})
    print(f"新增人像库id：{res.data}")
    assert res.code == "00000000"

    # 新增人像集
    with open("blacklist_face.jpg", "rb") as face_img:
        img_b64 = base64.b64encode(face_img.read()).decode('utf-8')

    data = {
        "test_facedbface_insert_01": {
            "facedbId": res.data,
            "faceImg": img_b64,
            "cardImg": img_b64
        }
    }

    response = facedbface.facedbface_insert(data)
    while response.code != "00000000":
        response = facedbface.facedbface_insert(data)
    print(f"新增人像集id：{response.data}")