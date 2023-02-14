from fastapi import FastAPI, Header, Query

from typing import Optional
from starlette.responses import Response
from foo.service import *

app = FastAPI()

"登陆"


@app.post("/login", description="登陆,初始化 cookie")
async def login(response: Response, username: str, password: str):
    code = authcode()
    response.set_cookie(key=KEY, value=code[1])
    info = auth_login(username, password, code[0], KEY + "=" + code[1])
    return {"userinfo": info, "cookie": code[1]}


"获取用户信息"


@app.get("/info", description="获取用户信息，初始化 cookie ")
async def info(Cookie: Optional[str] = Header(None)):
    return get_user_info(Cookie)


"获取楼栋号列表"


@app.get("/selfhelp/areas", description="获取楼栋号列表")
async def selfhelp_areas(Cookie: Optional[str] = Header(None)):
    return get_areas(Cookie)


"获取楼层号列表"


@app.get("/selfhelp/houses", description="获取楼层号列表")
async def selfhelp_houses(area_id: str = Query(..., description="楼栋号id"), Cookie: Optional[str] = Header(None)):
    return get_houses(area_id, Cookie)


"获取当前楼层所有房间余额"


@app.get("/selfhelp/rooms", description="获取当前楼层所有房间余额")
async def selfhelp_room(area_id: str = Query(..., description="楼栋号id"),
                        house_id: str = Query(..., description="楼层号id"),
                        Cookie: Optional[str] = Header(None)):
    return get_rooms(area_id, house_id, Cookie)
