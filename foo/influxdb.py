import json,time

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point, WritePrecision

bucket = ""
org = ""
token = ""
url = ""
# 代理，不需要可以删除
proxy = "http://localhost:7890"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, proxy=proxy)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_point(data):
    data = json.loads(data)
    points = []
    for room in data['rooms']:
        point = {
            "measurement": "room",
            "tags": {
                "area_id": data['area_id'],
                "house_id": data['house_id'],
                "room_id": room['id']
            },
            "fields": {
                "money": float(room["money"])
            }
        }
        db_point = Point.from_dict(point, WritePrecision.NS)
        points.append(db_point)
    try:
        write_api.write(bucket=bucket, record=points)
        print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()), "successfully write", data["area_id"], "data:", points.__sizeof__())
    except Exception:
        print("write failed 请检查您的网络", "area_id: ", data["area_id"], "house_id", data["house_id"])


def write_areas(data):
    data = json.loads(data)
    points = []
    for area in data:
        point = {
            "measurement": "area",
            "tags": {
                "id": area["id"]
            },
            "fields": {
                "name": area["name"]
            }
        }
        db_point = Point.from_dict(point, WritePrecision.NS)
        points.append(db_point)
    write_api.write(bucket=bucket, record=points)


def write_houses(data):
    data = json.loads(data)
    points = []
    for house in data['houses']:
        point = {
            "measurement": "house",
            "tags": {
                "area_id": data['area_id'],
                "id": house["id"]
            },
            "fields": {
                "name": house["name"]
            }
        }
        points.append(Point.from_dict(point, WritePrecision.NS))
    write_api.write(bucket=bucket, record=points)
# query code
# query_api = client.query_api()
# query = 'from(bucket: "bucket") |> range(start: -10m) |> filter(fn: (r) => r["_measurement"] == "dex_screener") '
#
# result = query_api.query(org=org, query=query)
# for table in result:
#     for record in table.records:
#         print(record.values)
