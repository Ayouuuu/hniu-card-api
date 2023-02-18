import schedule
from foo.service import *
import os

# 以下部分代码由 ChatGPT 生成
# 12个楼栋，优先读取北八
data = ["001005", "001001", "001002", "001003", "001004", "001006", "001007", "001008", "001009", "001010", "001011",
        "001012"]
output_interval = 1  # 输出间隔，单位为分钟
output_size = 1  # 每次输出的数据量
output_index = 0  # 记录已经输出的数据索引
max_retries = 3  # 最大重试次数
retry_count = 0  # 当前重试次数


def login():
    # 账号 密码
    info = auth_login()
    if info['name'] != '':
        print("登陆成功！")
    else:
        login()


# 读取进度并更新 data 变量的值
def load_progress():
    global output_index
    try:
        with open('progress.json', 'r') as f:
            progress = json.loads(f.read())
            output_index = 0 if int(progress['index']) >= len(data) else int(progress['index'])
            return data
    except:
        return data


# 每10分钟输出一次数据的函数
def output_data(retry_count, max_retries):
    login()
    global data
    global output_index
    try:
        if output_index < len(data):
            if os.path.exists('progress.json'):
                os.remove('progress.json')
            areas = data[output_index:output_index + output_size]
            output_index += output_size
            print("正在写入", areas[0], "楼栋电费数据")
            result = write_room(areas[0])
            if result['code'] != 200:
                output_index -= output_size
            if output_index == len(data):
                output_index = 0
        else:
            output_index = 0
    except Exception as e:
        # 保存当前进度到文件中
        with open('progress.json', 'w') as f:
            f.write(json.dumps({'index': output_index}))

        # 检查重试次数
        if retry_count < max_retries:
            retry_count += 1
            print(f"An error occurred: {e}. Retrying in 10 minutes. Retry count: {retry_count}/{max_retries}")
            time.sleep(1 * 60)
            areas(retry_count, max_retries)
        else:
            # 重置重试计数器
            retry_count = 0
            print(f"Max retry count reached. Output data skipped.")


def run_job():
    global retry_count
    # 每1分钟输出一次数据，直到所有数据输出完毕
    schedule.clear("output")
    schedule.every(1).minutes.do(output_data, retry_count, max_retries).tag('output')


# 启动定时任务
data = load_progress()
print("已加载楼栋:", data, " 即将写入数据楼栋：", data[output_index])
run_job()
while True:
    schedule.run_pending()
    time.sleep(output_interval * 60)
