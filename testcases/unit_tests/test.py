import asyncio

async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")
    return f"Result-{name}"

async def main():
    # 并发运行 3 个任务
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )
    print("All done:", results)  # 输出所有任务的结果

asyncio.run(main())