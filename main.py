from fastapi import FastAPI, Header, Query

from typing import Optional
from foo.service import *

app = FastAPI()

"获取用户信息"


@app.get("/info", description="获取用户信息")
async def info(cookie: Optional[str] = Header(None)):
    print(cookie)
    return get_user_info(cookie)


"获取楼栋号列表"


@app.get("/selfhelp/areas", description="获取楼栋号列表")
async def selfhelp_areas(cookie: Optional[str] = Header(None)):
    return get_areas(cookie)


"获取楼层号列表"


@app.get("/selfhelp/houses", description="获取楼层号列表")
async def selfhelp_houses(area_id: str = Query(..., description="楼栋号id"), cookie: Optional[str] = Header(None)):
    return get_houses(area_id, cookie)


"获取当前楼层所有房间余额"


@app.get("/selfhelp/rooms", description="获取当前楼层所有房间余额")
async def selfhelp_room(area_id: str = Query(..., description="楼栋号id"),
                        house_id: str = Query(..., description="楼层号id"),
                        cookie: Optional[str] = Header(None)):
    return get_rooms(area_id, house_id, cookie)
