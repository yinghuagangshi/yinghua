# test_async.py
import pytest
import asyncio

async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")
    return f"Result-{name}"

@pytest.mark.asyncio  # 需要安装 pytest-asyncio
async def test_main():
    results = await asyncio.gather(
        task("A", 0.1),  # 测试时缩短等待时间
        task("B", 0.1),
        task("C", 0.1),
    )
    assert results == ["Result-A", "Result-B", "Result-C"]
    print("All done:", results)