import sys
import time

import schedule

from cache_warmer.main import health_check

sys.path.append("/usr/local/lib/python3.11")


def check_service_health():
    health_check()


# Schedule the job every 5 minutes
schedule.every(5).minutes.do(check_service_health)

# Keep running the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
