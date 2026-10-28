"""
@Author:xuyinglai
@Date:2026/10/25
@DESC:
"""
import uvicorn
from fastapi import FastAPI, Path, Query, Body

# 创建应用
app=FastAPI(
    title="路径参数学习",
    description="写在网址的数据传入Python变量",
    version="0.1.0",
)


@app.post("/testbody")
def tsetbody(
        user=Body(...,default="用户信息") # 这里不能写str限制

):
    print(user,type(user) )
    return{
        "user":user
    }
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)