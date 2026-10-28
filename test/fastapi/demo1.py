"""
@Author:xuyinglai
@Date:2026/10/23
@DESC:
"""
import pathlib
import shutil
from typing import Any

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Depends, File, UploadFile
from fastapi import Request
import uuid

# 创建应用
app=FastAPI(
    title="路径参数学习",
    description="写在网址的数据传入Python变量",
    version="0.1.0",
)
# todo 路径参数
@app.get("/testpath/{id}/{name}/{gender}")
def testpath(
        id: int,
        name: str=Path(description="姓名"),
        gender: str = Path( description="性别")
):
    # 在运行程序的终端观察参数值和类型
    print("id=",id,"类型：",type(id))
    print("name=",name,"类型：",type(name))
    print("gender=",gender,"类型：",type(gender))

    # 返回给客户端的数据 JSON格式返回浏览器
    return {
        "id": id,
        "name": name,
        "gender": gender
    }

# todo 查询参数：对于这里这种 str、int 等普通标量参数，
#  如果它不在路径模板里，也没有另外指定来源，FastAPI 会把它当作查询参数。
@app.get("/hello")
def hello(name:str): # 不要把 ?name=... 写进路由装饰器里。参数由函数声明接收。
    print("我拿到的name是:",name)
    return {"message":f"你好{name}"}

@app.get("/hello2")
def hello(name:str= "我是默认值"): # 不要把 ?name=... 写进路由装饰器里。参数由函数声明接收。
    print("我拿到的name是:",name)
    return {"message":f"你好{name}"}

@app.get("/search")
def search(
        keyword:str=Query(...,description="搜索关键词",min_length=1),
        page:int=Query(default=1,description="页码",ge=1),
):
    print("keyword:",keyword,type(keyword))
    print("page:",page,type(page))

    return{
        "keyword":keyword,
        "page":page,
    }
# todo 请求体参数 一般传递JSON 和 表单类型(用户界面输入或上传文件)
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str=Field(title="用户的名字",description="名称",min_length=2)  # 在这里对name做限制，
    age:int=Field(title="用户的年龄",description="年龄",gt=0,le=100,default=18)

# 这里不能用get请求，无法使用浏览器测试，使用postman
@app.post("/testbody")
def testbody(
    user: User=Body(...,description="请求参数用户信息") # 不能写限制 :str             Body()是用来限制user整体必须是请求体参数
):
    print(user,type(user))  # 用User类做校验，会实例化一个对象
    return{
        "user":user, # 返回的不管是字典还是对象，都会被默认序列化成json串，长得一样
    }

###############################################################

class User1(BaseModel):
    username:str = Field(
        title= "用户民",
        description="用户的姓名"
    )
    age:int = Field(
        default=18,
        title="年龄",
        description="用户的年龄",
        gt=0,
        le=100,
    )

@app.post("/testUser1")
def testUser1(
        user:User1=Body()# 在这里用类 来做限制 user现在是Pydantic的对象
    ):

    print("收到的对象:",user)
    print("收到的对象类型:",type(user))
    print("用户名:",user.username,type(user.username))
    return user


# 四 todo 混合接受参数

class UserInfo(BaseModel):
    username:str = Field(...,description="用户名",min_length=2)
    password:str = Field(...,description="密码",min_length=6)
@app.post("/testmix/{id}")
def testmix(
        id: int = Path(..., description="用户id", gt=0, le=100), # 路径参数
        name:str=Query(...,description="用户名称",min_length=2),# 查询参数
        age:int=Query(...,description="年龄",gt=0,le=100),
        user_info:UserInfo=Body(...,description="用户信息"), # 请求体参数
):

    return{
        "id": id,
        "name": name,
        "age": age,
        "user_info": user_info
    }


# todo 混合接收参数可以分成两大类  键值对参数    请求体参数  把‘键值对参数’也封装成一个类

class UserInfo(BaseModel):
    username:str = Field(...,description="用户名",min_length=2)
    password:str = Field(...,description="密码",min_length=6)

class KeywordParams(BaseModel):
    def __init__(self, id,name,age):
        self.id = id
        self.name = name # 要是校验限制，得自己在这里写
        self.age = age

@app.post("/testmix/{id}")
def testmix(
        key_word_params:KeywordParams=Depends(KeywordParams),# 让fastapi自己解析
        user_info:UserInfo=Body(...,description="用户信息"), # 请求体参数
):

    return{
        "id": key_word_params.id,
        "name": key_word_params.name,
        "age": key_word_params.age,
        "user_info": user_info
    }

# todo 五 接收请求头信息


@app.get("/testheader")
def testheader(request: Request): # 把请求报文当成对象来解析
    # print(request.headers) # Headers({'token': '12345678987654', 'postman-token': '5104c16c-1870-4074-9e5c-deb436ad7dc6', 'host': 'localhost:8000', 'user-agent': 'PostmanRuntime/2.12.2', 'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'connection': 'keep-alive'})
    print(request.headers.get("token"))
    return {
        "token": request.headers.get("token")
    }


# todo 六 接收表单 前端上传文件 必须是post
@app.post("/upload")
def upload(file:UploadFile=File(...,description="12344444444")): # 也是解析成一个对象
    # 接收文件后 先本地存储，再转储
    print("file:",file)
    # print(type(file))
    # print(file.filename,type(file.filename))
    # print(file.headers,type(file.headers))
    img_dir="./images"
    img_dir_obj=pathlib.Path(img_dir)
    if not img_dir_obj.exists():
        img_dir_obj.mkdir(parents=True,exist_ok=True)
    file_name=str(uuid.uuid4())[:9]+file.filename
    print(file_name)
    with open(img_dir_obj / file_name,"wb") as f:
        # f.write(file.file.read()) f是新建的文件代指
        shutil.copyfileobj(file.file,f,1024*1024*10) # 10MB 一次读入再写本地
        pass



if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
