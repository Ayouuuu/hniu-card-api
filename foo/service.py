from pyquery import PyQuery as pq
from foo.pojo.studeninfo import StudentInfo
from foo.util import ocr_code
from foo.influxdb import *

import requests
import time
import ujson
import threading

"""
验证码
个人信息
自助缴费
费用查询
登陆
"""
url = [
    "http://10.14.0.124/zytk35portal/AuthCode.aspx",
    "http://10.14.0.124/zytk35portal/Cardholder/Cardholder.aspx",
    "http://10.14.0.124/zytk35portal/Cardholder/SelfHelp.aspx",
    "http://10.14.0.124/zytk35portal/ajaxpro/Zytk30Portal.Cardholder.SelfHelp,App_Web_selfhelp.aspx.67bdbcc7.ashx",
    "http://10.14.0.124/zytk35portal/default.aspx"
]

KEY = "ASP.NET_SessionId"
session = requests.Session()

"""
获取验证码
"""


def authcode():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    response = requests.get(url[0], headers=headers, stream=True)
    with open('code.png', 'wb') as file:
        for data in response.iter_content(128):
            file.write(data)
    cookie = response.cookies.get(KEY)
    session.cookies.set(KEY, cookie)
    return [ocr_code("code.png").upper(), cookie]


"登陆"


def auth_login(username: str, password: str, code: str):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "http://10.14.0.124/zytk35portal/default.aspx",
    }
    session.post(url[4], headers=headers, data="__EVENTTARGET=UserLogin%24ImageButton1&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTc0MDQ4ODc3Nw9kFgICAQ9kFhICAw8WAh4HVmlzaWJsZWhkAgUPFgIfAGhkAgcPFgIfAGhkAgkPPCsACQEADxYEHghEYXRhS2V5cxYAHgtfIUl0ZW1Db3VudGZkZAIODzwrAAkBAA8WBB8BFgAfAmZkZAIQDzwrAAkBAA8WBB8BFgAfAmZkZAISDzwrAAkBAA8WBB8BFgAfAmZkZAIUDzwrAAkBAA8WBB8BFgAfAmZkZAIWDzwrAAkBAA8WBB8BFgAfAmZkZGT7t2PaAC71nhjomcWWlS2Kl%2FDh6Icnffmmf1QCBjcqOg%3D%3D&__VIEWSTATEGENERATOR=E655DDB2&__EVENTVALIDATION=%2FwEdAAmmkB23XPRc6QJjrAxJx7jUohjo8sIky4Xs%2BCUBsum%2BnL6pRh%2FvC3eYiguVzFy%2FtEYvT53BE9ULYNj8jfQiCQeC35ZbbeGbJddowj1pY7sNivrI0G85IvfKPX4CghIMZ1NJ4PbCb80KUDHFYYKXgFT9PjMyUg6NAZP4%2BvrIPkQUuFOdcKl43UA3HbIoQpEPelhEPm0OSqwYeIaEyD7zfAzjHEWZ1PjzcAqdQtFUyg1jBg%3D%3D&UserLogin%3AtxtUser=" + username + "&UserLogin%3AtxtPwd=" + password + "&UserLogin%3AddlPerson=%BF%A8%BB%A7&UserLogin%3AtxtSure=" + code)
    info = get_user_info()
    return info


"获取用户信息"


def get_user_info():
    response = session.get(url[1])
    doc = pq(response.text)
    studentInfo = StudentInfo(doc)
    studentInfo.createTime = (int(time.time()))
    return studentInfo.__dict__


def get_areas():
    response = session.get(url[2])
    doc = pq(response.text)
    areas = doc.find("#lsArea").items("option")
    arr = []
    for area in areas:
        arr.append({
            'id': area.attr('value'),
            'name': area.text()
        })
    return arr


def get_houses(area_id: str):
    headers = {
        'X-AjaxPro-Method': "GetHouseList",
        "Content-Type": "text/plain"
    }
    data = {
        "AreaId": area_id
    }
    response = session.post(url[3], headers=headers, data=ujson.dumps(data))
    text = ujson.loads(response.text.replace(
        "new Ajax.Web.DataSet([new Ajax.Web.DataTable([[\"showvalue\",\"System.String\"],[\"showname\",\"System.String\"]],",
        "").replace(")]);/*", ""))
    array = []
    for arr in text:
        array.append({
            'id': arr[0],
            'name': arr[1]
        })

    d = {
        "area_id": area_id,
        "houses": array
    }
    return d


def get_rooms(area_id, house_id):
    headers = {
        'X-AjaxPro-Method': "GetRoomList",
        "Content-Type": "text/plain"
    }
    data = {
        "areaId": area_id,
        "HouseId": house_id
    }
    response = session.post(url[3], headers=headers, data=ujson.dumps(data))
    text = ujson.loads(response.text.replace(
        "new Ajax.Web.DataSet([new Ajax.Web.DataTable([[\"MeterID\",\"System.Int32\"],[\"Remnant\",\"System.Decimal\"],[\"showname\",\"System.String\"],[\"room_id\",\"System.String\"]],",
        "").replace(")]);/*", ""))
    array = []
    for arr in text:
        arr[1] = arr[1] if arr[1] is not None else 0
        array.append({
            'id': arr[0],
            'money': arr[1],
            'id': arr[2],
        })
    data = {
        "area_id": area_id,
        "house_id": house_id,
        "create_time": int(round(time.time() * 1000)),
        "rooms": array
    }
    return data


def write_room(area_id: str):
    try:
        get_areas()
        houses = get_houses(area_id)
        for house in houses["houses"]:
            threading.Thread(target=write_point, args=(json.dumps(get_rooms(area_id, house['id'])),)).start()
            time.sleep(1)
        return {"code": 200, "message": "写入成功"}
    except Exception as e:
        return {"code": "500",
                "message": "写入失败,请检查网络或者influxdb是否正常运行,以及电费网站是否可正常访问，如不能访问需要等待半小时或者更长！"}
