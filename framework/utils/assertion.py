

from typing import Any, Optional


class AssertionError(Exception):
    """自定义断言错误，提供更详细的错误信息"""
    pass


def assert_equal(field_name: str, expected: Any, actual: Any, message: Optional[str] = None) -> None:
    """
    断言两个值相等

    Args:
        field_name: 字段名称，用于错误信息
        expected: 期望值
        actual: 实际值
        message: 自定义错误消息
    """
    if expected != actual:
        error_msg = message or f"字段 '{field_name}' 不匹配: 预期值 '{expected}', 实际值 '{actual}'"
        raise AssertionError(error_msg)


def assert_str(field_name: str, expected: Any, actual: Any, message: Optional[str] = None) -> None:
    """
    断言两个字符串相等，会将值转换为字符串后比较

    Args:
        field_name: 字段名称，用于错误信息
        expected: 期望值
        actual: 实际值
        message: 自定义错误消息
    """
    expected_str = str(expected) if expected is not None else None
    actual_str = str(actual) if actual is not None else None
    assert_equal(field_name, expected_str, actual_str, message)


def assert_not_none(field_name: str, value: Any, message: Optional[str] = None) -> None:
    """
    断言值不为None

    Args:
        field_name: 字段名称，用于错误信息
        value: 要检查的值
        message: 自定义错误消息
    """
    if value is None:
        error_msg = message or f"字段 '{field_name}' 为 None"
        raise AssertionError(error_msg)


def assert_is_none(field_name: str, value: Any, message: Optional[str] = None) -> None:
    """
    断言值为None

    Args:
        field_name: 字段名称，用于错误信息
        value: 要检查的值
        message: 自定义错误消息
    """
    if value is not None:
        error_msg = message or f"字段 '{field_name}' 不为 None: '{value}'"
        raise AssertionError(error_msg)


def assert_in(field_name: str, value: Any, container: Any, message: Optional[str] = None) -> None:
    """
    断言值在容器中

    Args:
        field_name: 字段名称，用于错误信息
        value: 要检查的值
        container: 容器（列表、集合、字典等）
        message: 自定义错误消息
    """
    if value not in container:
        error_msg = message or f"字段 '{field_name}' 的值 '{value}' 不在容器中"
        raise AssertionError(error_msg)


def assert_not_in(field_name: str, value: Any, container: Any, message: Optional[str] = None) -> None:
    """
    断言值不在容器中

    Args:
        field_name: 字段名称，用于错误信息
        value: 要检查的值
        container: 容器（列表、集合、字典等）
        message: 自定义错误消息
    """
    if value in container:
        error_msg = message or f"字段 '{field_name}' 的值 '{value}' 在容器中"
        raise AssertionError(error_msg)


def assert_true(field_name: str, condition: bool, message: Optional[str] = None) -> None:
    """
    断言条件为True

    Args:
        field_name: 字段名称，用于错误信息
        condition: 要检查的条件
        message: 自定义错误消息
    """
    if not condition:
        error_msg = message or f"条件 '{field_name}' 不为 True"
        raise AssertionError(error_msg)


def assert_false(field_name: str, condition: bool, message: Optional[str] = None) -> None:
    """
    断言条件为False

    Args:
        field_name: 字段名称，用于错误信息
        condition: 要检查的条件
        message: 自定义错误消息
    """
    if condition:
        error_msg = message or f"条件 '{field_name}' 不为 False"
        raise AssertionError(error_msg)


def assert_length(field_name: str, value: Any, expected_length: int, message: Optional[str] = None) -> None:
    """
    断言值的长度等于预期长度

    Args:
        field_name: 字段名称，用于错误信息
        value: 要检查的值（需要支持len()函数）
        expected_length: 预期长度
        message: 自定义错误消息
    """
    actual_length = len(value) if hasattr(value, '__len__') else None
    if actual_length is None:
        error_msg = message or f"字段 '{field_name}' 不支持长度操作"
        raise AssertionError(error_msg)

    if actual_length != expected_length:
        error_msg = message or f"字段 '{field_name}' 的长度不匹配: 预期 {expected_length}, 实际 {actual_length}"
        raise AssertionError(error_msg)
