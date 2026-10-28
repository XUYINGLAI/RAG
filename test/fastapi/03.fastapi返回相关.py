"""
@Author:xuyinglai
@Date:2026/10/26
@DESC:
"""
import pathlib

import uvicorn

from fastapi import FastAPI
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

# todo 一.返回json 在return后面跟上python数据，一般是字典或对象 或字典列表 对象列表
#结果作为JsonResponse的content
@app.get("/returnjson")
def returnjson():

    # return {"hello":"world"}
    return JSONResponse(status_code=200,
                        content={"hello":"world"},
                        media_type="application/json",
                        )# 全写长这样

# todo 返回文件
@app.get("/download")
async def download():
    return FileResponse(r"C:\Users\23716\Music\伊雷娜.png",
                        media_type="image/png",
                        headers={"Content-Disposition":"attachment;filename=666.png"}
                        )

# todo 返回html

from fastapi.responses import HTMLResponse

@app.get("/hello")
def hello(name: str = "游客"):
    html_content = f"""
    <html>
        <body>
            <h1>你好，{name}！</h1>  
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# todo 返回纯文本
from fastapi.responses import PlainTextResponse

@app.get("/text")
async def get_text():
    return PlainTextResponse(content="这是纯文本响应", status_code=200)


# todo 重定向
from fastapi.responses import RedirectResponse

@app.get("/old-path")
async def redirect_old_path():
    # 重定向到 /new-path，状态码 307 表示临时重定向
    return RedirectResponse(url="/new-path", status_code=307)

@app.get("/new-path")
async def new_path():
    return {"message": "这是新接口"}


# todo 返回任意类型响应 Response
from fastapi.responses import Response

@app.get("/custom")
async def custom_response():
    # 返回二进制数据，指定自定义 MIME 类型
    return Response(
        content="<h1>纯文本</h1>",
        # media_type="text/plain",# 纯文本对待
        # media_type="text/html",
        media_type="application/json",
        status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)