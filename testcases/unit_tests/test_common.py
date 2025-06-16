import pytest
import allure

@allure.epic("用户管理系统")  # 大模块分类
@allure.feature("用户登录")    # 子功能模块
class TestLogin:

    @allure.story("登录成功")  # 用户故事
    @allure.title("验证正确用户名和密码登录")  # 用例标题
    @allure.severity(allure.severity_level.CRITICAL)  # 优先级
    def test_login_success(self):
        with allure.step("输入用户名"):
            print("输入admin")
        with allure.step("输入密码"):
            print("输入123456")
        with allure.step("点击登录按钮"):
            print("点击登录")
        assert 1 == 1

    @allure.story("登录失败")
    @allure.title("验证错误密码登录")
    def test_login_fail(self):
        allure.dynamic.description("这是一个动态描述的示例")  # 动态添加描述
        assert 1 == 2