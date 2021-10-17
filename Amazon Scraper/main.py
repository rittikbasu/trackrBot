import time
import schedule
from sheets import write_data
from keepalive import keep_alive

schedule.every().hour.do(write_data)

while True:
    keep_alive()
    time.sleep(3600)
    schedule.run_pending()

