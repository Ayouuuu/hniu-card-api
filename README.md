# HNIU 校园一卡通API
![GitHub](https://img.shields.io/github/license/Ayouuuu/hniu-card-api?color=green&style=flat-square)
![Forks](https://img.shields.io/github/forks/Ayouuuu/hniu-card-api?color=green&style=flat-square)
![Stars](https://img.shields.io/github/stars/Ayouuuu/hniu-card-api?color=green&style=flat-square)

_该脚本仅适用于 **HNIU** 校园一卡通服务_   
基于 **Python FastAPI** HNIU 校园一卡通 API 后端

## 程序功能

- 获取用户信息
- 获取各个寝室电费

## 如何使用

下载项目

```shell
git clone https://github.com/Ayouuuu/hniu-card-api.git
cd hniu-card-api
```

安装依赖

```shell
pip install -r requirements.txt
```

运行程序

```shell
python -m uvicorn main:app --reload
```

如果无法运行, 请安装 `uvicorn` 依赖

```shell
# 以下选择一种即可
pip install uvicorn
pip install uvicorn[standard]
```

## 接口使用

文档地址

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

登陆 [一卡通](http://10.14.0.124/zytk35portal/Cardholder/Cardholder.aspx) 按 F12 进入网页控制台，点击 Network(网络) 找到 `Cardholder.aspx` 文件 `Headers->Request Headers->Cookie` 然后复制
获取用户信息
```text
http://127.0.0.1:8000/info

请求头 
Cookie: 你复制的 cookie 值
```
返回
```json
{
  "name": "",
  "sex": "",
  "partment": "",
  "identity": "",
  "userId": "",
  "cardNum": "",
  "cardId": "",
  "money": "",
  "date": "",
  "status": "",
  "certCode": "",
  "cardType": "",
  "certType": "",
  "createTime": 1649074521
}
```
获取楼栋号列表
```text
http://127.0.0.1:8000/selfhelp/areas

请求头
Cookie: 你复制的 cookie 值
```
返回
```json
[
  {
    "id": "001005",
    "name": "10号楼"
  },
  {
    "id": "001006",
    "name": "23号楼"
  }
]
```

获取楼层号列表
```text
http://127.0.0.1:8000/selfhelp/houses?area_id=楼栋号id

请求头
Cookie: 你复制的 cookie 值
```
返回
```json
[
  {
    "id": "001005002",
    "name": "2楼"
  },
  {
    "id": "001005003",
    "name": "3楼"
  }
]
```
获取当前楼层所有房间信息
```text
http://127.0.0.1:8000/selfhelp/rooms?area_id=楼栋号id&house_id=楼层号id

请求头
Cookie: 你复制的 cookie 值
```
返回
```json
[
  {
    "id": "10-601",
    "money": 78.34,
    "name": "10-601"
  },
  {
    "id": "10-602",
    "money": 54.14,
    "name": "10-602"
  }
]
```
