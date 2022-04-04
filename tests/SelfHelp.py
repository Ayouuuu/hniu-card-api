from pyquery import PyQuery as pq
import requests

url = "http://10.14.0.124/zytk35portal/ajaxpro/Zytk30Portal.Cardholder.SelfHelp,App_Web_selfhelp.aspx.67bdbcc7.ashx"
#
# def get_house_list:
#
#
# def get_room_list:
#
#
# def set_room_num:


if __name__ == '__main__':
    doc = pq(filename="../.idea/httpRequests/2022-04-04T173309.200.html")

    # url = "http://10.14.0.124/zytk35portal/Cardholder/SelfHelp.aspx"
    # headers = {
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "Cookie": "ASP.NET_SessionId=ywvujrgpl1ndxoxuc12yxy01"
    # }
    # selfhelp = requests.get(url, headers=headers)
    # text = selfhelp.text
    # doc = pq(text)
    areas = doc.find("#lsArea").items("option")
    arr = []
    for area in areas:
        print(area.attr("value"))
    print(arr)
