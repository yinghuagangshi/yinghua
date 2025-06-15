import pytest
from pathlib import Path
from common.VariableActionLib import VariableActionLib
from test_data_loader import get_test_data
from utils.random_utils import get_random_str  # 假设随机字符串工具已定义
from services.facedb_service import (  # 假设数据库操作服务已封装
    g_facedb_insert,
    g_facedb_delete
)
from services.data_monitor_service import (
    ApplicationDataMonitor,
    g_data_monitor_delete
)
from utils.db_utils import pg_query  # 数据库查询工具
from utils.assert_utils import assert_str  # 断言工具
from common.ResponseHandleLib import ResponseHandleLib  # 响应处理工具


class TestDataMonitorAdd:
    @pytest.fixture(params=get_test_data("data_monitor", "add_cases.yaml"), name="add_case")
    def fixture_test_data(self, request):
        """
        测试夹具：加载测试数据并管理前置/后置资源
        """
        case = request.param  # 从参数中获取用例数据
        case_doc = case["case_doc"]
        req_data = case["req_data"].copy()  # 避免修改原始数据

        # 前置操作：创建 facedbId（使用上下文管理器或独立函数封装）
        facedb_name = "数据布控库_" + get_random_str(8)
        facedb_id = g_facedb_insert(facedb_name, 0)
        req_data["groupIds"] = facedb_id  # 注入前置数据到请求参数

        yield {  # 使用生成器传递数据到测试用例
            "case_doc": case_doc,
            "req_data": req_data,
            "exp_code": case["exp_code"],
            "exp_msg": case["exp_msg"],
            "assert_type": case["assert_type"],
            "facedb_id": facedb_id  # 传递需清理的资源 ID
        }

        # 后置操作：统一清理资源（无论测试是否失败）
        try:
            g_facedb_delete(facedb_id)  # 清理 facedb
        except Exception as e:
            pytest.fail(f"清理 facedb 失败：{str(e)}")

    def test_monitor_add(self, add_case):
        """
        数据监控添加功能测试
        """
        req_data = add_case["req_data"]
        exp_code = add_case["exp_code"]
        exp_msg = add_case["exp_msg"]
        assert_type = add_case["assert_type"]
        facedb_id = add_case["facedb_id"]  # 从夹具获取前置资源 ID

        try:
            # 发送请求
            res = ApplicationDataMonitor().monitor_data_add(req_data)

            # 差异化断言
            if assert_type == "success_db_check":
                # 校验响应数据
                monitor_id = ResponseHandleLib().check_response_return_data(
                    res, exp_code, exp_msg
                )

                # 数据库层面校验
                sql = "SELECT * FROM cw_mon_monitor WHERE monitor_id = %s"
                sql_data = pg_query(sql, (monitor_id,))  # 使用参数化查询防 SQL 注入
                assert len(sql_data) > 0, "监控数据未写入数据库"
                assert_str("monitorName", sql_data[0]["monitor_name"], req_data["monitorName"])

                # 清理监控数据（夹具已清理 facedb，此处清理 monitor）
                g_data_monitor_delete(monitor_id)

            elif assert_type == "error_param_check":
                # 校验错误响应
                res_json = res.response.json()
                assert res_json["code"] == exp_code, f"预期代码 {exp_code}，实际 {res_json['code']}"
                assert res_json["message"] == exp_msg, f"预期消息 {exp_msg}，实际 {res_json['message']}"

            else:
                pytest.skip(f"不支持的断言类型：{assert_type}")

        except Exception as e:
            pytest.fail(f"测试执行失败：{str(e)}", pytrace=False)