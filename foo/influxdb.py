import json

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point, WritePrecision

bucket = ""
org = ""
token = ""
url = ""

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, proxy="http://localhost:7890")
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
    write_api.write(bucket=bucket, record=points)
    print("successfully write data:", points.__sizeof__())


# write_api.write(bucket=bucket, record=points(data))

# query code
# query_api = client.query_api()
# query = 'from(bucket: "bucket") |> range(start: -10m) |> filter(fn: (r) => r["_measurement"] == "dex_screener") '
#
# result = query_api.query(org=org, query=query)
# for table in result:
#     for record in table.records:
#         print(record.values)
