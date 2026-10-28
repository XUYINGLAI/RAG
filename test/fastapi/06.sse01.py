"""
@Author:xuyinglai
@Date:2026/10/26
@DESC:
"""
import time
from queue import Queue

import uvicorn
# 案例1
#   1、客户前端发ajax请求要发邮件并携带session_id，服务端直接回复收到，制造邮件开始
# 	2、服务端就开始执行backgroundtask当中造邮件的函数，造的邮件全部放在队列当中
        # 队列必须按照session_id，每人创建一个Queue {id1:queue1(),id2:queue2(),id3:queue3() }
# 	3、客户端想直接拿到造的邮件内容，造一个拿一个，那么客户端需要去发送订阅sse请求
# 	4、服务端需要写sse回复接口，流式返回，流式返回就是把一个生成器对象返回生成器函数当中就是从queue_dict当中获取自己session_id的队列，从队列当中一个一个yield球
#
#注意：每个session_id对应自己的邮件队列

from fastapi import FastAPI, Query, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

app = FastAPI()

# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源访问
    allow_credentials=False,   # 不允许携带跨域凭证
    allow_methods=["*"],       # 允许所有请求方法
    allow_headers=["*"],       # 允许所有请求头
)
q_dict={}
def male_email(session_id:str):
    # 创建队列
    if session_id not in q_dict:
        q_dict[session_id]=Queue() # 同步队列
    q=q_dict.get(session_id)
    q.put(f"邮件1{session_id}")
    q.put(f"邮件2{session_id}")
    q.put(f"邮件3{session_id}")
    q.put(f"邮件4{session_id}")
    q.put(f"邮件5{session_id}")
    q.put(f"邮件6{session_id}")
    q.put(None)

@app.get("/sse01")
def sse01(
        background_tasks: BackgroundTasks,
        session_id:str=Query(...,description="会话id"),

):
    background_tasks.add_task(male_email,session_id)

    return {
        "message":"收到id，开始制造邮件"
    }
# 在这里定义生成器函数
def generate_data(session_id:str):
    # 从队列里面获取邮件 一个一个的yield
    while q_dict.get(session_id) is None:
        time.sleep(1)
    q=q_dict.get(session_id)
    while True:
        data=q.get()
        yield f"data: {data}\n\n" # 必须符合sse规范
        if data is None:
            break

# 处理sse
@app.get("/handersse01")
def handersse01(
        session_id:str=Query(...,description="会话id")
):
    return StreamingResponse(generate_data(session_id),media_type="text/event-stream") # 流失响应对象

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)