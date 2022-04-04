# HNIU 校园一卡通API

_该脚本仅适用于 **HNIU** 校园一卡通服务_   
基于 **Python FastAPI** HNIU 校园一卡通 API 后端

## 程序功能

- 获取用户信息
- 获取各个寝室电费

## 如何使用

下载项目

```shell
git clone
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

## 项目地址

```text
http://127.0.0.1:8000
```

文档地址

```text
http://127.0.0.1:8000/docs
```