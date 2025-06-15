import allure
from allure_commons.types import AttachmentType


class AllureManager:
    """Allure测试报告辅助工具类，提供在测试过程中添加各种类型附件和步骤的静态方法"""

    @staticmethod
    def attach_screenshot(name, driver):
        """
        截取当前浏览器页面并附加到Allure报告中

        Args:
            name: 截图在报告中的显示名称
            driver: WebDriver实例，用于执行截图操作
        """
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG
        )

    @staticmethod
    def step(step_title):
        """
        在Allure报告中创建一个测试步骤

        Args:
            step_title: 步骤的标题描述

        Returns:
            allure.step对象，可作为上下文管理器使用
        """
        return allure.step(step_title)

    @staticmethod
    def attach_response_data(response):
        """
        将API响应数据附加到Allure报告中，包括状态码、响应头和响应体

        Args:
            response: HTTP响应对象，通常来自requests库
        """
        allure.attach(
            f"Status: {response.status_code}\nHeaders: {response.headers}\nBody: {response.text}",
            name="API Response",
            attachment_type=AttachmentType.TEXT
        )
