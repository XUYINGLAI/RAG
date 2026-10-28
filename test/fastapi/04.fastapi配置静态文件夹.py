"""
@Author:xuyinglai
@Date:2026/10/26
@DESC:
"""
import pathlib

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


app=FastAPI()





# todo 静态挂载 前后端不分离 前端文件都得写在static文件夹下 也是:8000
# 当前文件目录
BASE_DIR = pathlib.Path(__file__).parent
print("当前文件目录：", BASE_DIR)
static_dir = BASE_DIR / "static"

# 挂载静态文件
# 第一个参数：所有以 /static 开头的请求都交给这个模块处理
# 第二个参数：指定静态文件的存放目录
# 第三个参数：给挂载点起个名字（路由的名字）
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# todo 跨域解决的中间件
# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有来源访问
    allow_credentials=False,   # 不允许携带跨域凭证
    allow_methods=["*"],       # 允许所有请求方法
    allow_headers=["*"],       # 允许所有请求头
)

@app.get("/hello")
def hello():
    return {"hello":"world999999999999999999999999999999999999999999999999999999"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)


# todo 跨域

