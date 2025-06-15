class API:
    def __init__(self):
        self.modules = {}

    def mark(self, module):
        def decorator(func):
            if module not in self.modules:
                self.modules[module] = []
            self.modules[module].append(func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

# 创建 API 实例
api = API()

# 示例类
class ApplicationDataMonitor:
    @api.mark(module='ocean')
    def monitor_data_add(self, data):
        """数据布控新增"""
        return dict(json=data)

class ApplicationDataMonitor2:
    @api.mark(module='ocean')
    def monitor_data_add2(self, data):
        """数据布控新增"""
        return dict(json=data)

# 可以通过 api.modules 获取模块信息
print(api.modules)