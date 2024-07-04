"""
根据配置的 cron 表达式定时执行任务。
"""
import time
import schedule
from SyncPypi import SyncPypi


syncPypi = SyncPypi()

# 定义任务函数
def run_task():
    print(f"Running task at {time.strftime('%Y-%m-%d %H:%M:%S')} ...")
    syncPypi.execute_pip_download()
    syncPypi.create_pypi_index()
    print("Task completed.")


# 设置定时任务，每天凌晨02:00执行
schedule.every().day.at("15:16").do(run_task)

# 循环执行任务
while True:
    schedule.run_pending()
    time.sleep(1)
