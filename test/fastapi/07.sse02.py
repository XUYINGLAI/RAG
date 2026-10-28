"""
@Author:xuyinglai
@Date:2026/10/26
@DESC:
"""
import time

import uvicorn
##### 场景2：异步任务+发送post请求

# 目标：后端先接收查询请求，后台处理，SSE 推送处理结果
#
# 案例2 使用post请求加异步操作
# 	1、前端发请求传递一个query，再传递一个session_id  两个参数到后端进行请求体接收
# 	2、后端写一个接口获取这两个参数，并返回给前端收到的消息，并启动task造消息
# 	3、前端订阅sse请求
# 	4、服务端需要写sse回复接口，从task当中获取自己的队列，从队列当中一个一个yield答案


from fastapi import FastAPI, BackgroundTasks, Body, Query
from pydantic import BaseModel, Field

from starlette.middleware.cors import CORSMiddleware
from asyncio import Queue

from starlette.responses import StreamingResponse
import asyncio         

app = FastAPI()
# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源访问
    allow_credentials=False,   # 不允许携带跨域凭证
    allow_methods=["*"],       # 允许所有请求方法
    allow_headers=["*"],       # 允许所有请求头
)
class BodyParams(BaseModel):
    query:str = Field(...,description="查询内容")
    session_id:str=Field(...,description="会话ID")
q_dict={}
async def make_data(query:str,session_id:str):
    if q_dict.get(session_id) is None:
        q_dict[session_id]=Queue()
    q=q_dict[session_id]
    await  q.put("我是")
    await  q.put("我")
    await  q.put("l")
    await  q.put("y")
    await  q.put("x")
    await  q.put(None)


@app.post("/sse02")
def sse02(
        background_tasks: BackgroundTasks,
        body_params: BodyParams,
):
    query = body_params.query
    session_id = body_params.session_id

    background_tasks.add_task(make_data,query,session_id)


    return {
        "message":"hello"
    }

@app.get("/handlersse02")
async def handlersse02(
        session_id:str=Query(...,description="会话session_id"),
):
    async def generate_data():
        while q_dict.get(session_id) is None:
            await asyncio.sleep(1)
        q=q_dict.get(session_id)
        while True:
            data=await q.get()
            await asyncio.sleep(1)
            yield f"data: {data}\n\n"

            if data is None:
                break


    return StreamingResponse(generate_data(),media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
