"""
@Author:xuyinglai
@Date:2026/10/22
@DESC:
"""
import asyncio

async def task1():
    print("A：任务1开始")
    await asyncio.sleep(3)
    print("D：任务1结束")

async def task2():
    print("B：任务2开始")
    await asyncio.sleep(2)
    print("C：任务2结束")

async def main():
    await asyncio.gather(task1(), task2())

if __name__ == '__main__':

    asyncio.run(main())