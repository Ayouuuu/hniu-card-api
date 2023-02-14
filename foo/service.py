from pyquery import PyQuery as pq
from foo.pojo.studeninfo import StudentInfo


import requests
import time
import ujson

"""
验证码
个人信息
自助缴费
费用查询
"""
url = [
    "http://10.14.0.124/zytk35portal/AuthCode.aspx",
    "http://10.14.0.124/zytk35portal/Cardholder/Cardholder.aspx",
    "http://10.14.0.124/zytk35portal/Cardholder/SelfHelp.aspx",
    "http://10.14.0.124/zytk35portal/ajaxpro/Zytk30Portal.Cardholder.SelfHelp,App_Web_selfhelp.aspx.67bdbcc7.ashx"
]


async def authcode(cookie: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie
    }
    response = requests.get(url[0], headers=headers, stream=True)
    with open('test2.png', 'wb') as file:
        for data in response.iter_content(128):
            file.write(data)
    print(response.status_code)
    return response.status_code

def get_user_info(cookie: str):
    headers = {
        'Cookie': cookie,
    }
    response = requests.get(url[1], headers=headers)
    doc = pq(response.text)
    studentInfo = StudentInfo(doc)
    studentInfo.createTime = (int(time.time()))
    return studentInfo.__dict__


def get_areas(cookie: str):
    headers = {
        'Cookie': cookie
    }
    response = requests.get(url[2], headers=headers)
    doc = pq(response.text)
    # doc = pq(filename=".idea/httpRequests/2022-04-04T143732.200.html")
    areas = doc.find("#lsArea").items("option")
    arr = []
    for area in areas:
        arr.append({
            'id': area.attr('value'),
            'name': area.text()
        })
    return arr


def get_houses(area_id: str, cookie: str):
    headers = {
        'Cookie': cookie,
        'X-AjaxPro-Method': "GetHouseList",
        "Content-Type": "text/plain"
    }
    data = {
        "AreaId": area_id
    }
    response = requests.post(url[3], headers=headers, data=ujson.dumps(data))
    text = ujson.loads(response.text.replace(
        "new Ajax.Web.DataSet([new Ajax.Web.DataTable([[\"showvalue\",\"System.String\"],[\"showname\",\"System.String\"]],",
        "").replace(")]);/*", ""))
    array = []
    for arr in text:
        array.append({
            'id': arr[0],
            'name': arr[1]
        })
    return array


def get_rooms(area_id, house_id, cookie):
    headers = {
        'Cookie': cookie,
        'X-AjaxPro-Method': "GetRoomList",
        "Content-Type": "text/plain"
    }
    data = {
        "areaId": area_id,
        "HouseId": house_id
    }
    response = requests.post(url[3], headers=headers, data=ujson.dumps(data))
    text = ujson.loads(response.text.replace(
        "new Ajax.Web.DataSet([new Ajax.Web.DataTable([[\"MeterID\",\"System.Int32\"],[\"Remnant\",\"System.Decimal\"],[\"showname\",\"System.String\"],[\"room_id\",\"System.String\"]],",
        "").replace(")]);/*", ""))
    array = []
    for arr in text:
        array.append({
            'id': arr[0],
            'money': arr[1],
            'id': arr[2],
        })
    return array
