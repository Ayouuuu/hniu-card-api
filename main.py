from fastapi import FastAPI, Query

from starlette.responses import Response
from foo.service import *

app = FastAPI()

"登陆"


@app.post("/login", description="登陆,初始化 cookie")
async def login(response: Response, username: str, password: str):
    code = authcode()
    response.set_cookie(key=KEY, value=code[1])
    info = auth_login(username, password, code[0])
    if info['name'] == '':
        return {"code": 403, "message": "无法获取登陆信息，请再次尝试或等待几分钟"}
    return {"userinfo": info, "cookie": code[1]}


"获取用户信息"


@app.get("/info", description="获取用户信息，初始化 cookie ")
async def info():
    return get_user_info()


"获取楼栋号列表"


@app.get("/selfhelp/areas", description="获取楼栋号列表")
async def selfhelp_areas():
    return get_areas()


"获取楼层号列表"


@app.get("/selfhelp/houses", description="获取楼层号列表")
async def selfhelp_houses(area_id: str = Query(..., description="楼栋号id")):
    return get_houses(area_id)


"获取当前楼层所有房间余额"


@app.get("/selfhelp/rooms", description="获取当前楼层所有房间余额")
async def selfhelp_room(area_id: str = Query(..., description="楼栋号id"),
                        house_id: str = Query(..., description="楼层号id")):
    return get_rooms(area_id, house_id)


@app.get("/write/rooms", description="""写入当前楼栋所有房间余额
    一般为宿舍楼 001001-001012""")
async def write_room_data(area_id: str = Query(..., description="楼栋号id")):
    return write_room(area_id)