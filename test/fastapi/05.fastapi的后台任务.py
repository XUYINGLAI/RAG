"""
@Author:xuyinglai
@Date:2026/10/26
@DESC:
"""
import time

import uvicorn
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def print_lova(n):
    while n > 0:
        print("i love u")
        time.sleep(2)
        n-=1

@app.get("/backgroundtask")
def backgroundtask(background_tasks: BackgroundTasks):
    background_tasks.add_task(print_lova,10) # 没有在这里阻塞，
    return {"message": "后台任务在执行"}



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)